import arcade
import math
import time
from actors import laser_beam
import stat_biases

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

HEALTH_BAR_HEIGHT = 20
HEALTH_BAR_MAX_WIDTH = 60

HALF_PI = math.pi / 2

RAY_TRACES = False


class Pawn:
    def __init__(self, brain, x, y, direc=0, mcontrols=None, dcontrols=None, acontrols=None, match_index=-1, bias=None):
        """
        The default pawn type.

        Args:
            brain: The brain is the artificial controller for the pawn.
            x, y: Starting position.
            mcontrols: A list of movement controls containing arcade.keys for LEFT, UP, RIGHT, & DOWN respectively.
            dcontrols: A list of diretional movement controls containing arcade.keys for CLOCKWISE & COUNTER-CLOCKWISE respectively.
            mcontrols: An arcade.key that controls the dispatching of lasers (the Pawn.attack(...) method).
        """

        if brain != None:
            if type(brain) is type:
                self.brain_constructor = brain
                self.brain = brain(self)
            else:
                self.brain = brain
                self.brain.pawn = self
                self.brain_constructor = None
        else:
            self.brain = None
            self.brain_constructor = None

        # Graphical data initialization
        self.radius = 20
        self.radius_squared = self.radius * self.radius
        self.minor_radius = self.radius * 0.5
        self.mod_radius = self.radius * 0.464

        # Base-Stats
        self.speed = 120
        self.look_speed = 2
        self.max_health = 200
        self.short_laser_life = 300
        self.long_laser_life = 600
        self.long_laser_damage = 15
        self.short_laser_damage = 8
        self.long_laser_speed = 700
        self.short_laser_speed = 500
        self.laser_cooldown = 0.1  # measured in seconds
        self.max_shield_count = 5
        self.shield_count = self.max_shield_count  # amount of shield uses
        self.shield_durability = 5  # amount of hits the shield can take

        # Bias Stats
        if bias != None:
            self.bias = bias
        else:
            self.bias = stat_biases.Normal()

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
        self.__long_held__ = False
        self.__short_held__ = False

        # Manual control override initialization
        self.mcontrols = mcontrols
        self.dcontrols = dcontrols
        self.acontrols = acontrols

        # Fitness variables
        self.frames_alive = 1
        self.laser_hits = 0
        self.lasers_shot = 1
        self.laser_hits_taken = 1
        self.won = False
        self.is_dead = False

        self.last_shot = None
        self.lasers = []
        self.env = None

        self.match_index = match_index

    def reset(self):
        """
        Returns a new instance of the same pawn with it's starting values.
        """

        out = Pawn(
            self.brain_constructor if self.brain_constructor != None else self.brain,
            self.start_pos[0],
            self.start_pos[1],
            self.starting_dir,
            self.mcontrols,
            self.dcontrols,
            self.acontrols,
            self.match_index,
            self.bias
        )

        out.env = self.env

        return out

    def calculate_fitness(self):
        """
        Returns a score that determines how well this pawn is doing.
        """

        # Goals for maximum efficiency:

        # + Minimize incoming laser damage
        # + Maximize outgoing laser damage
        # + Maximize hit/miss ratio
        # + Maximize time alive

        hit_rate = self.laser_hits / self.lasers_shot
        fitness = 1000 * hit_rate ** 2
        # fitness *= self.laser_hits / 5

        if self.won:
            fitness *= 1.3
        if self.is_dead:
            fitness *= 0.7

        return fitness

    def on_death(self):
        """
        Called when this pawn is killed.
        """

        self.frames_alive = self.env.__frame_count__
        self.is_dead = True

    def use_shield(self):
        """
        Attempt to activate shield for this pawn.
        """

        if self.shield_count <= 0 or self.__shield_on__:
            return

        self.__shield_on__ = True
        self.shield_count -= 1

    def get_dir(self):
        return self.dir

    def get_speed(self):
        return self.speed

    def get_vel(self):
        return self.vel

    def get_health(self):
        return self.health

    def set_env(self, env):
        self.env = env

    def angle_to(self, pos):
        """
        Get the required direction to be looking at (in radians) the given position.
        """

        vec = (
            self.pos[0] - pos[0],
            self.pos[1] - pos[1]
        )

        d = math.atan2(vec[1], vec[0])
        return d

    def get_pawns(self):
        """
        Returns all pawns in the environment that isn't itself.
        """

        return self.env.get_pawns(self)

    def get_pos(self):
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
        Returns all lasers shot by the current pawn.
        """

        return self.lasers

    def look(self, direction):
        """
        Starts rotation towards 'right' (clockwise) or 'left' (counter-clockwise)
        Args:
            direction: Must be of value 'right', 'left', or None. Otherwise, it will be converted to None.
        """

        self.rotation = "right" if direction == "right" else "left" if direction == "left" else None

    def display_fitness(self):
        arcade.draw_text(str(round(self.calculate_fitness())),
                         self.pos[0]-100, self.pos[1]-35, arcade.color.WHITE, align="center", width=200)

    def draw_health_bar(self):
        """
        Displays the pawns health above it's graphical representation.
        Length is set in the global variable 'HEALTH_BAR_WIDTH'.
        Height above it's body is set in the global variable 'HEALTH_BAR_HEIGHT'.
        """

        if self.health <= 0:
            return

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

    def draw(self, color=arcade.color.WHITE):
        """
        Creates the graphical representation for the pawn using a triangle & circle.
        Sizing is relative to the radius field variable.
        """

        if self.__shield_on__:
            color = arcade.color.BLUE
        elif self.health <= 0:
            color = arcade.color.RED

        # Get triangle verticies relative to the rotation stored in the field variable 'direction'.
        facing = (math.cos(self.dir) * self.radius*1.3,
                  math.sin(self.dir) * self.radius*1.3)

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
        if self.brain_constructor == None:
            self.display_fitness()

    def press(self, key):
        """
        Called when a key is pressed, this method executes the action assigned to a given key
        in the manual control overrides.
        """

        if self.acontrols != None:
            if key in self.acontrols:
                i = self.acontrols.index(key)

                if i == 0:
                    self.__long_held__ = True
                elif i == 1:
                    self.__short_held__ = True
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

    def has_active_shield(self):
        """
        Returns wether this pawn has it's shield active.
        """

        return self.__shield_on__

    def get_shield_count(self):
        """
        Returns how many shields this pawn has.
        """

        return self.shield_count

    def take_damage(self, amount):
        """
        Inflicts damage on this pawn.
        """
        hit = True

        if self.__shield_dura__ <= 0 and self.__shield_on__:
            self.__shield_on__ = False
            self.__shield_dura__ = self.shield_durability

            # Shield de-activates before damage can be taken
            return
        elif self.__shield_on__:
            self.__shield_dura__ -= 1
            hit = False

        if hit:
            self.health -= amount
            self.laser_hits_taken += 1

    def attack(self, t="long"):
        """
        Checks if the pawn is on laser cooldown, if not it dispatches a laser from the origin of the
        graphical representation.

        Args:
            type (string): Type of attack. Accepts 'long' & 'short'.
        """

        if self.laser_on_cooldown():
            return

        laser = None
        b = self.bias

        if t == "long":
            laser = laser_beam.LaserBeam(
                [self.pos[0], self.pos[1]],
                self.dir,
                self.short_laser_life * b.short_laser_life_mod,
                self.long_laser_life * b.long_laser_life_mod,
                self.long_laser_damage * b.long_laser_damage_mod,
                self.long_laser_speed * b.long_laser_speed_mod,
                arcade.color.RED, self)

            self.lasers_shot += 1
        elif t == "short":
            laser = laser_beam.LaserBeam(
                [self.pos[0], self.pos[1]],
                self.dir,
                0,
                self.short_laser_life * b.short_laser_life_mod,
                self.short_laser_damage * b.short_laser_damage_mod,
                self.short_laser_speed * b.short_laser_speed_mod,
                arcade.color.BLUE, self)

            self.lasers_shot += 1

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

        Returns:
            A list of all pawns that were killed by lasers.
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

        if self.acontrols != None:
            if key in self.acontrols:
                i = self.acontrols.index(key)

                if i == 0:
                    self.__long_held__ = False
                elif i == 1:
                    self.__short_held__ = False
                elif i == 2:
                    self.use_shield()

                return

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
        Returns the pawn's rotational heading.
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

        self.frames_alive += 1

        if self.__short_held__:
            self.attack("short")
        elif self.__long_held__:
            self.attack("long")

        if self.health <= -100:
            self.health = self.max_health

        # Artifical controller decision making process if a brain is contained.
        if self.brain != None:
            self.brain.on_tick(delta_time)

        # Check for laser collisions
        for l in lasers:
            if self.colliding_with(l):
                if l.get_distance_traveled_squared() < l.minimum_life_span_squared:
                    l.kill(None)
                    continue

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

    def dist_squared(self, pos, compare_pos=None):
        """
        Args:
            pos: Tuple or array of the pos in the form [x,y].

        Returns:
            The distance squared from this pawn to the given pos.
        """

        if compare_pos == None:
            compare_pos = self.pos

        return math.pow(compare_pos[0]-pos[0], 2) + math.pow(compare_pos[1]-pos[1], 2)
