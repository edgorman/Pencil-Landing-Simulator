import gym
import pygame
from pygame import Vector2
from abc import abstractmethod

from PLSimulator.agents.agent import BaseAgent


class BaseEnvironment(gym.Env):
    '''
        BaseEnvironment

        This is the environment class from which all other environments will inherit.
        It inherits from the gym environment class.
    '''

    def __init__(
        self,
        agent: BaseAgent,
        entities: list = [],
        width: int = 1600,
        height: int = 900,
        bg_colour: tuple = (0, 0, 0)) -> None:
        '''
            Initialise the environment

            Parameters:
                agent: The agent operating in the environment
                entities: The entities interacting in the environment
                gravity: Force applied to agent in a downward direction
                max_velocity: Max velocity achievable in environment
                width: Width of the window (default is 1600)
                height: Height of the window (default is 900)
                bg_colour: Colour of the background

            Returns:
                None
        '''
        # Set up entities
        self._agent = agent
        self._entities = entities
        self._entities.append(agent)

        # Set up environment
        self._rotation_scale = 0.1
        self._force_scale = 0.05

        # Set up window
        self._window_width = width
        self._window_height = height
        self._window_bg_colour = bg_colour

        # Set up pygame
        pygame.init()
        self.running = False
        self.window = pygame.display.set_mode((self._window_width, self._window_height))
        self.clock = pygame.time.Clock()

    @abstractmethod
    def reset(self) -> list:
        '''
            Reset the environment to starting conditions

            Parameters:
                None

            Returns:
                state: Starting state of environment
        '''

    @abstractmethod
    def state(self) -> list:
        '''
            Get the current state of the environment

            Parameters:
                None

            Returns:
                state: Information about the environment in relation to the agent
        '''

    @abstractmethod
    def step(self, action: list) -> list:
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
