import os
import cv2
import gym
import numpy as np
from gym import Env, spaces

from PencilAgent import Pencil

font = cv2.FONT_HERSHEY_COMPLEX_SMALL

class SolidGround(Env):
    """
    
    """

    def __init__(self):
        super(SolidGround, self).__init__()

        # Define a 2-D observation space
        self.observation_shape = (600, 800, 3)
        self.observation_space = spaces.Box(low = np.zeros(self.observation_shape), 
                                            high = np.ones(self.observation_shape),
                                            dtype = np.float16)
    
        
        # Define an action space ranging from 0 to 4
        self.action_space = spaces.Discrete(6,)
                        
        # Create a canvas to render the environment images upon 
        self.canvas = np.ones(self.observation_shape) * 1
        
        # Define elements present inside the environment
        self.elements = []

        # Maximum fuel available to pencil
        self.max_fuel = 1000

        # Permissible area of helicper to be 
        self.y_min = int(self.observation_shape[0] * 0.1)
        self.x_min = 0
        self.y_max = int(self.observation_shape[0] * 0.9)
        self.x_max = self.observation_shape[1]

    def draw_elements_on_canvas(self):
        # Init the canvas 
        self.canvas = np.ones(self.observation_shape) * 1

        # Draw the pencil on canvas
        for elem in self.elements:
            x,y = int(elem.x), int(elem.y)
            w,h = int(elem.width), int(elem.height)
            self.canvas[y : y+h, x : x+w] = elem.icon

        text = 'Fuel Left: {} | Rewards: {}'.format(self.fuel_left, self.ep_return)

        # Put the info on canvas 
        self.canvas = cv2.putText(self.canvas, text, (10,20), font, 0.8, (0,0,0), 1, cv2.LINE_AA)

    def reset(self):
        # Reset the fuel consumed
        self.fuel_left = self.max_fuel

        # Reset the reward
        self.ep_return  = 0

        # Determine a place to intialise the pencil in
        x = self.observation_shape[0] * 0.5
        y = 256
        
        # Intialise the chopper
        self.pencil = Pencil("pencil", self.x_max, self.x_min, self.y_max, self.y_min, os.path.join(os.getcwd(), 'src', 'assets', 'pencil.png'))
        self.pencil.set_position(x,y)

        # Intialise the elements 
        self.elements = [self.pencil]

        # Reset the Canvas 
        self.canvas = np.ones(self.observation_shape) * 1

        # Draw elements on the canvas
        self.draw_elements_on_canvas()

        # return the observation
        return self.canvas 

    def render(self, mode = "human"):
        assert mode in ["human", "rgb_array"], "Invalid mode, must be either \"human\" or \"rgb_array\""
        if mode == "human":
            cv2.imshow("Game", self.canvas)
            cv2.waitKey(10)
        
        elif mode == "rgb_array":
            return self.canvas
    
    def close(self):
        cv2.destroyAllWindows()