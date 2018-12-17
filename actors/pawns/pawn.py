from actors import actor
import arcade
import random
from enum import Enum
from util.match_up import *
from environments.environment import *
from controllers.controller import *
import math
from actors.laser import *
from typing import Set, Tuple
from util.cooldown import *
import util.stat_biases as SB

HALF_PI = math.pi / 2

DEFAULT_START_POS = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
RAY_TRACES = False

HEALTH_BAR_HEIGHT = 20
HEALTH_BAR_MAX_WIDTH = 60

# Determines how wide the base of the aiming cone should be.
LEG_BASE = BODY_RADIUS * 0.75
# Determines how far the end of the aiming cone should be.
CONE_END = BODY_RADIUS * 1.4


class StartTypes(Enum):
    RANDOM_START = 1
    FIXED_START = 2


class Pawn(actor.Actor):

    # Starter Data
    start_pos: tuple
    start_direc: float
    start_pos_type = None

    is_dead: bool = False
    health: float = 0

    # Shields
    shield_dura: int = 0  # How many hits this pawn's CURRENT shield has left.
    shield_count: int = 0
    shield_on: bool = False

    # Constants
    max_outward_bound: int = BODY_RADIUS

    # Laser Stuff
    lasers: Set[Laser] = None
    laser_cooldown = None

    controller: Controller
    stat_bias: SB.StatBias

    def __init__(
        self,
        start_pos_type=StartTypes.RANDOM_START,
        start_pos: list = DEFAULT_START_POS,
        start_direc: float = 0
    ):
        assert start_pos_type in StartTypes, 'Starting position type MUST be contained in the \'StartTypes\' enum.'

        self.stat_bias = SB.Normal
        self.start_pos_type = start_pos_type
        self.start_pos = list(start_pos)
        self.start_direc = start_direc
        self.controller = Controller(self)
        self.reset()

    def set_controller(self, controller: type):
        assert issubclass(type(controller), Controller) or issubclass(
            controller, Controller)

        if callable(controller):
            self.controller = controller(self)
        else:
            self.controller = controller

    def set_stat_bias(self, stat_bias: SB.StatBias):
        self.stat_bias = stat_bias

    def reset(self):
        sb: SB.StatBias = self.stat_bias

        self.vel = [0, 0]
        self.lasers = set()
        self.shield_on = False
        self.is_dead = False

        self.health = sb.max_health
        self.shield_count = sb.max_shield_count
        self.shield_dura = sb.shield_strength

        if self.start_pos_type == StartTypes.RANDOM_START:
            # randomly init position & direc
            self.set_pos(
                (SCREEN_WIDTH * random.random(), SCREEN_HEIGHT * random.random())
            )

            self.set_direc(math.pi * random.random() * 2)

        elif self.start_pos_type == StartTypes.FIXED_START:
            # set position & direc back to starting
            self.set_pos(
                (self.start_pos[0], self.start_pos[1])
            )

            self.set_direc(self.start_direc)

        else:
            raise Exception(
                'Starting position type MUST be contained in the "StartTypes" map.')

    def calculate_fitness(self):
        """Calculates this pawn's fitness (brainless = 0 always)."""
        return 0

    def kill(self):
        self.is_dead = True
        self.health = 0

    def take_damage(self, amount: float) -> bool:
        """
        Causes damage to the current Pawn.

        Args:
                amount (float): MUST be a positive float.

        Returns:
                bool:
                        True: if was killed as a result of this damage.
                        False: if no death was caused. DOES NOT MEAN THE PAWN IS STILL ALIVE!
        """
        if amount == 0:
            return False

        assert amount >= 0, 'Damage values MUST be positive.'

        self.hit_shield()  # handles shield dura etc.
        if self.is_dead or self.shield_on:
            return False

        self.health -= amount
        if self.health < 0:
            self.kill()

        return self.is_dead

    def hit_shield(self):
        """Damages this pawn's shield IF it has one currently on."""

        if not self.shield_on:
            return

        self.shield_dura -= 1

        if self.shield_dura <= 0:
            self.shield_on = False
            self.shield_dura = self.shield_count
            return

    def use_shield(self):
        """Attempts to equip a shield."""

        if self.shield_count <= 0 or self.shield_on:
            return

        self.shield_on = True
        self.shield_dura = self.stat_bias.shield_strength
        self.shield_count -= 1
        assert self.shield_count >= 0, 'Something went terribly wrong with shields...'

    def draw(self, color=arcade.color.WHITE):
        """
        Creates the graphical representation for the pawn using a triangle & circle.
        Sizing is relative to the BODY_RADIUS global variable.
        """

        if self.shield_on:
            color = arcade.color.BLUE

        if self.health <= 0:
            color = arcade.color.RED

        # Get triangle verticies relative to the rotation stored in the field variable 'direction'.
        facing = (math.cos(self.direc) * CONE_END,
                  math.sin(self.direc) * CONE_END)

        temp = self.direc+HALF_PI
        leftLeg = (math.cos(temp) * LEG_BASE,
                   math.sin(temp) * LEG_BASE)

        temp = self.direc-HALF_PI
        rightLeg = (math.cos(temp) * LEG_BASE,
                    math.sin(temp) * LEG_BASE)

        # Draw Ray Traces (Debugging)
        if RAY_TRACES:
            arcade.draw_line(self.pos[0], self.pos[1], facing[0]
                             * 1000, facing[1] * 1000, arcade.color.RED_DEVIL, 3)

        # Draw body circle
        arcade.draw_circle_filled(
            self.pos[0], self.pos[1], BODY_RADIUS * 0.7, color)

        # Draw triangle according to the determined verticies.
        arcade.draw_triangle_filled(self.pos[0]+facing[0], self.pos[1]+facing[1],
                                    self.pos[0] +
                                    leftLeg[0], self.pos[1]+leftLeg[1],
                                    self.pos[0] +
                                    rightLeg[0], self.pos[1]+rightLeg[1],
                                    color)

        self.draw_health_bar()
        self.draw_fitness_score()

    def draw_health_bar(self):
        """
        Displays the pawns health above it's graphical representation.
        Length is set in the global variable 'HEALTH_BAR_WIDTH'.
        Height above it's body is set in the global variable 'HEALTH_BAR_HEIGHT'.
        """

        if self.health <= 0:
            return

        x = self.pos[0] - HEALTH_BAR_MAX_WIDTH / 2
        y = self.pos[1] + BODY_RADIUS + HEALTH_BAR_HEIGHT

        normal_health = self.health / self.stat_bias.max_health

        color = arcade.color.GREEN

        if normal_health <= 0.2:
            color = arcade.color.RED
        elif normal_health <= 0.5:
            color = arcade.color.YELLOW
        elif normal_health <= 0.7:
            color = arcade.color.ORANGE

        arcade.draw_line(x, y, x + (HEALTH_BAR_MAX_WIDTH *
                                    normal_health), y, color, 5)

    def draw_fitness_score(self):
        fit = self.calculate_fitness()
        if fit <= 0:
            return

        arcade.draw_text(str(round(fit)),
                         self.pos[0]-100, self.pos[1]-35, arcade.color.WHITE, align="center", width=200)

    def draw_lasers(self, imminent_laser=None):
        laser: Laser
        for laser in self.lasers:
            if laser == imminent_laser:
                laser.draw(specific_color=arcade.color.GREEN)
            else:
                laser.draw()

    def update(self, match_up: 'MatchUp', delta_time) -> bool:
        """Returns False if this pawn was killed."""

        super().update(delta_time)

        enemy_lasers = match_up.get_lasers(self)
        laser: Laser
        for laser in enemy_lasers:
            if self.is_colliding_with_laser(laser):
                if self.take_damage(laser.get_damage()):
                    return False

                laser.kill()

        return True

    def is_colliding_with_laser(self, laser: Laser):
        if self.is_dead:
            return False

        return laser.dist_squared(actor=self) <= BODY_RADIUS_SQUARED

    def update_lasers(self, match_up: 'MatchUp', delta_time):
        dead = set()

        laser: Laser
        for laser in self.lasers:
            laser.update(delta_time)
            if laser.is_dead:
                dead.add(laser)

        # Delete all dead lasers
        self.lasers.difference_update(dead)

    def on_key_press(self, symbol):
        self.controller.on_key_press(symbol)

    def on_key_release(self, symbol):
        self.controller.on_key_release(symbol)

    def long_attack(self):
        sb: SB.StatBias = self.stat_bias

        if self.check_attack_capability_and_set_cooldown(sb.long_attack_cooldown):
            return

        super().long_attack()

        laser = Laser(
            self.pos,
            self.direc,
            speed=sb.long_attack_speed,
            min_life_span=sb.long_attack_range[0],
            max_life_span=sb.long_attack_range[1],
            damage=sb.long_attack_damage,
            color=sb.long_attack_color
        )

        self.lasers.add(laser)

    def short_attack(self):
        sb: SB.StatBias = self.stat_bias

        if self.check_attack_capability_and_set_cooldown(sb.short_attack_cooldown):
            return

        super().short_attack()

        laser = Laser(
            self.pos,
            self.direc,
            speed=sb.short_attack_speed,
            min_life_span=sb.short_attack_range[0],
            max_life_span=sb.short_attack_range[1],
            damage=sb.short_attack_damage,
            color=sb.short_attack_color
        )

        self.lasers.add(laser)

    def check_attack_capability_and_set_cooldown(self, cool_time) -> bool:
        """Returns True if on cooldown, otherwise False."""

        if self.laser_cooldown == None:
            self.laser_cooldown = Cooldown(cool_time)

        if self.laser_cooldown.on_cooldown():
            return True

        self.laser_cooldown.set_cooldown_time(cool_time)
        self.laser_cooldown.reset()
        return False

    def get_lasers(self):
        return self.lasers

    def get_best_aim_position(self, pawn: 'Pawn') -> Tuple[float, float]:
        """
        Args:
            actor (Actor): The actor to which you want the best aim position for.
        """

        bias = 100
        sb: StatBias = self.stat_bias

        pos = pawn.get_pos()
        vel = pawn.get_vel()
        dist = math.sqrt(self.dist_squared(actor=pawn))

        if dist < sb.short_attack_range[1]:
            scalar = dist / sb.short_attack_speed * bias
        else:
            scalar = dist / sb.long_attack_speed * bias

        return (
            pos[0] + vel[0]*scalar,
            pos[1] + vel[1]*scalar
        )
