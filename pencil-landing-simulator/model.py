from keras.models import Sequential
from keras.layers import Input, Dense, Activation
from keras.optimizers import Adam


class SimpleModel:
    ''' SimpleModel
    
        This is the simple model class which is a single hidden layer neural network.
    '''

    def __init__(self, env):
        ''' Initialise the model 
        
            Parameters:
                env: A gym environment
            
            Returns:
                none
        '''
        self.model = Sequential()
        self.model.add(Dense(16, input_shape=(env.observation_space.n,)))
        self.model.add(Activation('relu'))
        self.model.add(Dense(env.action_space.n))
        self.model.add(Activation('linear'))

        print(self.model.summary())
