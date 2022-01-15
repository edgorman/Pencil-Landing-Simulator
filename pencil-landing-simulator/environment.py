import gym
import math
import pygame

class BaseEnvironment(gym.Env):
    ''' BaseEnvironment

        This is the environment class from which all other environments will inherit.
        It inherits from the gym environment class.
    '''

    def __init__(self, agent):
        ''' Initialise the environment 
        
            Parameters:
                agent: Agent object to run in environment
            
            Returns:
                none
        '''
        # Set up environment
        self.observation_space = gym.spaces.Discrete(8)
        self.action_space = gym.spaces.Discrete(8)

        # Set up window 
        self.window_width = 1600
        self.window_height = 900

        # Set up pygame
        pygame.init()
        self.running = False
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        self.clock = pygame.time.Clock()

        # Set up agent
        self.agent = agent

    def reset(self):
        ''' Reset the environment to starting conditions 
        
            Parameters:
                none
            
            Returns:
                state: Starting state of environment
        '''

        self.running = True
        return None
    
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
        distance = self.window_height - self.agent.y
        velocityX = self.agent.dx
        velocityY = self.agent.dy
        angle = math.radians(0) - math.radians(self.agent.angle)

        return [distance, velocityX, velocityY, angle]

    def step(self, action):
        ''' Step the environment given an action by agent 
        
            Parameters:
                action: The action made by the agent during this step
            
            Returns:
                reward: Value to reward the agent
                info: Any extra information about environment
        '''
        rotation_scale = 0.15
        acceleration_scale = -1.05

        # Apply rotation due to action
        self.agent.angle += action[1] * rotation_scale
        self.agent.angle -= action[2] * rotation_scale

        # Apply acceleration due to action
        rad = math.radians(self.agent.angle)
        self.agent.ax += action[0] * acceleration_scale * math.sin(rad)
        self.agent.ay += action[0] * acceleration_scale * math.cos(rad)

        # Apply external forces
        self.agent.ay += 1 # gravity

        # Calcualte new velocity of agent
        self.agent.dx += self.agent.ax
        self.agent.dy += self.agent.ay

        # Calculate new position of agent
        self.agent.x += self.agent.dx
        self.agent.y += self.agent.dy

        # If agent has passed screen boundaries, exit
        if self.agent.y > self.window_height or \
        self.agent.x < 0 or self.agent.x > self.window_width:
            self.running = False
        
        return None, None
    
    def render(self):
        ''' Render the environment to screen 
        
            Paramters:
                none
            
            Returns:
                none
        '''
        self.window.fill((169, 197, 231))
        image = pygame.transform.rotate(self.agent.image, self.agent.angle)
        self.window.blit(image, (self.agent.x, self.agent.y))
        pygame.display.update()