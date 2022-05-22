import math

from PLSimulator.agents.agent import BaseAgent
from PLSimulator.environments.space import SpaceEnvironment


class PlanetEnvironment(SpaceEnvironment):
    '''
        PlanetEnvironment

        This environment models an environment with gravity on a planet
    '''

    def __init__(
        self,
        agent: BaseAgent,
        entities: list = [],
        gravity: float = 1,
        density: float = 1,
        width: int = 1600,
        height: int = 900):
        super().__init__(agent, entities, width, height)

        self._gravity = gravity
        self._density = density
    
    def reset(self):
        self.running = True
        return self.state()
    
    def state(self):
        return [0, 0, 0, 0]
    
    def step(self, action):
        # Move agent under gravity
        gravity = (0, self._gravity * self._force_scale)
        self._agent.update_position(gravity)

        # Move agent under drag: Fd = 0.5 * Cd * A * p * V^2
        drag = (
            0.5 * 0.82 * 1 * self._density * self._agent.velocity[0]**2,
            0.5 * 0.47 * 1 * self._density * self._agent.velocity[1]**2
        )
        drag = (
            -math.copysign(drag[0], self._agent.velocity[0]) * self._force_scale,
            -math.copysign(drag[1], self._agent.velocity[1]) * self._force_scale,

        )
        self._agent.update_position(drag)

        # Move agent under parents forces/actions
        _, _, _, _ = super().step(action)

        return self.state(), 0, False, {}


class EarthEnvironment(PlanetEnvironment):
    '''
        EarthEnvironment

        This environment models an Earth environment
    '''

    def __init__(
        self, 
        agent: BaseAgent, 
        entities: list = [], 
        width: int = 1600, 
        height: int = 900):
        super().__init__(agent, entities, 0.98, 0.1, width, height)


class MarsEnvironment(PlanetEnvironment):
    '''
        MarsEnvironment

        This environment models an Mars environment
    '''

    def __init__(
        self, 
        agent: BaseAgent, 
        entities: list = [], 
        width: int = 1600, 
        height: int = 900):
        super().__init__(agent, entities, 0.49, 0.05, width, height)
