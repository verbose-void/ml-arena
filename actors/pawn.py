import arcade
import math

HALF_PI = math.pi / 2


class Pawn:
    def __init__(self, x, y, mcontrols=None, dcontrols=None):
        self.radius = 20
        self.minor_radius = self.radius * 0.5
        self.mod_radius = self.radius * 0.464

        self.pos = [x, y]
        self.vel = [0, 0]
        self.dir = 0  # radians
        self.rotation = None

        self.mcontrols = mcontrols
        self.dcontrols = dcontrols

        self.speed = 2

    def move(self, x, y):
        if x != None:
            self.vel[0] = 0 if x == 0 else 1 if x > 0 else -1
        if y != None:
            self.vel[1] = 0 if y == 0 else 1 if y > 0 else -1

    def look(self, direction):
        self.rotation = "right" if direction == "right" else "left" if direction == "left" else None

    def draw(self):
        arcade.draw_circle_filled(
            self.pos[0], self.pos[1], self.mod_radius, arcade.color.WHITE)

        # Draw directional arrow
        facing = (math.cos(self.dir) * self.radius,
                  math.sin(self.dir) * self.radius)

        temp = self.dir+HALF_PI
        leftLeg = (math.cos(temp) * self.minor_radius,
                   math.sin(temp) * self.minor_radius)

        temp = self.dir-HALF_PI
        rightLeg = (math.cos(temp) * self.minor_radius,
                    math.sin(temp) * self.minor_radius)

        arcade.draw_triangle_filled(self.pos[0]+facing[0], self.pos[1]+facing[1],
                                    self.pos[0] +
                                    leftLeg[0], self.pos[1]+leftLeg[1],
                                    self.pos[0] +
                                    rightLeg[0], self.pos[1]+rightLeg[1],
                                    arcade.color.WHITE)

    def press(self, key):
        if self.mcontrols == None:
            return

        if key in self.mcontrols:
            i = self.mcontrols.index(key)
            if i != -1:
                if i == 0:
                    # left
                    self.move(-1, None)
                elif i == 1:
                    # up
                    self.move(None, 1)
                elif i == 2:
                    # right
                    self.move(1, None)
                elif i == 3:
                    # down
                    self.move(None, -1)

                return

        if self.dcontrols == None:
            return

        if key in self.dcontrols:
            i = self.dcontrols.index(key)
            if i == 0:
                self.rotation = "left"
            elif i == 1:
                self.rotation = "right"

    def release(self, key):
        if self.mcontrols == None:
            return

        # Reset corresponding velocity
        if key in self.mcontrols:
            i = self.mcontrols.index(key)
            if i != -1:
                if i == 0 or i == 2:
                    # left
                    self.vel[0] = 0
                elif i == 1 or i == 3:
                    # up
                    self.vel[1] = 0

        if self.dcontrols == None:
            return

        if key in self.dcontrols:
            i = self.dcontrols.index(key)
            if i == 0 or i == 1:
                self.rotation = None

    def rotate(self):
        if self.rotation == "right":
            # Look to right
            self.dir -= 0.05  # radians
        elif self.rotation == "left":
            # Look to left
            self.dir += 0.05  # radians

        self.dir = self.dir % (2 * math.pi)

    def update(self):
        self.rotate()
        self.pos[0] += (self.vel[0] * self.speed)
        self.pos[1] += (self.vel[1] * self.speed)
