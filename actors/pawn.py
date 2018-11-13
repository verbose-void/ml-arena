import arcade
import math
import time
from actors import laser_beam

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

HEALTH_BAR_HEIGHT = 20
HEALTH_BAR_MAX_WIDTH = 60

HALF_PI = math.pi / 2


class Pawn:
    def __init__(self, x, y, mcontrols=None, dcontrols=None, acontrol=None):
        # Graphical data initialization
        self.radius = 20
        self.radius_squared = self.radius * self.radius
        self.minor_radius = self.radius * 0.5
        self.mod_radius = self.radius * 0.464

        # Base-Stats
        self.speed = 120
        self.look_speed = 2
        self.max_health = 100
        self.laser_life = 600
        self.laser_damage = 10
        self.laser_speed = 700
        self.laser_cooldown = 0.1  # measured in seconds

        # Meta initialization
        self.pos = [x, y]
        self.vel = [0, 0]
        self.dir = 0  # radians
        self.health = -100
        self.rotation = None
        self.__last_laser__ = time.time()

        # Manual control override initialization
        self.mcontrols = mcontrols
        self.dcontrols = dcontrols
        self.acontrol = acontrol

        self.lasers = []

    def move(self, x, y):
        """
        Starts movement in the axis changed. Values are normalized to -1, 0, & 1.
        """

        if x != None:
            self.vel[0] = 0 if x == 0 else 1 if x > 0 else -1
        if y != None:
            self.vel[1] = 0 if y == 0 else 1 if y > 0 else -1

    def laser_on_cooldown(self):
        """
        Checks weather laser usage is on cooldown according to the 'laser_cooldown' field variable.
        """

        return self.__last_laser__ + self.laser_cooldown >= time.time()

    def get_lasers(self):
        """
        @return Returns all lasers shot by the current pawn.
        """

        return self.lasers

    def look(self, direction):
        """
        Starts rotation towards 'right' (clockwise) or 'left' (counter-clockwise)
        @param direction must be of value 'right', 'left', or None. Otherwise, it will be converted to None.
        """

        self.rotation = "right" if direction == "right" else "left" if direction == "left" else None

    def draw_health_bar(self):
        """
        Displays the pawns health above it's graphical representation.
        Length is set in the global variable 'HEALTH_BAR_WIDTH'.
        Height above it's body is set in the global variable 'HEALTH_BAR_HEIGHT'.
        """

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
        """
        Creates the graphical representation for the pawn using a triangle & circle.
        Sizing is relative to the radius field variable.
        """

        # Draw body circle
        arcade.draw_circle_filled(
            self.pos[0], self.pos[1], self.mod_radius, arcade.color.WHITE)

        # Get triangle verticies relative to the rotation stored in the field variable 'direction'.
        facing = (math.cos(self.dir) * self.radius,
                  math.sin(self.dir) * self.radius)

        temp = self.dir+HALF_PI
        leftLeg = (math.cos(temp) * self.minor_radius,
                   math.sin(temp) * self.minor_radius)

        temp = self.dir-HALF_PI
        rightLeg = (math.cos(temp) * self.minor_radius,
                    math.sin(temp) * self.minor_radius)

        # Draw triangle according to the determined verticies.
        arcade.draw_triangle_filled(self.pos[0]+facing[0], self.pos[1]+facing[1],
                                    self.pos[0] +
                                    leftLeg[0], self.pos[1]+leftLeg[1],
                                    self.pos[0] +
                                    rightLeg[0], self.pos[1]+rightLeg[1],
                                    arcade.color.WHITE)

        self.draw_health_bar()

    def press(self, key):
        """
        Called when a key is pressed, this method executes the action assigned to a given key
        in the manual control overrides.
        """

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
        """
        Checks if the pawn is on laser cooldown, if not it dispatches a laser from the origin of the
        graphical representation.
        """

        if self.laser_on_cooldown():
            return

        self.lasers.append(laser_beam.LaserBeam(
            [self.pos[0], self.pos[1]], self.dir, self.laser_life, self.laser_damage, self.laser_speed))

        self.__last_laser__ = time.time()

    def draw_lasers(self):
        """
        Draws all of the lasers shot by this pawn.
        """

        for laser in self.lasers:
            laser.draw()

    def update_lasers(self, delta_time):
        """
        Updates each individual laser this pawn is responsible for.
        @return Returns a list of all pawns that were killed by lasers.
        """

        keep = []
        pawns_killed = set()

        for laser in self.lasers:
            if laser.update(delta_time) != False:
                keep.append(laser)
            elif laser.who_was_killed() != None:
                pawns_killed.add(laser.who_was_killed())

        self.lasers = keep
        return pawns_killed

    def release(self, key):
        """
        Called when the given key is released. Undoes actions controlled 
        by the manual control overrides.
        """

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

    def rotate(self, delta_time):
        """
        Executes graphical rotation for the given pawn according to the 'look_speed'
        field variable.
        """

        if self.rotation == "right":
            # Look to right
            self.dir -= self.look_speed * delta_time  # radians
        elif self.rotation == "left":
            # Look to left
            self.dir += self.look_speed * delta_time  # radians

        self.dir = self.dir % (2 * math.pi)

    def update(self, lasers, delta_time):
        """
        Called every update round: handles updates for lasers & pawn position / rotation.
        """

        if self.health <= -100:
            self.health = self.max_health

        # Check for laser collisions
        for l in lasers:
            if self.colliding_with(l):
                self.health -= l.get_damage()
                if self.health <= 0.1:
                    l.kill(self)
                else:
                    l.kill(None)

        self.rotate(delta_time)
        self.pos[0] += (self.vel[0] * self.speed) * delta_time
        self.pos[1] += (self.vel[1] * self.speed) * delta_time

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
        """
        Collision detection between the calling pawn & the given laser.
        """

        lhp = laser.get_head_position()

        dist_squared = math.pow(
            self.pos[0]-lhp[0], 2) + math.pow(self.pos[1]-lhp[1], 2)

        return dist_squared < self.radius_squared
