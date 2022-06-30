import os
import io
import gym
import math
import pygame
import random
import imageio
import numpy as np
from gym.spaces import Box
from pygame import Vector2
from ray.rllib.env.env_context import EnvContext

from PLSimulator.constants import ASSET_DATA_DIRECTORY
from PLSimulator.entities.pencil import Pencil
from PLSimulator.entities.static import Ground
from PLSimulator.entities.static import LandingPad


class Environment(gym.Env):
    '''
        Environment

        This is the environment class for the pencil landing simulation.
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
        self._gravity = config["physics"]["gravity"]
        self._density = config["physics"]["density"]
        self._land_ang = config["physics"]["land_ang"]
        self._land_vel = config["physics"]["land_vel"]

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
        self.total_reward = 0
        self._min_fuel = config["agent"]["min_fuel"]
        self._max_fuel = config["agent"]["max_fuel"]
        self._min_pos = config["agent"]["min_pos"]
        self._max_pos = config["agent"]["max_pos"]
        self._min_ang = config["agent"]["min_ang"]
        self._max_ang = config["agent"]["max_ang"]
        self._min_vel = config["agent"]["min_vel"]
        self._max_vel = config["agent"]["max_vel"]

        # Set up window
        self._window_width = config["window"]["width"]
        self._window_height = config["window"]["height"]
        self._window_bg_colour = config["window"]["colour"]
        self._window_frames = []
        self.window = None

    def reset(self) -> list:
        '''
            Reset the environment to starting conditions

            Parameters:
                None

            Returns:
                state: Starting state of environment
        '''
        self.pencil.position = Vector2(
            random.uniform(self._min_pos[0] * self._window_width, self._max_pos[0] * self._window_width),
            random.uniform(self._min_pos[1] * self._window_width, self._max_pos[1] * self._window_width),
        )
        self.pencil.velocity = Vector2(
            random.uniform(self._min_vel[0] * self._window_width, self._max_vel[0] * self._window_width),
            random.uniform(self._min_vel[1] * self._window_width, self._max_vel[1] * self._window_width),
        )
        self.pencil.angle = random.uniform(self._min_ang, self._max_ang)
        self.pencil.fuel_mass = random.uniform(self._min_fuel, self._max_fuel)
        self.total_reward = 0

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
                round((self.pad.velocity - self.pencil.velocity)[0], 1),
                round((self.pad.velocity - self.pencil.velocity)[1], 1),
                round((self.pad.angle - self.pencil.angle) / 45, 1)
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
        state = self.state()

        info = {
            "outcome": "none",
            "pos": Vector2(state[0], state[1]),
            "vel": Vector2(state[2], state[3]),
            "ang": round(state[4], 1),
            "fuel": round(self.pencil.fuel_mass, 1),
            "legs": 0,
        }

        self.step_collisions(info)
        self.step_physics(action)
        reward, done = self.step_rewards(info)
        self.total_reward += reward

        return state, reward, done, info

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
                info["outcome"] = "failed"
                break

            # Detect if both legs are touching the landing pad
            if self.pencil.entities[3] in c and self.pad in c:
                info["legs"] += 1
            if self.pencil.entities[4] in c and self.pad in c:
                info["legs"] += 1

        # Check if both landing legs are on pad
        if not info["outcome"] == "failed" and info["legs"] == 2:
            # Check the pencil velocity and angle are within bounds
            velCondition = abs(self.pad.velocity.magnitude() - self.pencil.velocity.magnitude()) < self._land_vel
            angCondition = abs(self.pad.angle - self.pencil.angle) < self._land_ang

            # Update landed and crashed states
            info["outcome"] = "success" if velCondition and angCondition else "failed"

        # Check if pencil is within bounds of screen
        if self.pencil.position[0] < 0 or self.pencil.position[0] > self._window_width or self.pencil.position[1] < 0:
            info["outcome"] = "failed"

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
        cd = 0.5 * math.sin(math.radians(heading)) + 0.5
        drag = 0.5 * cd * 1 * self._density * Vector2(self.pencil.velocity[0]**2, self.pencil.velocity[1]**2)
        if self.pencil.velocity[0] > 0:
            drag[0] *= -1
        if self.pencil.velocity[1] > 0:
            drag[1] *= -1
        drag = self._force_scale * drag

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
        slowing = not (
            np.sign(distance[0]) != np.sign(acceleration[0]) and np.sign(distance[1]) != np.sign(acceleration[1])
        )

        # Reward if pencil is not firing engine far from landing pad
        if abs(acceleration.magnitude()) <= 0 and distance.magnitude() > 0.5:
            reward += 2
        # Reward if pencil is moving and slowing towards landing pad
        elif moving and slowing or distance.magnitude() < 0.5 and velocity.magnitude() <= self._land_vel:
            reward += 8 * (0.5 - distance.magnitude()) * math.cos(math.radians(self.pencil.angle))
        # Otherwise negatively reward pencil
        else:
            reward -= 8

        # Reward agent for successful landing vs crash landing
        if info["outcome"] == "success":
            reward += 100 + self.pencil.fuel_mass * 10
        if info["outcome"] == "failed":
            reward -= 100

        return round(reward, 1), info["outcome"] in ["success", "failed"]

    def render(self, save_video: bool = False) -> None:
        '''
            Render the entities to window

            Paramters:
                save_video: Whether to save simulation as a video

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

        # Save this frame in list
        if save_video:
            frame = io.BytesIO()
            pygame.image.save(self.window, frame, "PNG")
            self._window_frames.append(imageio.imread(frame))

    def save_video(self, dir: str = '', fps: int = 30):
        '''
            Save the window frames collection as a gif

            Parameters:
                dir: The directory to store the gif in
                fps: Frames per second for the gif

            Returns:
                None
        '''
        imageio.mimsave(os.path.join(dir, "simulation.gif"), self._window_frames, 'GIF', duration=1 / fps)
