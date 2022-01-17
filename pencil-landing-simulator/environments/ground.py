import math

import numpy as np
import pygame

from .environment import BaseEnvironment


class GroundEnvironment(BaseEnvironment):
    ''' GroundEnvironment
    
        This environment models a simple static ground environment.
    '''

    def __init__(self, agent, width=1600, height=900):
        super().__init__(agent, width, height)

        self.gravity = 0.05
    
    def get_state(self):
        relDistance = self.window_height - self.agent.y
        velocityX = self.agent.dx
        velocityY = self.agent.dy
        relAngle = math.radians(0) - math.radians(self.agent.an)

        return [relDistance, velocityX, velocityY, relAngle]
    
    def step(self, action):
        rotation_scale = 0.15
        acceleration_scale = 0.15

        # Apply rotation due to action
        self.agent.an += action[1] * rotation_scale
        self.agent.an -= action[2] * rotation_scale

        # Apply acceleration due to action
        rad = math.radians(self.agent.an)
        self.agent.ax -= action[0] * acceleration_scale * math.sin(rad)
        self.agent.ay -= action[0] * acceleration_scale * math.cos(rad)

        # Apply external forces
        self.agent.ay += self.gravity

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
        
        # Calculate reward for agent
        reward = 100 - np.prod(self.get_state())

        return self.get_state(), reward, self.running, {}
    
    def render(self):
        self.window.fill((169, 197, 231))
        image = pygame.transform.rotate(self.agent.image, self.agent.an)
        self.window.blit(image, (self.agent.x, self.agent.y))
        pygame.display.update()