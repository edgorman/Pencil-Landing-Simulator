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
        self._keep_files = ['.gitkeep']

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
            if f in self._keep_files:
                continue
            
            a = os.path.join(dir, f)
            self.clear(a) if os.path.isdir(a) else os.remove(a)
