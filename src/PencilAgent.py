import os
import cv2


class Pencil:
    """
    
    """

    def __init__(self, name, x_max, x_min, y_max, y_min, icon_path):
        self.name = name
        self.x = 0
        self.y = 0
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.width = 16
        self.height = 128
        self.icon = cv2.imread(icon_path, 1)
        # self.icon = cv2.resize(self.icon, (self.height, self.width))

    def clamp(self, n, minn, maxn):
        return max(min(maxn, n), minn)

    def get_position(self):
        return (self.x, self.y)

    def set_position(self, x, y):
        self.x = self.clamp(x, self.x_min, self.x_max - self.width)
        self.y = self.clamp(y, self.y_min, self.y_max - self.height)
    
    def move(self, del_x, del_y):
        self.x += del_x
        self.y += del_y
        
        self.x = self.clamp(self.x, self.x_min, self.x_max - self.width)
        self.y = self.clamp(self.y, self.y_min, self.y_max - self.height)

