import math
import arcade

SPEED = 25
LENGTH = 20
WIDTH = 3
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600


class LaserBeam:
    def __init__(self, pos, direction, life_span, damage):
        self.dir = direction
        self.start_pos = [pos[0], pos[1]]
        self.pos = pos
        self.life_span_squared = math.pow(life_span, 2)
        self.killed = None
        self.end_of_life = False
        self.damage = damage

    def get_damage(self):
        return self.damage

    def kill(self, pawn):
        self.killed = pawn
        self.end_of_life = True

    def who_was_killed(self):
        return self.killed

    def update(self):
        if self.killed != None or self.end_of_life:
            return False

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
        hp = self.get_head_position()

        arcade.draw_line(self.pos[0], self.pos[1],
                         hp[0], hp[1], arcade.color.RED, WIDTH)

    def get_head_position(self):
        return (self.pos[0] + math.cos(self.dir) * LENGTH, self.pos[1] + math.sin(self.dir) * LENGTH)
