import os
from abc import abstractmethod

from PLSimulator.constants import MODEL_DATA_DIRECTORY


class BaseAgent:
    '''
        BaseAgent

        This is the agent class from which all other agents will inherit.
    '''

    def __init__(self, model_name) -> None:
        '''
            Initialise the agent.

            Parameters:
                None

            Returns:
                None
        '''
        self._model_dir = os.path.join(MODEL_DATA_DIRECTORY, model_name)
        if not os.path.exists(self._model_dir):
            os.makedirs(self._model_dir)

    @abstractmethod
    def reset(self) -> None:
        '''
            Reset the agent to starting conditions

            Parameters:
                None

            Returns:
                None
        '''

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

    def clear(self, dir: str = '') -> None:
        '''
            Clear the saved model from local storage

            Parameters:
                None

            Returns
                None
        '''
        path = os.path.join(MODEL_DATA_DIRECTORY, dir)
        for f in os.listdir(path):
            a = os.path.join(path, f)
            if os.path.isdir(a):
                self.clear(a)
                os.removedirs(a)
            else:
                os.remove(a)
