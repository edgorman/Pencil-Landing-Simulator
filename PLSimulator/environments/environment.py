import os
import gym
import math
import pygame
import numpy as np
from gym.spaces import Box
from pygame import Vector2

from PLSimulator.constants import ASSET_DATA_DIRECTORY
from PLSimulator.entities.entity import BaseEntity


class BaseEnvironment(gym.Env):
    '''
        BaseEnvironment

        This is the environment class from which all other environments will inherit.
        It inherits from the gym environment class.
    '''

    def __init__(
        self,
        entities: list = [],
        width: int = 1280,
        height: int = 720,
        bg_colour: tuple = (0, 0, 0)) -> None:
        '''
            Initialise the environment

            Parameters:
                entities: The entities interacting in the environment
                width: Width of the window (default is 1600)
                height: Height of the window (default is 900)
                bg_colour: Colour of the background

            Returns:
                None
        '''
        # Set up pencil
        parts = [
            BaseEntity('engine firing.png', Vector2(16, 80), Vector2(0, 84), Vector2(0, 0), 0, 0, [], False),
            BaseEntity('rcs firing.png', Vector2(16, 16), Vector2(14, 53), Vector2(0, 0), 180, 0, [], False),
            BaseEntity('rcs firing.png', Vector2(16, 16), Vector2(14, -53), Vector2(0, 0), 0, 0, [], False),
        ]
        self._fuel = 20
        self._dry_mass = 10
        mass = self._fuel + self._dry_mass
        self._pencil = BaseEntity('pencil.png', Vector2(16, 128), Vector2(0, 0), Vector2(0, 0), 0, mass, parts, True)

        # Set up entities
        self._entities = entities
        self._entities.append(self._pencil)
        self._rotation_scale = 0.1
        self._force_scale = 0.05

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
        self.running = False
        self.window = pygame.display.set_mode((self._window_width, self._window_height))
        self.clock = pygame.time.Clock()

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
        # Convert agent actions into forces
        thrust = -action[0] * 15 * self._force_scale
        left = -action[1] * 15 * self._rotation_scale
        right = action[2] * 15 * self._rotation_scale

        # Check if agent has enough fuel to fire engine
        if self._fuel <= 0:
            thrust = 0
        
        # Remove fuel from agent if fired engine
        if abs(thrust) > 0:
            self._fuel -= 0.1
            self._pencil.mass = self._dry_mass + self._fuel
        
        # Calculate new heading of pencil
        heading = self._pencil.angle + left + right
        heading_rads = math.radians(heading)

        # Move agent under it's own thrust
        thrust = thrust * Vector2(math.sin(heading_rads), math.cos(heading_rads))
        self._pencil.update_position(thrust, heading)

        return self.state(), 0, False, {}

    def render(self) -> None:
        '''
            Render the entities to window

            Paramters:
                None

            Returns:
                None
        '''
        self.window.fill(self._window_bg_colour)

        for entity in self._entities:
            if entity.isRenderable:
                pivot = entity.position + entity._asset_size
                images = entity.render(pivot)
                for image, position in images:
                    self.window.blit(image, position)

        pygame.display.update()
