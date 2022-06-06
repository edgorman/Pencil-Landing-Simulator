import math
from pygame import Vector2

from PLSimulator.environments.environment import BaseEnvironment


class SpaceEnvironment(BaseEnvironment):
    '''
        SpaceEnvironment

        This environment models an environment with no objects or gravity
    '''

    def __init__(
        self,
        entities: list = [],
        width: int = 1280,
        height: int = 720,
        bg_colour: tuple = (0, 0, 0)):
        super().__init__(entities, width, height, bg_colour)
    
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
        if self._fuel <= 0:
            thrust = 0
        
        # Remove fuel from agent if fired engine
        if abs(thrust) > 0:
            self._fuel -= 0.1
            self._pencil.mass = self._dry_mass + self._fuel
        
        # Move agent under it's own thrust
        heading = self._pencil.angle + left + right
        thrust = thrust * Vector2(math.sin(math.radians(heading)), math.cos(math.radians(heading)))
        self._pencil.update_position(thrust, heading)

        return self.state(), 0, False, {}
