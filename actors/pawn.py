import arcade
import math
from actors import laser_beam

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

HEALTH_BAR_HEIGHT = 20
HEALTH_BAR_MAX_WIDTH = 60

HALF_PI = math.pi / 2


class Pawn:
    def __init__(self, x, y, mcontrols=None, dcontrols=None, acontrol=None):
        self.radius = 20
        self.radius_squared = self.radius * self.radius
        self.minor_radius = self.radius * 0.5
        self.mod_radius = self.radius * 0.464

        self.health = -100
        self.laser_damage = 10
        self.max_health = 100

        self.pos = [x, y]
        self.vel = [0, 0]
        self.dir = 0  # radians
        self.rotation = None
        self.look_speed = 0.04

        self.mcontrols = mcontrols
        self.dcontrols = dcontrols
        self.acontrol = acontrol

        self.speed = 2
        self.laser_life = 600

        self.lasers = []

    def move(self, x, y):
        if x != None:
            self.vel[0] = 0 if x == 0 else 1 if x > 0 else -1
        if y != None:
            self.vel[1] = 0 if y == 0 else 1 if y > 0 else -1

    def get_lasers(self):
        return self.lasers

    def look(self, direction):
        self.rotation = "right" if direction == "right" else "left" if direction == "left" else None

    def draw_health_bar(self):
        x = self.pos[0] - HEALTH_BAR_MAX_WIDTH / 2
        y = self.pos[1] + self.mod_radius + HEALTH_BAR_HEIGHT

        normal_health = self.health / self.max_health

        color = arcade.color.GREEN

        if normal_health <= 0.2:
            color = arcade.color.RED
        elif normal_health <= 0.5:
            color = arcade.color.YELLOW
        elif normal_health <= 0.7:
            color = arcade.color.ORANGE

        arcade.draw_line(x, y, x + (HEALTH_BAR_MAX_WIDTH *
                                    normal_health), y, color, 5)

    def draw(self):
        # Draw body circle
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

        self.draw_health_bar()

    def press(self, key):
        if self.acontrol != None:
            if key == self.acontrol:
                self.attack()
                return

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

    def attack(self):
        self.lasers.append(laser_beam.LaserBeam(
            [self.pos[0], self.pos[1]], self.dir, self.laser_life, self.laser_damage))

    def draw_lasers(self):
        for laser in self.lasers:
            laser.draw()

    def update_lasers(self):
        keep = []
        pawns_killed = set()

        for laser in self.lasers:
            if laser.update() != False:
                keep.append(laser)
            elif laser.who_was_killed() != None:
                pawns_killed.add(laser.who_was_killed())

        self.lasers = keep
        return pawns_killed

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
            self.dir -= self.look_speed  # radians
        elif self.rotation == "left":
            # Look to left
            self.dir += self.look_speed  # radians

        self.dir = self.dir % (2 * math.pi)

    def update(self, lasers):
        if self.health <= -100:
            self.health = self.max_health

        # Check for laser collisions
        if isinstance(lasers, (list,)):
            for l in lasers:
                if self.colliding_with(l):
                    self.health -= l.get_damage()
                    if self.health <= 0.1:
                        l.kill(self)
                    else:
                        l.kill(None)

        self.rotate()
        self.pos[0] += (self.vel[0] * self.speed)
        self.pos[1] += (self.vel[1] * self.speed)

        temp = self.radius * 1.2

        # X wrapping
        if self.pos[0] < -temp:
            self.pos[0] = SCREEN_WIDTH + temp
        elif self.pos[0] > SCREEN_WIDTH + temp:
            self.pos[0] = -temp

        # Y wrapping
        if self.pos[1] < -temp:
            self.pos[1] = SCREEN_HEIGHT + temp
        elif self.pos[1] > SCREEN_HEIGHT + temp:
            self.pos[1] = -temp

    def colliding_with(self, laser):
        lhp = laser.get_head_position()

        dist_squared = math.pow(
            self.pos[0]-lhp[0], 2) + math.pow(self.pos[1]-lhp[1], 2)

        return dist_squared < self.radius_squared
