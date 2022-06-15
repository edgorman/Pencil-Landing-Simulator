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
                width: Width of the window (default is 1280)
                height: Height of the window (default is 720)

            Returns:
                None
        '''
        # Set up pencil
        parts = [
            BaseEntity('engine_firing.png', Vector2(16, 80), Vector2(0, 84), Vector2(0, 0), 0, 0, [], False, False),
            BaseEntity('rcs_firing.png', Vector2(16, 16), Vector2(14, 53), Vector2(0, 0), 180, 0, [], False, False),
            BaseEntity('rcs_firing.png', Vector2(16, 16), Vector2(14, -53), Vector2(0, 0), 0, 0, [], False, False),
        ]
        self._max_fuel = max_fuel
        self._fuel, self._dry_mass = max_fuel, 10
        self._pencil = BaseEntity('pencil.png', Vector2(16, 128), Vector2(0, 0), Vector2(0, 0), 0, self._fuel + self._dry_mass, parts, True)

        # Set up landing zone
        self._lander = BaseEntity('landing_zone.png', Vector2(256, 16), Vector2(0, height - 24), Vector2(0, 0), 0, 100, [], True)

        # Set up entities
        self._entities = []
        self._entities.extend([self._pencil, self._lander])

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
        reward = 0
        done = False
        info = {}

        # Convert agent actions into forces
        # and sacle by the force scale
        thrust = -action[0] * 15 * self._force_scale
        left = -action[1] * 15 * self._rotation_scale
        right = action[2] * 15 * self._rotation_scale

        # Check if agent has enough fuel to fire engine
        if self._fuel <= 0:
            thrust = 0
        elif abs(thrust) > 0:
            self._fuel -= 0.1
            self._pencil.mass = self._dry_mass + self._fuel
        
        # Move pencil under gravity and drag, where
        # drag is calculated using: Fd = 0.5 * Cd * A * p * V^2
        gravity = self._force_scale * Vector2(0, self._gravity)
        drag = 0.5 * 0.82 * 1 * self._density * Vector2(self._pencil.velocity[0]**2, self._pencil.velocity[1]**2)
        drag = self._force_scale * drag.rotate(180)

        # Move pencil under force of it's own thrust
        heading = self._pencil.angle + left + right
        thrust = thrust * Vector2(math.sin(math.radians(heading)), math.cos(math.radians(heading)))
        
        # Update pencils position under external and internal forces
        self._pencil.update_position(gravity + drag)
        self._pencil.update_position(thrust, heading)

        # Update pencil sub-entities rendering
        for i, entity in enumerate(self._pencil.entities):
            entity.isRenderable = action[i] != 0
        
        # Determine if pencil has entered a final state
        if self._pencil.collides_with(self._lander):
            done = True

        return self.state(), reward, done, info

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
        for entity in self._entities:
            if entity.isRenderable:
                # Calculate pivot and render entity around that
                pivot = entity.position + entity._asset_size
                images = entity.render(pivot)

                # Render all images that make up entity
                for image, position in images:
                    self.window.blit(image, position)

        pygame.display.update()
