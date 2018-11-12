import math
import arcade

SPEED = 25
LENGTH = 20
WIDTH = 3
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600


class LaserBeam:
    def __init__(self, pos, direction, life_span):
        self.dir = direction
        self.start_pos = [pos[0], pos[1]]
        self.pos = pos
        self.life_span_squared = math.pow(life_span, 2)

    def update(self):
        self.pos[0] += math.cos(self.dir) * SPEED
        self.pos[1] += math.sin(self.dir) * SPEED

        dist_squared = math.pow(
            self.start_pos[0]-self.pos[0], 2) + math.pow(self.start_pos[1]-self.pos[1], 2)

        if dist_squared > self.life_span_squared:
            return False

        if self.pos[0] > SCREEN_WIDTH or self.pos[0] < 0:
            return False

        if self.pos[1] > SCREEN_HEIGHT or self.pos[1] < 0:
            return False

    def draw(self):
        endX = self.pos[0] + math.cos(self.dir) * LENGTH
        endY = self.pos[1] + math.sin(self.dir) * LENGTH

        arcade.draw_line(self.pos[0], self.pos[1],
                         endX, endY, arcade.color.RED, WIDTH)
