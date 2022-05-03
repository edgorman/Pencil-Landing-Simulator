import math

import numpy as np
import pygame

from .environment import BaseEnvironment


class GroundEnvironment(BaseEnvironment):
    ''' GroundEnvironment
    
        This environment models a simple static ground environment.
    '''

    def __init__(self, goal_pos=(800, 900), width=1600, height=900):
        super().__init__(goal_pos, width, height)

        self.gravity = 0.05
        self.max_speed = 10

    
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
        self.agent.x += min(self.agent.dx, self.max_speed)
        self.agent.y += min(self.agent.dy, self.max_speed)

        # If agent has passed screen boundaries, done
        if self.agent.y > self.window_height or self.agent.x < 0 or self.agent.x > self.window_width:
            self.running = False
        
        # Calculate reward for agent
        reward = math.sqrt(
            math.pow(self.goal_position[0] - self.agent.x, 2) + 
            math.pow(self.goal_position[1] - self.agent.y, 2)
        )

        return self.get_state(), reward, self.running, {}
    
    def render(self):
        self.window.fill((169, 197, 231))
        image = pygame.transform.rotate(self.agent.image, self.agent.an)
        self.window.blit(image, (self.agent.x, self.agent.y))
        pygame.display.update()