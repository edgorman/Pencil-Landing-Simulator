import os
import pygame


class BaseAgent:
    ''' BaseAgent
    
        This is the agent class from which all other agents will inherit.
    '''

    def __init__(self, x, y):
        ''' Initialise the agent 
        
            Parameters:
                none
            
            Returns:
                none
        '''

        # Set up default parameters
        self.reward = 0

        # Set up positional parameters
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.ax = 0
        self.ay = 0.001
        self.angle = 0

        # Set up view
        self.assets_path = os.path.join(os.getcwd(), 'pencil-landing-simulator', 'assets')
        self.image = pygame.image.load(os.path.join(self.assets_path, 'pencil.png'))
        self.image = pygame.transform.scale(self.image, (16, 128))
    
    def get_action(self, state):
        ''' Get the next action of the agent
        
            Parameters:
                state: State of the environment
            
            Returns: 
                action: The next action for the agent
        '''

        return [0, 1, 0]
    
    def give_reward(self, reward):
        ''' Give the reward from the environment
        
            Parameters:
                reward: Value of how well agent performed
            
            Returns:
                none
        '''

        pass
