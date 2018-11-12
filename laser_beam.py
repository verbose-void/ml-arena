import math
import pawn
import arcade

SPEED = 5
LENGTH = 20
WIDTH = 3


class LaserBeam:
    def __init__(self, pos, direction):
        self.dir = direction
        self.pos = pos

    def update(self):
        self.pos[0] += math.cos(self.dir) * SPEED
        self.pos[1] += math.sin(self.dir) * SPEED

        if self.pos[0] > pawn.SCREEN_WIDTH or self.pos[0] < 0:
            return False

        if self.pos[1] > pawn.SCREEN_HEIGHT or self.pos[1] < 0:
            return False

    def draw(self):
        endX = self.pos[0] + math.cos(self.dir) * LENGTH
        endY = self.pos[1] + math.sin(self.dir) * LENGTH

        arcade.draw_line(self.pos[0], self.pos[1],
                         endX, endY, arcade.color.RED, WIDTH)
