import math

import numpy as np
import pygame

from .environment import BaseEnvironment


class GroundEnvironment(BaseEnvironment):
    ''' GroundEnvironment
    
        This environment models a simple static ground environment.
    '''

    def __init__(self, width=1600, height=900):
        super().__init__(width, height)
    
    def get_state(self, agent):
        relDistance = self.window_height - agent.y
        velocityX = agent.dx
        velocityY = agent.dy
        relAngle = math.radians(0) - math.radians(agent.an)

        return [relDistance, velocityX, velocityY, relAngle]
    
    def step(self, agent, action):
        rotation_scale = 0.15
        acceleration_scale = -1.05

        # Apply rotation due to action
        agent.an += action[1] * rotation_scale
        agent.an -= action[2] * rotation_scale

        # Apply acceleration due to action
        rad = math.radians(agent.an)
        agent.ax += action[0] * acceleration_scale * math.sin(rad)
        agent.ay += action[0] * acceleration_scale * math.cos(rad)

        # Apply external forces
        agent.ay += 0.9 # gravity

        # Calcualte new velocity of agent
        agent.dx += agent.ax
        agent.dy += agent.ay

        # Calculate new position of agent
        agent.x += agent.dx
        agent.y += agent.dy

        # If agent has passed screen boundaries, exit
        if agent.y > self.window_height or \
        agent.x < 0 or agent.x > self.window_width:
            self.running = False
        
        # Calculate reward for agent
        reward = 100 - np.prod(self.get_state(agent))

        return self.get_state(agent), reward, self.running, {}
    
    def render(self, agent):
        self.window.fill((169, 197, 231))
        image = pygame.transform.rotate(agent.image, agent.an)
        self.window.blit(image, (agent.x, agent.y))
        pygame.display.update()