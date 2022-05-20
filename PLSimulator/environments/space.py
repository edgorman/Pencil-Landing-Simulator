import math
import pygame

from PLSimulator.agents.agent import BaseAgent
from PLSimulator.environments.environment import BaseEnvironment


class SpaceEnvironment(BaseEnvironment):
    '''
        SpaceEnvironment

        This environment models an environment with no objects or gravity
    '''

    def __init__(
        self,
        agent: BaseAgent,
        entities: list = [],
        width: int = 1600,
        height: int = 900):
        super().__init__(agent, entities, width, height)
    
    def reset(self):
        self.running = True
        return self.state()
    
    def state(self):
        return [0, 0, 0, 0]
    
    def step(self, action):
        thrust = action[0] * -self._acc_force_scale
        left = action[1] * -self._rot_force_scale
        right = action[2] * self._rot_force_scale
        
        # Process angular data
        ang_acceleration = left + right
        self._agent.angle += ang_acceleration

        thrust = (
            thrust * math.sin(math.radians(self._agent.angle)),
            thrust * math.cos(math.radians(self._agent.angle))
        )

        # Process positional data
        pos_acceleration = (
            thrust[0] / self._agent.mass,
            thrust[1] / self._agent.mass
        )
        self._agent.velocity = (
            self._agent.velocity[0] + pos_acceleration[0],
            self._agent.velocity[1] + pos_acceleration[1]
        )
        self._agent.position = (
            self._agent.position[0] + self._agent.velocity[0],
            self._agent.position[1] + self._agent.velocity[1]
        )

        return self.state(), 0, False, {}
    
    def render(self):
        self.window.fill((0, 0, 0))
        
        rotated_image = pygame.transform.rotate(self._agent.image, self._agent.angle)
        new_rect = rotated_image.get_rect(center = self._agent.image.get_rect(topleft = self._agent.position).center)
        self.window.blit(rotated_image, new_rect.topleft)
        
        pygame.display.update()
