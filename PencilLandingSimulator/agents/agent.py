import os
import random
from abc import abstractmethod

import pygame

from PencilLandingSimulator.constants import ASSET_DATA_DIRECTORY


class BaseAgent:
    ''' BaseAgent

        This is the agent class from which all other agents will inherit.
    '''

    def __init__(self, asset_name='pencil.png'):
        ''' Initialise the agent

            Parameters:
                None

            Returns:
                none
        '''
        # Set up agent parameters
        self._dry_mass = 10
        self._max_fuel = 100
        self._fuel = self._max_fuel

        # Set up model parameters
        self._load_model = False
        self._state_size = 4
        self._action_size = 3

        # Set up view in pygame
        image_path = os.path.join(ASSET_DATA_DIRECTORY, asset_name)
        self._image = pygame.image.load(image_path)
        self._image = pygame.transform.scale(self._image, (16, 128))
    
    @property
    def fuel(self):
        '''
            Return the amount of fuel remaining

            Parameters:
                None
            
            Returns:
                fuel: Amount of fuel remaining
        '''
        return self._fuel
    
    @property
    def mass(self):
        '''
            Return the mass of the agent in terms of wet and dry mass

            Parameters:
                None
            
            Returns:
                mass: Mass of the agent
        '''
        return self._dry_mass + self._fuel

    def reset(self, pos=(0, 0), vel=(0, 0), ang=0, acc=(0, 0)):
        ''' 
            Reset the agent to starting parameters

            Parameters:
                pos: Starting position of the agent
                vel: Starting velocity of the agent
                ang: Starting angle of the agent
                acc: Starting acceleration of the agent

            Returns:
                None
        '''
        self.x, self.y = pos
        self.dx, self.dy = vel
        self.an = ang
        self.ax, self.ay = acc

    @abstractmethod
    def get_action(self, state):
        ''' 
            Get the action of the agent given an environment state

            Parameters:
                state: State of the environment

            Returns
                action: Action of the agent in environment
        '''

    @abstractmethod
    def train(self, environment, render=False):
        ''' 
            Trains the agent and stores the result in self.model

            Paremeters:
                environment: Environment to train agent in
                render: Whether to render the training (default is False)

            Returns:
                none
        '''
