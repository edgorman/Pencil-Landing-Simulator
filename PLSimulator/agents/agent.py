import os
from abc import abstractmethod
from pygame import Vector2

from PLSimulator.entities.entity import BaseEntity
from PLSimulator.test import MODEL_DATA_DIRECTORY


class BaseAgent(BaseEntity):
    '''
        BaseAgent

        This is the agent class from which all other agents will inherit.
    '''

    def __init__(
        self,
        asset_name: str = 'pencil.png',
        position: Vector2 = Vector2(0, 0),
        velocity: Vector2 = Vector2(0, 0),
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
        entities = [
            BaseEntity('engine firing.png', Vector2(16, 80), Vector2(0, 84), Vector2(0, 0), 0, 0, [], False),
            BaseEntity('rcs firing.png', Vector2(16, 16), Vector2(14, 53), Vector2(0, 0), 180, 0, [], False),
            BaseEntity('rcs firing.png', Vector2(16, 16), Vector2(14, -53), Vector2(0, 0), 0, 0, [], False),
        ]
        super().__init__(asset_name, Vector2(16, 128), position, velocity, angle, mass, entities, True)
        
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
        position: Vector2 = Vector2(0, 0),
        velocity: Vector2 = Vector2(0, 0),
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
    def train(self) -> dict:
        '''
            Train the model from in the environment

            Parameters:
                None

            Returns
                Result: Metrics from training
        '''
    
    @abstractmethod
    def step(self, state: list) -> list:
        '''
            Get the action of the agent given an environment state

            Parameters:
                state: State of the environment

            Returns
                action: Action of the agent in environment
        '''

    @abstractmethod
    def save(self) -> None:
        '''
            Save the model to a local folder

            Parameters:
                None

            Returns
                None
        '''
    
    @abstractmethod
    def load(self) -> None:
        '''
            Load the model from a saved file

            Parameters:
                None

            Returns
                None
        '''

        
    def clear(self, sub_dir: str = '') -> None:
        '''
            Clear the saved model parameters from local folder

            Parameters:
                sub_dir: Current sub directory

            Returns
                None
        '''
        dir = os.path.join(MODEL_DATA_DIRECTORY, sub_dir)
        for f in os.listdir(dir):
            a = os.path.join(dir, f)
            self.clear(a) if os.path.isdir(a) else os.remove(a)
