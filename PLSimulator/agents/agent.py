from abc import abstractmethod

from PLSimulator.entities.entity import BaseEntity


class BaseAgent(BaseEntity):
    '''
        BaseAgent

        This is the agent class from which all other agents will inherit.
    '''

    def __init__(
        self,
        asset_name: str = 'pencil.png',
        position: tuple = (0, 0),
        velocity: tuple = (0, 0),
        angle: float = 0,
        mass: float = 10,
        fuel: float = 1000) -> None:
        '''
            Initialise the agent. For extra parameters see :func:`<PLSimulator.entities.entity.BaseEntity>`

            Parameters:
                fuel: Amount of fuel remaining

            Returns:
                None
        '''
        super().__init__(asset_name, (16, 128), position, velocity, angle, mass, True)
        
        # Set up extra parameters
        self.fuel = fuel
        self._max_fuel = 100

    @property
    def wet_mass(self) -> float:
        '''
            Return the mass of the agent in terms of fuel and dry mass

            Parameters:
                None

            Returns:
                mass: Mass of the agent
        '''
        return self.mass + self.fuel

    def reset(
        self,
        position: tuple = (0, 0),
        velocity: tuple = (0, 0),
        angle: float = 0,
        fuel: float = 100) -> None:
        '''
            Reset the agent to starting parameters

            Parameters:
                position: Current position of entity
                velocity: Current velocity of entity
                angle: Current angle of the entity
                fuel: Amount of fuel remaining

            Returns:
                None
        '''
        self.position = position
        self.velocity = velocity
        self.angle = angle
        self.fuel = fuel

    @abstractmethod
    def get_action(self, state: list) -> list:
        '''
            Get the action of the agent given an environment state

            Parameters:
                state: State of the environment

            Returns
                action: Action of the agent in environment
        '''
