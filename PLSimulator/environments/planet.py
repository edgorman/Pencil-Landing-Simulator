from pygame import Vector2

from PLSimulator.environments.space import SpaceEnvironment


class PlanetEnvironment(SpaceEnvironment):
    '''
        PlanetEnvironment

        This environment models an environment with gravity on a planet
    '''

    def __init__(
        self,
        entities: list = [],
        gravity: float = 1,
        density: float = 1,
        width: int = 1280,
        height: int = 720,
        bg_colour: tuple = (0, 0, 0)):
        super().__init__(entities, width, height, bg_colour)

        self._gravity = gravity
        self._density = density
    
    def reset(self):
        self.running = True
        return self.state()
    
    def state(self):
        return [0, 0, 0, 0]
    
    def step(self, action):
        # Move agent under gravity
        gravity = self._force_scale * Vector2(0, self._gravity)

        # Move agent under drag: Fd = 0.5 * Cd * A * p * V^2
        drag = 0.5 * 0.82 * 1 * self._density * Vector2(self._pencil.velocity[0]**2, self._pencil.velocity[1]**2)
        drag = self._force_scale * self._pencil.velocity.rotate(180)

        # Move agent under parents forces/actions
        self._pencil.update_position(gravity + drag)
        _, _, _, _ = super().step(action)

        return self.state(), 0, False, {}


class EarthEnvironment(PlanetEnvironment):
    '''
        EarthEnvironment

        This environment models an Earth environment
    '''

    def __init__(
        self, 
        entities: list = [], 
        width: int = 1280, 
        height: int = 720):
        super().__init__(entities, 9.8, 1, width, height, (137, 207, 240))
    

class MarsEnvironment(PlanetEnvironment):
    '''
        MarsEnvironment

        This environment models a Mars environment
    '''

    def __init__(
        self, 
        entities: list = [], 
        width: int = 1280, 
        height: int = 720):
        super().__init__(entities, 4.9, 0.1, width, height, (110, 38, 14))


class MoonEnvironment(PlanetEnvironment):
    '''
        MoonEnvironment

        This environment models a Moon environment
    '''

    def __init__(
        self, 
        entities: list = [], 
        width: int = 1280, 
        height: int = 720):
        super().__init__(entities, 0.6, 0, width, height, (169, 169, 169))
