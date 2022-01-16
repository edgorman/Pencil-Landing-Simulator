import os
import random
from abc import abstractmethod

import pygame


class BaseAgent:
    ''' BaseAgent
    
        This is the agent class from which all other agents will inherit.
    '''

    def __init__(self, x=0, y=0, dx=0, dy=0, an=0):
        ''' Initialise the agent 
        
            Parameters:
                x: X position of agent (default is 0)
                y: Y position of agent (default is 0)
                dx: X velocity of agent (default is 0)
                dy: Y velocity of agent (default is 0)
                an: Angle of agent (default is 0)
            
            Returns:
                none
        '''
        # Set up model parameters
        self.load_model = False
        self.state_size = 4
        self.action_size = 3

        # Set up positional parameters
        self.startParameters = (x, y, dx, dy, an, 0, 0)
        self.reset()

        # Set up view in pygame
        image_path = os.path.join(os.getcwd(), 'pencil-landing-simulator', 'assets', 'pencil.png')
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (16, 128))
    
    def reset(self, seed=random.randint(0, 10e6)):
        ''' Reset the agent to starting parameters
        
            Parameters: 
                none
            
            Returns:
                none
        '''
        self.x = self.startParameters[0]
        self.y = self.startParameters[1]
        self.dx = self.startParameters[2]
        self.dy = self.startParameters[3]
        self.an = self.startParameters[4]
        self.ax = self.startParameters[5]
        self.ay = self.startParameters[6]
    
    @abstractmethod
    def get_action(self, state):
        ''' Get the action of the agent given an environment state
        
            Parameters:
                state: State of the environment
            
            Returns
                action: Action of the agent in environment
        '''
    
    @abstractmethod
    def train(self, environment, render=False):
        ''' Trains the agent and stores the result in self.model
        
            Paremeters:
                environment: Environment to train agent in
                render: Whether to render the training (default is False)
            
            Returns:
                none
        '''
    