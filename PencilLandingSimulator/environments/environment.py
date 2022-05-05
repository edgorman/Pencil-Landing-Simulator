from abc import abstractmethod

import gym
import pygame

from PencilLandingSimulator.agents.agent import BaseAgent


class BaseEnvironment(gym.Env):
    ''' 
        BaseEnvironment

        This is the environment class from which all other environments will inherit.
        It inherits from the gym environment class.
    '''

    def __init__(
        self,
        goal_pos: tuple,
        goal_eps: tuple,
        vel_eps: float,
        vel_max: float = float('inf'),
        gravity: float = 9.8,
        width: int = 1600,
        height: int = 900) -> None:
        ''' 
            Initialise the environment

            Parameters:
                goal_pos: Position the agent should end at
                goal_eps: Positional margin allowed for agent when landing
                vel_eps: Velocity margin allowed for agent when landing
                vel_max: Max velocity achievable in environment
                gravity: Force applied to agent in a downward direction
                width: Width of the window (default is 1600)
                height: Height of the window (default is 900)

            Returns:
                None
        '''
        # Set up environment
        self._observation_space = gym.spaces.Discrete(4)
        self._action_space = gym.spaces.Discrete(3)

        # Set up variables for agent
        self._goal_pos = goal_pos
        self._goal_eps = goal_eps
        self._vel_eps = vel_eps
        self._vel_max = vel_max
        self._gravity = gravity

        # Set up window
        self._window_width = width
        self._window_height = height

        # Set up pygame
        pygame.init()
        self._running = False
        self._window = pygame.display.set_mode((self._window_width, self._window_height))
        self._clock = pygame.time.Clock()

    @abstractmethod
    def reset(self, agent: BaseAgent) -> list:
        '''
            Reset the environment and agent to starting conditions

            Parameters:
                agent: Agent to set in the environment

            Returns:
                state: Starting state of environment
        '''

    @abstractmethod
    def get_state(self) -> list:
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

    @abstractmethod
    def render(self) -> None:
        '''
            Render the environment to screen

            Paramters:
                None

            Returns:
                None
        '''
