import arcade
import random
from typing import List
from test.path_environment import *


class Goal:
    radius = 10
    pos: list

    def __init__(self, x: float = None, y: float = None):
        if x == None or y == None:
            pos = [0, 0]
        else:
            self.pos = [x, y]

    def on_draw(self):
        arcade.draw_circle_filled(
            self.pos[0], self.pos[1], self.radius, arcade.color.GREEN)

    def randomize(self, _max: float, _min: float):
        self.pos = [
            random.random() * _max,
            random.random() * _min
        ]
