import arcade
import math
import time
from actors import laser_beam

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

HEALTH_BAR_HEIGHT = 20
HEALTH_BAR_MAX_WIDTH = 60

HALF_PI = math.pi / 2

RAY_TRACES = True


class Pawn:
    def __init__(self, brain, x, y, direc=0, mcontrols=None, dcontrols=None, acontrols=None):
        """
        The default pawn type.
        @param brain The brain is the artificial controller for the pawn.
        @param x, y Starting position.
        @param mcontrols A list of movement controls containing arcade.keys for LEFT, UP, RIGHT, & DOWN respectively.
        @param dcontrols A list of diretional movement controls containing arcade.keys for CLOCKWISE & COUNTER-CLOCKWISE respectively.
        @param mcontrols An arcade.key that controls the dispatching of lasers (the Pawn.attack(...) method).
        """

        self.brain_constructor = brain

        if brain != None:
            self.brain = brain(self)
        else:
            self.brain = None

        # Graphical data initialization
        self.radius = 20
        self.radius_squared = self.radius * self.radius
        self.minor_radius = self.radius * 0.5
        self.mod_radius = self.radius * 0.464

        # Base-Stats
        self.speed = 120
        self.look_speed = 2
        self.max_health = 500
        self.laser_life = 600
        self.laser_damage = 10
        self.laser_speed = 700
        self.laser_cooldown = 0.1  # measured in seconds
        self.shield_count = 5  # amount of shield uses
        self.shield_durability = 5  # amount of hits the shield can take

        # Meta initialization
        self.pos = [x, y]
        self.start_pos = (x, y)
        self.vel = [0, 0]
        self.dir = direc  # radians
        self.starting_dir = direc
        self.health = -100
        self.rotation = None

        self.__last_laser__ = time.time()
        self.__shield_on__ = False
        self.__shield_dura__ = self.shield_durability

        # Manual control override initialization
        self.mcontrols = mcontrols
        self.dcontrols = dcontrols
        self.acontrols = acontrols

        self.last_shot = None
        self.lasers = []
        self.env = None

    def reset(self):
        """
        Returns a new instance of the same pawn with it's starting values.
        """

        out = Pawn(
            self.brain_constructor,
            self.start_pos[0],
            self.start_pos[1],
            self.starting_dir,
            self.mcontrols,
            self.dcontrols,
            self.acontrols
        )

        out.set_env(self.env)

        return out

    def get_laser_life(self):
        """
        @return Returns the pawn's laser's life-span.
        """

        return self.laser_life

    def use_shield(self):
        """
        Attempt to activate shield for this pawn.
        """

        if self.shield_count <= 0:
            return

        self.__shield_on__ = True
        self.shield_count -= 1

    def get_dir(self):
        """
        @return Returns the pawn's direction in radians.
        """

        return self.dir

    def get_speed(self):
        """
        @return Returns the speed of this pawn.
        """

        return self.speed

    def get_vel(self):
        """
        @return Returns this pawn's velocities (headings)
        """

        return self.vel

    def get_health(self):
        """
        @return Returns this pawn's health value.
        """

        return self.health

    def set_env(self, env):
        """
        Sets the environment containing this pawn.
        """

        self.env = env

    def get_pawns(self):
        """
        @return Returns all pawns in the environment that isn't itself.
        """

        return self.env.get_pawns(self)

    def get_pos(self):
        """
        @return Returns the pawns position.
        """

        return self.pos

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

        If the last shot was a long shot, cooldown is twice the time.
        Otherwise, if shot was a short shot, cooldown is half the time.
        """

        if self.last_shot == None:
            return self.__last_laser__ + 1 >= time.time()

        cool = self.laser_cooldown

        if self.last_shot == "long":
            cool = self.laser_cooldown * 4

        return self.__last_laser__ + cool >= time.time()

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

        color = arcade.color.WHITE

        if self.__shield_on__:
            color = arcade.color.BLUE

        # Get triangle verticies relative to the rotation stored in the field variable 'direction'.
        facing = (math.cos(self.dir) * self.radius,
                  math.sin(self.dir) * self.radius)

        temp = self.dir+HALF_PI
        leftLeg = (math.cos(temp) * self.minor_radius,
                   math.sin(temp) * self.minor_radius)

        temp = self.dir-HALF_PI
        rightLeg = (math.cos(temp) * self.minor_radius,
                    math.sin(temp) * self.minor_radius)

        # Draw Ray Traces (Debugging)
        if RAY_TRACES:
            arcade.draw_line(self.pos[0], self.pos[1], facing[0]
                             * 1000, facing[1] * 1000, arcade.color.RED_DEVIL, 3)

        # Draw body circle
        arcade.draw_circle_filled(
            self.pos[0], self.pos[1], self.mod_radius, color)

        # Draw triangle according to the determined verticies.
        arcade.draw_triangle_filled(self.pos[0]+facing[0], self.pos[1]+facing[1],
                                    self.pos[0] +
                                    leftLeg[0], self.pos[1]+leftLeg[1],
                                    self.pos[0] +
                                    rightLeg[0], self.pos[1]+rightLeg[1],
                                    color)

        self.draw_health_bar()

    def press(self, key):
        """
        Called when a key is pressed, this method executes the action assigned to a given key
        in the manual control overrides.
        """

        if self.acontrols != None:
            if key in self.acontrols:
                i = self.acontrols.index(key)

                if i == 0:
                    self.attack("long")
                elif i == 1:
                    self.attack("short")
                elif i == 2:
                    self.use_shield()

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

    def get_long_range_dist(self):
        """
        Returns how far a long distance attack will travel.
        """

        return self.laser_life*2

    def get_short_range_dist(self):
        """
        Returns how far a short distance attack will travel.
        """

        return self.laser_life*0.4

    def has_active_shield(self):
        """
        @return Returns wether this pawn has it's shield active.
        """

        return self.__shield_on__

    def get_shield_count(self):
        """
        @return Returns how many shields this pawn has.
        """

        return self.shield_count

    def take_damage(self, amount):
        """
        Inflicts damage on this pawn.
        """

        hit = True

        if self.__shield_dura__ <= 0:
            self.__shield_on__ = False
            self.__shield_dura__ = self.shield_durability
        else:
            self.__shield_dura__ -= 1
            hit = False

        if hit:
            self.health -= amount

    def attack(self, t="long"):
        """
        Checks if the pawn is on laser cooldown, if not it dispatches a laser from the origin of the
        graphical representation.
        @param type Type of attack. Accepts 'long' & 'short'.
        """

        if self.laser_on_cooldown():
            return

        laser = None

        if t == "long":
            laser = laser_beam.LaserBeam(
                [self.pos[0], self.pos[1]],
                self.dir, self.get_long_range_dist(), self.laser_damage*2, self.laser_speed, arcade.color.RED)
        elif t == "short":
            laser = laser_beam.LaserBeam(
                [self.pos[0], self.pos[1]],
                self.dir, self.get_short_range_dist(), self.laser_damage*0.8, self.laser_speed*0.6, arcade.color.BLUE)

        self.lasers.append(laser)

        self.__last_laser__ = time.time()
        self.last_shot = t

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

    def get_rotation(self):
        """
        @return Returns the pawn's rotational heading.
        """

        return self.rotation

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

        # Artifical controller decision making process if a brain is contained.
        if self.brain != None:
            self.brain.on_tick()

        if self.health <= -100:
            self.health = self.max_health

        # Check for laser collisions
        for l in lasers:
            if self.colliding_with(l):
                self.take_damage(l.get_damage())
                if self.health <= 0:
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

        return self.dist_squared(lhp) < self.radius_squared

    def dist_squared(self, pos):
        """
        @param pos Tuple or array of the pos in the form [x,y].
        @return Returns the distance squared from this pawn to the given pos.
        """

        return math.pow(self.pos[0]-pos[0], 2) + math.pow(self.pos[1]-pos[1], 2)
