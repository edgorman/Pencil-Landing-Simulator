import os
import gym
import math
import pygame
import numpy as np
from gym.spaces import Box
from pygame import Vector2

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

    def __init__(
        self,
        gravity: float = 9.8,
        density: float = 1.0,
        max_fuel: float = 20,
        bg_colour: tuple = (137, 207, 240),
        width: int = 640,
        height: int = 900) -> None:
        '''
            Initialise the environment

            Parameters:
                gravity: Gravity of body (0 if none present)
                density: Density of atmosphere (0 if none present)
                max_fuel: Max amount of fuel available to agent
                bg_colour: Colour of environment background
                width: Width of the window (default is 640)
                height: Height of the window (default is 900)

            Returns:
                None
        '''
        # Set up entities
        self._max_fuel = max_fuel
        self._fuel, self._dry_mass = max_fuel, 15
        self.entities = {
            'pencil': Pencil(),
            'ground': Ground(),
            'landingPad': LandingPad()
        }

        # Set up forces
        self._rotation_scale = 0.1
        self._force_scale = 0.35
        self._gravity = gravity
        self._density = density

        # Set up environment
        self.action_space = Box(
            np.array([0, 0, 0], dtype=np.float32),
            np.array([1, 1, 1], dtype=np.float32),
            dtype=np.float32
        )
        self.observation_space = Box(
            np.array([-1, 0, 0, 0], dtype=np.float32),
            np.array([1, 1, 1, 1], dtype=np.float32),
            dtype=np.float32
        )

        # Set up window
        self._window_width = width
        self._window_height = height
        self._window_bg_colour = bg_colour
        image_path = os.path.join(ASSET_DATA_DIRECTORY, 'pencil.png')
        self._icon = pygame.image.load(image_path).subsurface(0, 0, 16, 16)
        pygame.display.set_icon(self._icon)
        pygame.display.set_caption('Pencil Landing Simulator')

        # Set up pygame
        pygame.init()
        self.window = pygame.display.set_mode((self._window_width, self._window_height))
        self.clock = pygame.time.Clock()
        self.running = False

    def reset(self) -> list:
        '''
            Reset the environment to starting conditions

            Parameters:
                None

            Returns:
                state: Starting state of environment
        '''
        self.running = True
        return self.state()

    def state(self) -> list:
        '''
            Get the current state of the environment

            Parameters:
                None

            Returns:
                state: Information about the environment in relation to the agent
        '''
        return [0, 0, 0, 0]

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
        pencil = self.entities["pencil"]
        reward = 0
        info = {
            "landed": False,
            "crashed": False,
            "legs_on_pad": [],
            "fuel_left": round(self._fuel, 1)
        }

        self.step_collisions(info, pencil)
        self.step_physics(info, pencil, action)
        self.step_rewards(info, pencil, reward)

        return self.state(), reward, info["landed"] or info["crashed"], info

    def step_collisions(self, info: dict, pencil: Pencil):
        collisions = []

        # Collect collisions between pencil and other entities
        for other in [self.entities["ground"], self.entities["landingPad"]]:
            collisions.extend(pencil.collides_with(other))
        collisions = set(collisions)

        # For each collision, check for crash/landing cases
        for c in collisions:
            # Detect if pencil is touching ground or landing pad
            if pencil in c and self.entities["ground"] in c or \
               pencil in c and self.entities["landingPad"] in c or \
               pencil.entities[3] in c and self.entities["ground"] in c or \
               pencil.entities[4] in c and self.entities["ground"] in c:
                info["crashed"] = True
                break
            
            # Detect if both legs are touching the landing pad
            if pencil.entities[3] in c and self.entities["landingPad"] in c:
                info["legs_on_pad"].append(pencil.entities[3])
            if pencil.entities[4] in c and self.entities["landingPad"] in c:
                info["legs_on_pad"].append(pencil.entities[4])
        
        # Calculate if a landing has occurred
        # TODO: Need to check velocity of pencil entity
        if not info["crashed"] and len(info["legs_on_pad"]) == 2:
            info["landed"] = True
    
    def step_physics(self, info: dict, pencil: Pencil, action: list):
        # Check if agent has enough fuel to fire engine
        # TODO: see if theres a nicer way to write this
        if self._fuel <= 0:
            action[0] = 0
        elif abs(action[0]) > 0:
            self._fuel -= 0.1
            pencil.mass = self._dry_mass + self._fuel

        # Convert agent actions into forces
        thrust = -action[0] * 12 * self._force_scale
        left = -action[1] * 12 * self._rotation_scale
        right = action[2] * 12 * self._rotation_scale
        heading = pencil.angle + left + right
        pencil.update_entities(action)

        # Move pencil under the forces of its thrust, gravity and drag:
        thrust = thrust * Vector2(math.sin(math.radians(heading)), math.cos(math.radians(heading)))
        gravity = self._force_scale * Vector2(0, self._gravity)
        # drag is calculated using: Fd = 0.5 * Cd * A * p * V^2
        # TODO: drag coeff should be relative to angle of pencil (e.g. larger when horizontal)
        drag = 0.5 * 0.82 * 1 * self._density * Vector2(pencil.velocity[0]**2, pencil.velocity[1]**2)
        drag = self._force_scale * drag.rotate(180)
        
        # Update pencils position under external and internal forces
        pencil.update_position(gravity + drag)
        pencil.update_position(thrust, heading)

    def step_rewards(self, info: dict, pencil: Pencil, reward: float):
        # Reward agent for moving closer to goal and conserving fuel
        # TODO: Reimplment this
        reward += 1

    def render(self) -> None:
        '''
            Render the entities to window

            Paramters:
                None

            Returns:
                None
        '''
        # Clear screen
        self.window.fill(self._window_bg_colour)

        # For each entity, render if renderable
        for _, entity in self.entities.items():
            if entity.isRenderable:
                # Calculate pivot and render entity around that
                pivot = entity.position + entity._asset_size
                images = entity.render(pivot)

                # Render all images that make up entity
                for image, position in images:
                    self.window.blit(image, position)

        pygame.display.update()
