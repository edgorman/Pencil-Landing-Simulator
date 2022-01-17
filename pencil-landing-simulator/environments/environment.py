import random
from abc import abstractmethod

import gym
import pygame

class BaseEnvironment(gym.Env):
    ''' BaseEnvironment

        This is the environment class from which all other environments will inherit.
        It inherits from the gym environment class.
    '''

    def __init__(self, agent, goal_position, width=1600, height=900):
        ''' Initialise the environment 
        
            Parameters:
                agent: The agent active in this environment
                width: Width of the window (default is 1600)
                height: Height of the window (default is 900)
            
            Returns:
                none
        '''
        # Set up environment
        self.observation_space = gym.spaces.Discrete(4)
        self.action_space = gym.spaces.Discrete(3)
        self.goal_position = goal_position

        # Set up agent
        self.agent = agent

        # Set up window 
        self.window_width = width
        self.window_height = height

        # Set up pygame
        pygame.init()
        self.running = False
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        self.clock = pygame.time.Clock()

    def reset(self, seed=random.randint(0, 10e6)):
        ''' Reset the environment to starting conditions 
        
            Parameters:
                seed: Seed used to influence starting state
            
            Returns:
                state: Starting state of environment
        '''
        self.agent.reset()
        self.running = True
        return self.get_state()
    
    @abstractmethod
    def get_state(self):
        ''' Get the current state of the environment
        
            Parameters:
                none
            
            Returns:
                Tuple where:
                    0 = Distance of agent to ground
                    1 = X velocity of agent relative to ground
                    1 = Y velocity of agent relative to ground
                    2 = Angle of agent relative to ground normal
        '''

    @abstractmethod    
    def step(self, action):
        ''' Step the environment given an action by agent 
        
            Parameters:
                action: The action made by the agent during this step
            
            Returns:
                state: Next state of the environment
                reward: Value to reward the agent
                done: Whether the environment is done
                info: Any extra information about environment
        '''
    
    @abstractmethod
    def render(self):
        ''' Render the environment to screen 
        
            Paramters:
                none
            
            Returns:
                none
        '''
