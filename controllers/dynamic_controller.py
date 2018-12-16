from controllers.controller import *
from enum import Enum
from typing import Tuple, Callable
import random

from actors.laser import *
from actors.actor import *
from actors.pawns.pawn import *
from util.match_up import *
from util.stat_biases import *


class ShieldStrat(Enum):
    SPREAD = 0
    PANIC = 1


class DynamicController(Controller):

    shield_strat: ShieldStrat

    imminent_laser: Laser = None
    closest_opponent: Pawn = None

    next_move: Tuple[int] = None
    next_look: int = 0
    optimal_lead: Tuple[float, float] = None
    next_attack: Callable = None
    will_use_shield_next: bool = False

    def __init__(self, pawn: Pawn):
        super().__init__(pawn)

        self.shield_strat = random.choice(list(ShieldStrat))

    def set_optimal_move(self):
        """Set 'next_move' to the most viable velocity combination."""

        # Goal: Get out of the way of the imminent laser.
        il: Laser = self.imminent_laser

        if il == None:
            # Move towards enemy
            self.next_move = (
                self.closest_opponent.get_x() - self.actor.get_x(),
                self.closest_opponent.get_y() - self.actor.get_y()
            )
            return

        # Ideally, this value is -1.
        min_dist = float('inf')

        # Loop through all possible moves
        for i in range(-1, 2):
            for j in range(-1, 2):
                move = (i, j)

                dist = il.get_dist_if_in_path(move, BODY_RADIUS)

                if dist < min_dist:
                    min_dist = dist
                    self.next_move = move

                    if dist == -1:
                        break

    def set_optimal_attack(self):
        dist_squared = self.actor.dist_squared(actor=self.closest_opponent)
        sb: StatBias = self.actor.stat_bias

        if dist_squared <= sb.short_attack_range[1] ** 2:
            self.next_attack = self.actor.short_attack
        else:
            self.next_attack = self.actor.long_attack

    def look(self, match_up: MatchUp):
        """Observe the environment"""
        self.closest_opponent = match_up.get_closest_opponent(self.actor)
        self.imminent_laser = match_up.get_most_imminent_laser(self.actor)

    def think(self):
        """Determine the best course of action."""

        p: Pawn = self.actor
        sb: StatBias = p.stat_bias
        e_sb: StatBias = self.closest_opponent.stat_bias

        self.set_optimal_move()
        self.set_optimal_attack()
        self.optimal_lead = p.get_best_aim_position(self.closest_opponent)

        if self.shield_strat == "spread":
            if p.health < sb.max_health / sb.max_shield_count * p.shield_count:
                # Use shields periodically throughout gameplay.
                self.will_use_shield_next = True
        elif self.shield_strat == "panic":
            if p.health < e_sb.long_attack_damage * 3:
                # Use shields when health is critical.
                self.will_use_shield_next = True

    def act(self):
        """Act out decision."""
        p: Pawn = self.actor

        p.set_vel(self.next_move)
        p.look_towards(pos=self.optimal_lead)

        if self.next_attack:
            self.next_attack()
            p.clear_attack()

        if self.will_use_shield_next:
            p.use_shield()
