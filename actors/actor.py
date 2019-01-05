import math
from typing import Union, Tuple, List, Callable
from environments.environment import *

# Base Stats
BASE_MOVEMENT_SPEED = 100
BASE_DIRECTIONAL_SPEED = 2

# Determines how large the body will be.
BODY_RADIUS = 20
BODY_RADIUS_SQUARED = BODY_RADIUS ** 2


def find_intersection(x1, y1, x2, y2, x3, y3, x4, y4):
    px = ((x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4)) / \
        ((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4))
    py = ((x1*y2-y1*x2)*(y3-y4)-(y1-y2)*(x3*y4-y3*x4)) / \
        ((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4))
    return [px, py]


def dist_squared(p1, p2):
    return math.pow(p1[0]-p2[0], 2) + \
        math.pow(p1[1]-p2[1], 2)


class Actor:

    pos: List[float] = None
    vel: List[float] = None
    movement_speed: float = BASE_MOVEMENT_SPEED

    direc: float = 0
    directional_speed: float = BASE_DIRECTIONAL_SPEED

    # Defines which way the actor is looking towards (changes the direc incrementally on update)
    looking: int = 0

    # Defines how far they can move offscreen before wrapping
    max_outward_bound: int = 50

    # If holding an attack button, this function gets called.
    current_attack: Callable = None

    def get_movement_speed(self):
        return self.movement_speed

    def get_directional_speed(self):
        return self.directional_speed

    def get_looking(self):
        return self.looking

    def get_direc(self):
        return self.direc

    def get_pos(self):
        assert self.pos != None, 'Actor positions HAVE to be initialized.'
        return self.pos

    def get_x(self):
        return self.pos[0]

    def get_y(self):
        return self.pos[1]

    def get_x_v(self):
        return self.vel[0]

    def get_y_v(self):
        return self.vel[1]

    def get_vel(self):
        assert self.vel != None, 'Actor velocities HAVE to be initialized.'
        return self.vel

    def set_pos(self, new_pos: Tuple[float]):
        self.pos = list(new_pos)
        self.wrapX()
        self.wrapY()

    def wrapX(self) -> bool:
        """Wraps the X pos. Returns True if wrapping occured."""

        if self.pos[0] < -self.max_outward_bound:
            self.pos[0] = SCREEN_WIDTH + self.max_outward_bound
            return True
        elif self.pos[0] > SCREEN_WIDTH + self.max_outward_bound:
            self.pos[0] = -self.max_outward_bound
            return True

        return False

    def wrapY(self) -> bool:
        """Wraps the Y pos. Returns True if wrapping occured."""

        if self.pos[1] < -self.max_outward_bound:
            self.pos[1] = SCREEN_HEIGHT + self.max_outward_bound
            return True
        elif self.pos[1] > SCREEN_HEIGHT + self.max_outward_bound:
            self.pos[1] = -self.max_outward_bound
            return True

        return False

    def set_vel(self, new_vel: Tuple[float, float]):
        """Automatically normalized to -1, 0, or 1."""

        # Set values to -1, 0, or 1.
        for i, am in enumerate(new_vel):
            if am == None:
                continue

            if am < 0:
                self.vel[i] = -1

            elif am > 0:
                self.vel[i] = 1

            else:
                self.vel[i] = 0

    def set_looking(self, new_looking: int):
        """
        Args:
                new_looking(int): MUST be -1 (LEFT), 0 (NONE), or 1 (RIGHT).
        """

        assert new_looking == 0 or new_looking == 1 or new_looking == - \
            1, 'Actors can only look right, left, or nowhere.'

        self.looking = new_looking

    def set_direc(self, new_direc: float):
        """Sets the direction to a normalized value from 0-2Pi"""
        self.direc = new_direc % (math.pi * 2)

    def set_movement_speed(self, new_movement_speed: float):
        self.movement_speed = new_movement_speed

    def modify_pos(self, updater: Tuple[float]):
        """Adds the given 'updater' to the position."""
        self.set_pos((
            self.get_x() + updater[0],
            self.get_y() + updater[1]
        ))

    def modify_direc(self, updater: float):
        """Adds the given 'updater' to the direction & normalizes the value."""
        self.set_direc(self.direc + updater)

    def raw_dist_squared(self, pos: Tuple[int] = None, actor: 'Actor' = None):
        """Returns the raw distance squared between this Actor & the given position / Actor."""

        assert pos != None or actor != None, 'Can\'t compute the distance between None & None.'
        assert not(pos != None and actor !=
                   None), 'Can only compute the distance between a position or an actor, not both.'

        position = pos if pos != None else actor.get_pos()

        return dist_squared(self.pos, position)

    def dist_squared(self, pos: Tuple[int] = None, actor: 'Actor' = None):
        """Returns the donut-compensated distance squared between this Actor & the given position / Actor."""
        raw_dist = self.raw_dist_squared(pos, actor)
        alt_dist = abs(max(SCREEN_WIDTH, SCREEN_HEIGHT) ** 2 - raw_dist)

        if alt_dist < raw_dist:
            print('alt')

        return min(raw_dist, alt_dist)

    def angle_to(self, pos: Tuple[int] = None, actor: 'Actor' = None):
        """
        Get the required direction to be looking at (in radians) the given position.
        """

        assert pos != None or actor != None, 'Can\'t compute the distance between None & None.'
        assert not(pos != None and actor !=
                   None), 'Can only compute the distance between a position or an actor, not both.'

        position = pos if pos != None else actor.get_pos()

        vec = (
            self.pos[0] - position[0],
            self.pos[1] - position[1]
        )

        d = math.atan2(vec[1], vec[0]) + (math.pi)

        if d < 0:
            # Convert to [0, 2pi] range
            d = math.pi + (-d)

        raw_dist = self.raw_dist_squared(pos, actor)
        alt_dist = max(SCREEN_WIDTH, SCREEN_HEIGHT) ** 2 - raw_dist

        if alt_dist < raw_dist:
            d += math.pi

        return d % (2*math.pi)

    def update(self, delta_time) -> float:
        """
        Updates this Actors position based on it's movement_speed, velocity, & current position.
        Also update's it's rotation if applicable.

        Returns:
            It's current position.
        """

        # Movement
        temp = self.movement_speed * delta_time
        self.modify_pos((
                        self.get_x_v() * temp,
                        self.get_y_v() * temp
                        ))

        # Direction
        self.set_direc(self.direc + (self.get_directional_speed()
                                     * delta_time * (-self.looking)))

        if self.current_attack != None:
            self.current_attack()

        return self.pos

    def on_tick(self, delta_time: float):
        self.update_pos()

    def draw(self):
        """Draws nothing since it's a basic actor."""
        pass

    def short_attack(self):
        self.current_attack = self.short_attack

    def long_attack(self):
        self.current_attack = self.long_attack

    def clear_attack(self):
        """Clears the current attack function (releases the key)."""
        self.current_attack = None

    def look_towards(self, pos: Tuple[int] = None, actor: 'Actor' = None):
        """
        Make the actor look at the given pos/actor.
        """

        assert pos != None or actor != None, 'Can\'t compute the distance between None & None.'
        assert not(pos != None and actor !=
                   None), 'Can only compute the distance between a position or an actor, not both.'

        pos: Tuple[float] = pos if pos != None else (
            actor.get_x(),
            actor.get_y()
        )

        di = self.get_direc()

        # A = (x1, y1)
        A = (math.cos(di)+self.pos[0], math.sin(di)+self.pos[1])

        # B = (x2, y2)
        B = (-math.cos(di)+self.pos[0], -math.sin(di)+self.pos[1])

        # P = (x, y)

        # d=(x−x1)(y2−y1)−(y−y1)(x2−x1)
        d = (pos[0]-A[0]) * (B[1]-A[1]) - (pos[1]-A[1]) * (B[0]-A[0])

        looking: int = 0

        if self.dist_squared(pos=pos) < self.raw_dist_squared(pos=pos):
            if d < 0.505:
                looking = -1
            elif d > 0.505:
                looking = 1

        else:
            if d > 0.505:
                looking = -1
            elif d < 0.505:
                looking = 1

        self.set_looking(looking)
