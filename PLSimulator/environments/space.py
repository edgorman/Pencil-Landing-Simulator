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
        height: int = 900,
        bg_colour: tuple = (0, 0, 0)):
        super().__init__(agent, entities, width, height, bg_colour)
    
    def reset(self):
        self.running = True
        return self.state()
    
    def state(self):
        return [0, 0, 0, 0]
    
    def step(self, action):
        # Convert agent actions into forces
        thrust = -action[0] * 15 * self._force_scale
        left = -action[1] * 15 * self._rotation_scale
        right = action[2] * 15 * self._rotation_scale

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
