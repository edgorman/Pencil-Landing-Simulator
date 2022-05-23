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
        # Convert agent actions into forces
        thrust = -action[0] * 14 * self._force_scale
        left = -action[1] * 14 * self._rotation_scale
        right = action[2] * 14 * self._rotation_scale

        # Check if agent has enough fuel to fire engine
        if self._agent.fuel <= 0:
            thrust = 0
        
        # Move agent under it's own thrust
        heading = self._agent.angle + left + right
        thrust = (
            thrust * math.sin(math.radians(heading)),
            thrust * math.cos(math.radians(heading))
        )
        self._agent.update_position(thrust, heading)

        # Remove fuel from agent if fired engine
        if thrust != 0:
            self._agent.fuel -= 1

        return self.state(), 0, False, {}
    
    def render(self):
        self.window.fill((0, 0, 0))
        
        rotated_image = pygame.transform.rotate(self._agent.image, self._agent.angle)
        new_rect = rotated_image.get_rect(center = self._agent.image.get_rect(topleft = self._agent.position).center)
        self.window.blit(rotated_image, new_rect.topleft)

        pygame.display.update()
