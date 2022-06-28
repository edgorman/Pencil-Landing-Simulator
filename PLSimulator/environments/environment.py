import os
import gym
import math
import pygame
import numpy as np
from gym.spaces import Box
from pygame import Vector2
from ray.rllib.env.env_context import EnvContext

from PLSimulator.constants import ASSET_DATA_DIRECTORY
from PLSimulator.entities.pencil import Pencil
from PLSimulator.entities.static import Ground
from PLSimulator.entities.static import LandingPad


class BaseEnvironment(gym.Env):
    '''
        BaseEnvironment

        This is the environment class from which all other environments will inherit.
        It inherits from the gym environment class.
    '''

    def __init__(self, config: EnvContext) -> None:
        '''
            Initialise the environment

            Parameters:
                config: The parameters used to initialise the environment

            Returns:
                None
        '''
        # Set up entities
        self.pencil = Pencil()
        self.ground = Ground()
        self.pad = LandingPad()
        self.entities = [
            self.pencil,
            self.ground,
            self.pad
        ]

        # Set up forces
        self._rotation_scale = 0.1
        self._force_scale = 0.35
        self._gravity = config["gravity"]
        self._density = config["density"]

        # Set up environment
        self.action_space = Box(
            np.array([0, 0, 0], dtype=np.int),
            np.array([1, 1, 1], dtype=np.int),
            dtype=np.int
        )
        self.observation_space = Box(
            np.array([-1, -1, -1, -1, -1], dtype=np.float32),
            np.array([1, 1, 1, 1, 1], dtype=np.float32),
            dtype=np.float32
        )

        # Set up window
        self._window_width = config["width"]
        self._window_height = config["height"]
        self._window_bg_colour = config["bg_colour"]
        self.window = None

    def reset(self) -> list:
        '''
            Reset the environment to starting conditions

            Parameters:
                None

            Returns:
                state: Starting state of environment
        '''
        self.pencil.position = Vector2(312, 64)
        self.pencil.velocity = Vector2(0, 0)
        self.pencil.angle = 0
        self.pencil.fuel_mass = self.pencil.start_fuel

        return self.state()

    def state(self) -> list:
        '''
            Get the current state of the environment

            Parameters:
                None

            Returns:
                state: Information about the environment in relation to the agent
        '''
        return np.clip(
            np.array([
                round((self.pad.position - self.pencil.position)[0] / self._window_width, 1),
                round((self.pad.position - self.pencil.position)[1] / self._window_height, 1),
                round((self.pad.velocity - self.pencil.velocity)[0] / 100, 1),
                round((self.pad.velocity - self.pencil.velocity)[1] / 100, 1),
                round((self.pad.angle - self.pencil.angle) / 90, 1)
            ], dtype=np.float32),
            -1,
            1
        )

    def step(self, action: list) -> tuple:
        '''
            Step the environment given an action by agent

            Parameters:
                action: The action made by the agent during this step

            Returns:
                state: Next state of the environment
                reward: Value to reward the agent
                done: Whether the environment is done
                info: Any extra information about environment
        '''
        info = {
            "landed": False,
            "crashed": False,
            "fuel_left": round(self.pencil.fuel_mass, 1),
            "legs_on_pad": 0,
            "land_velocity": 0
        }

        self.step_collisions(info)
        self.step_physics(action)
        reward = self.step_rewards(info)

        return self.state(), reward, info["landed"] or info["crashed"], info

    def step_collisions(self, info: dict):
        # Collect collisions between pencil and other entities
        collisions = []
        for entity in self.entities:
            collisions.extend(self.pencil.collides_with(entity))
        collisions = set(collisions)

        # For each collision, check for crash/landing cases
        for c in collisions:
            # Detect if pencil is touching ground or landing pad
            if self.pencil in c and self.ground in c or \
               self.pencil in c and self.pad in c or \
               self.pencil.entities[3] in c and self.ground in c or \
               self.pencil.entities[4] in c and self.ground in c:
                info["crashed"] = True
                break

            # Detect if both legs are touching the landing pad
            if self.pencil.entities[3] in c and self.pad in c:
                info["legs_on_pad"] += 1
            if self.pencil.entities[4] in c and self.pad in c:
                info["legs_on_pad"] += 1

        # Check if both landing legs are on pad
        if not info["crashed"] and info["legs_on_pad"] == 2:
            # Check the pencil velocity and angle are within bounds
            velCondition = abs(self.pad.velocity.magnitude() - self.pencil.velocity.magnitude()) < 2
            angCondition = abs(self.pad.angle - self.pencil.angle) < 5

            # Update landed and crashed states
            info["landed"] = velCondition and angCondition
            info["crashed"] = not info["landed"]
        info["land_velocity"] = round(abs((self.pad.velocity - self.pencil.velocity).magnitude()) / 100, 1)

        # Check if pencil is within bounds of screen
        if self.pencil.position[0] < 0 or self.pencil.position[0] > self._window_width or self.pencil.position[1] < 0:
            info["crashed"] = True

    def step_physics(self, action: list):
        # Check if agent has enough fuel to fire engine
        if action[0] > 0 and not self.pencil.fire_engine():
            action[0] = 0

        # Convert agent actions into forces
        thrust = -action[0] * 12 * self._force_scale
        left = -action[1] * 12 * self._rotation_scale
        right = action[2] * 12 * self._rotation_scale
        heading = self.pencil.angle + left + right
        self.pencil.update_entities(action)

        # Move pencil under the forces of its thrust, gravity and drag:
        thrust = thrust * Vector2(math.sin(math.radians(heading)), math.cos(math.radians(heading)))
        gravity = self._force_scale * Vector2(0, self._gravity)
        # drag is calculated using: Fd = 0.5 * Cd * A * p * V^2
        # TODO: drag coeff should be relative to angle of pencil (e.g. larger when horizontal)
        drag = 0.5 * 0.82 * 1 * self._density * Vector2(self.pencil.velocity[0]**2, self.pencil.velocity[1]**2)
        drag = self._force_scale * drag.rotate(180)

        # Update pencils position under external and internal forces
        self.pencil.update_position(gravity + drag)
        self.pencil.update_position(thrust, heading)

    def step_rewards(self, info: dict):
        # Reward agent for conserving fuel
        reward = 0

        # Calculate distance/velocity/acceleration of pencil relative to landing pad
        distance = (self.pad.position - self.pencil.position) / self.pad.position.magnitude()
        velocity = (self.pad.velocity - self.pencil.velocity)
        acceleration = (self.pad.acceleration - self.pencil.acceleration)

        # Determine if pencil is moving/slowing towards landing pad
        moving = np.sign(distance[0]) != np.sign(velocity[0]) and np.sign(distance[0]) != np.sign(velocity[1])
        slowing = not (np.sign(distance[0]) != np.sign(acceleration[0]) and np.sign(distance[1]) != np.sign(acceleration[1]))

        # Reward if pencil is not firing engine far from landing pad
        if abs(acceleration.magnitude()) <= 0 and distance.magnitude() > 0.5:
            reward += 2
        # Reward if pencil is moving and slowing towards landing pad
        elif moving and slowing or distance.magnitude() < 0.5 and velocity.magnitude() <= 2.0:
            reward += 8 * (0.5 - distance.magnitude()) * math.cos(math.radians(self.pencil.angle))
        # Otherwise negatively reward pencil 
        else:
            reward -= 8
        
        # Reward agent for successful landing vs crash landing
        if info["landed"]:
            reward += 100
        if info["crashed"]:
            reward -= 100

        return round(reward, 1)

    def render(self) -> None:
        '''
            Render the entities to window

            Paramters:
                None

            Returns:
                None
        '''
        # Set up pygame
        if self.window is None:
            image_path = os.path.join(ASSET_DATA_DIRECTORY, 'pencil.png')
            self._icon = pygame.image.load(image_path).subsurface(0, 0, 16, 16)
            pygame.display.set_icon(self._icon)
            pygame.display.set_caption('Pencil Landing Simulator')

            pygame.init()
            self.window = pygame.display.set_mode((self._window_width, self._window_height))
            self.clock = pygame.time.Clock()

        # Clear screen
        self.window.fill(self._window_bg_colour)

        # For each entity, render if renderable
        for entity in self.entities:
            if entity.isRenderable:
                images = entity.render(entity.position)

                # Render all images that make up entity
                for image, position in images:
                    self.window.blit(image, position)

        pygame.display.update()
