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
        gravity: float = 0.98,
        width: int = 1600,
        height: int = 900):
        super().__init__(agent, entities, width, height)
        self._gravity = gravity
    
    def reset(self):
        self.running = True
        return self.state()
    
    def state(self):
        return [0, 0, 0, 0]
    
    def step(self, action):
        y_force = self._gravity * self._force_scale
        y_acceleration = y_force / self._agent.mass
        
        self._agent.velocity = (
            self._agent.velocity[0],
            self._agent.velocity[1] + y_acceleration
        )

        self._agent.position = (
            self._agent.position[0],
            self._agent.position[1] + self._agent.velocity[1]
        )

        super().step(action)
