from errno import EPERM
import os
import random
from abc import abstractmethod
from collections import deque

import pygame
import numpy as np
from keras.layers import Dense
from keras.optimizers import Adam
from keras.models import Sequential


class BaseAgent:
    ''' BaseAgent
    
        This is the agent class from which all other agents will inherit.
    '''

    def __init__(self, x=0, y=0, dx=0, dy=0, an=0):
        ''' Initialise the agent 
        
            Parameters:
                x: X position of agent (default is 0)
                y: Y position of agent (default is 0)
                dx: X velocity of agent (default is 0)
                dy: Y velocity of agent (default is 0)
                an: Angle of agent (default is 0)
            
            Returns:
                none
        '''
        # Set up default parameters
        self.load_model = False
        self.state_size = 4
        self.action_size = 3

        # Set up positional parameters
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.an = an
        self.ax = 0
        self.ay = 1

        # Set up view in pygame
        image_path = os.path.join(os.getcwd(), 'pencil-landing-simulator', 'assets', 'pencil.png')
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (16, 128))
    
    @abstractmethod
    def get_action(self, state):
        ''' Get the action of the agent given an environment state
        
            Parameters:
                state: State of the environment
            
            Returns
                action: Action of the agent in environment
        '''
        ...
    
    @abstractmethod
    def train_batch(self):
        ''' Trains the agent in a batch (method is called my 'train')
        
            Paremeters:
                none
            
            Returns:
                none
        '''
    
    @abstractmethod
    def train(self, environment, render=False):
        ''' Trains the agent and stores the result in self.model
        
            Paremeters:
                environment: Environment to train agent in
                render: Whether to render the training (default is False)
            
            Returns:
                none
        '''
    
class DQNAgent(BaseAgent):
    ''' DQNAgent
    
        Trains a nerual network to learn in an environment
    '''

    def __init__(self, x=0, y=0, dx=0, dy=0, an=0):
        ''' Initialise the DQNAgent
        
            Parameters:
                x: X position of agent (default is 0)
                y: Y position of agent (default is 0)
                dx: X velocity of agent (default is 0)
                dy: Y velocity of agent (default is 0)
                an: Angle of agent (default is 0)
            
            Returns:
                none
        '''
        super().__init__(x, y, dx, dy, an)

        # These are hyper parameters for the DQN
        self.discount_factor = 0.99
        self.learning_rate = 0.001
        self.epsilon = 1.0
        self.epsilon_decay = 0.999
        self.epsilon_min = 0.01
        self.batch_size = 64
        self.train_start = 1000
        self.episodes = 100

        # Memory stored in deque
        self.memory = deque(maxlen=2000)

        # Initialise main and target model
        self.model = self.build_model()
        self.target_model = self.build_model()

        # Load an existing model
        if self.load_model:
            self.model.load_weights("./models/pencil-dqnagent.h5")
        self.update_target_model()
    
    def build_model(self):
        ''' Builds the neural network model
        
            Parameters:
                none
            
            Returns:
                model: Neural network
        '''
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu', kernel_initializer='he_uniform'))
        model.add(Dense(24, activation='relu', kernel_initializer='he_uniform'))
        model.add(Dense(self.action_size, activation='linear', kernel_initializer='he_uniform'))
        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
        return model
    
    def update_target_model(self):
        ''' Updates the weights of the target model with current model
        
            Parameters:
                none
            
            Returns:
                none
        '''
        self.target_model.set_weights(self.model.get_weights())
    
    def update_memory(self, state, action, reward, next_state, done):
        ''' Saves the state and resultant environment parameters once action was complete
        
            Parameters:
                state: State of the environment
                action: Action of the agent given the state
                reward: Reward received by agent's action in environment
                next_state: Following environment state from action
                done: Whether action caused environment to finish
            
            Returns:
                none
        '''
        self.memory.append((state, action, reward, next_state, done))

        # Over time epsilon should decay to reduce exploration of agent in state space
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
    
    def get_action(self, state):
        action = []

        # If model should choose random action
        if np.random.rand() <= self.epsilon:
            action = [
                random.uniform(0, 1),
                random.uniform(0, 1),
                random.uniform(0, 1)
            ]
        # Else model should choose best known action
        else:
            q_value = self.model.predict(np.reshape(state, [1, self.state_size]))
            action =  q_value[0]
        
        return action

    def train_batch(self):
        # Randomly sample memory to get training batch
        if len(self.memory) < self.train_start:
            return
        batch_size = min(self.batch_size, len(self.memory))
        mini_batch = random.sample(self.memory, batch_size)

        # Store input and state after each agent action
        update_input = np.zeros((batch_size, self.state_size))
        update_target = np.zeros((batch_size, self.state_size))
        action, reward, done = [], [], []

        # Iterate over training batch and store actions, rewards and completeness
        for i in range(self.batch_size):
            update_input[i] = mini_batch[i][0]
            action.append(mini_batch[i][1])
            reward.append(mini_batch[i][2])
            update_target[i] = mini_batch[i][3]
            done.append(mini_batch[i][4])

        # Get model and target model predictions on training batch
        target = self.model.predict(update_input)
        target_val = self.target_model.predict(update_target)

        # Iterate over training batch and aggregate rewards for actions
        for i in range(self.batch_size):
            # If action resulted in the environment being done
            if done[i]:
                # TODO: Reward highly if in correct state
                target[i][action[i]] = reward[i]
            else:
                target[i][action[i]] = reward[i] + self.discount_factor * (np.amax(target_val[i]))

        # Finally fit the model
        self.model.fit(update_input, target, batch_size=self.batch_size, epochs=1, verbose=0)

    def train(self, environment, render=False):
        history = []

        # For each episode of training
        for index in range(self.episodes):
            done = False
            score = 0
            state = environment.reset(index)

            # Repeat until environment is done
            while not done:
                # If environment should be rendered
                # Warning: will slow down training significantly
                if render:
                    environment.render()
                
                # Get agent action and step in environment
                action = self.get_action(state)
                next_state, reward, done, info = environment.step(action)

                # Save sample to replay memory
                self.update_memory(state, action, reward, next_state, done)

                # Batch train the model
                self.train_batch()
                score += reward
                state = next_state

                # If environment is done
                if done:
                    # Update agent target model
                    self.update_target_model()

                    # Store score history
                    history.append(score)
        
        # Display history
        print(history)
