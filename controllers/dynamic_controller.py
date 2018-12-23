from controllers.controller import *
from enum import Enum
from typing import Tuple, Callable, Set
import random

from actors.laser import *
from actors.actor import *
from actors.pawns.pawn import *
from util.match_up import *
from util.stat_biases import *

DEBUG = False


class ShieldStrat(Enum):
    SPREAD = 0
    PANIC = 1


class DynamicController(Controller):

    shield_strat: ShieldStrat

    imminent_laser: Laser = None
    lasers: Set[Laser] = None
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
        """
        Set 'next_move' to the most viable velocity combination.
        Analyzes all enemy laser paths and chooses the path of least resistance.
        Does NOT take into consideration delta time, because it is calculating the best
        future reward, not necessarily immediately following the current frame.
        """

        pawn: Pawn = self.actor
        lasers = self.lasers
        laser: Laser

        moves_map = dict()
        initialized = False

        # Loop through every possible move
        for i in range(-1, 2):
            for j in range(-1, 2):
                move = (i, j)

                # Loop through every laser and get if it's heading towards
                # the current testing position

                dx = pawn.get_x() + i * BODY_RADIUS * 1.5
                dy = pawn.get_y() + j * BODY_RADIUS * 1.5

                if DEBUG:
                    # Draw each path of testing for debugging
                    arcade.draw_line(
                        pawn.pos[0], pawn.pos[1], dx, dy, arcade.color.WHITE, 2)

                for laser in lasers:
                    if moves_map.get(move, None) == None:
                        initialized = True
                        moves_map[move] = float('-inf')

                    dist = laser.get_dist_if_in_path((dx, dy), BODY_RADIUS)

                    # Log the worst move
                    moves_map[move] = \
                        max(moves_map[move], dist)

        if DEBUG:
            arcade.finish_render()

        if initialized:
            # Pick min moves_map
            min_dist = float('inf')
            best_move = None
            for move in moves_map.keys():
                worst = moves_map[move]
                if worst < min_dist:
                    min_dist = worst
                    best_move = move

            self.next_move = best_move

        else:
            # if random.random() < 0.5:
            #     pawn.move(enemy.vel[1], enemy.vel[0])
            # else:
            #     pawn.move(enemy.pos[0] - pawn.pos[0],
            #               enemy.pos[1] - pawn.pos[1])

            pawns_dist = pawn.dist_squared(actor=self.closest_opponent)

            if pawns_dist > 600:

                # Move towards enemy

                # Get raw distance
                raw_dist = pawn.dist_squared(actor=self.closest_opponent)
                raw_move = (
                    self.closest_opponent.get_x() - pawn.get_x(),
                    self.closest_opponent.get_y() - pawn.get_y()
                )

                # Get world wrap distance
                wrap_dist = float('inf')
                wrap_move = (0, 0)
                for i in range(2):
                    for j in range(2):
                        dist = pawn.dist_squared(pos=(
                            SCREEN_WIDTH * i,
                            SCREEN_HEIGHT * j
                        ))

                        dist += self.closest_opponent.dist_squared(pos=(
                            SCREEN_WIDTH * j,
                            SCREEN_HEIGHT * i
                        ))

                        if dist < wrap_dist:
                            wrap_dist = dist

                            xv = SCREEN_WIDTH * i
                            yv = SCREEN_HEIGHT * j

                            wrap_move = (
                                xv if xv > 0 else -1,
                                yv if yv > 0 else -1
                            )

                # Set next move to closest
                self.next_move = raw_move if raw_dist <= wrap_dist else wrap_move

            else:

                # Move away from enemy
                self.next_move = (
                    pawn.get_x() - self.closest_opponent.get_x(),
                    pawn.get_y() - self.closest_opponent.get_y()
                )

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
        self.lasers = match_up.get_lasers(self.actor)
        self.imminent_laser = match_up.get_most_imminent_laser(self.actor)

    def think(self):
        """Determine the best course of action."""

        p: Pawn = self.actor
        sb: StatBias = p.stat_bias
        e_sb: StatBias = self.closest_opponent.stat_bias

        self.set_optimal_move()
        self.set_optimal_attack()
        self.optimal_lead = p.get_best_aim_position(self.closest_opponent)
        ss = self.shield_strat

        if ss == ShieldStrat.SPREAD:

            if p.health < sb.max_health / sb.max_shield_count * p.shield_count:
                # Use shields periodically throughout gameplay.
                self.will_use_shield_next = True

        elif ss == ShieldStrat.PANIC:

            if p.health < e_sb.long_attack_damage * 3:
                # Use shields when health is critical.
                self.will_use_shield_next = True

    def act(self):
        """Act out decision."""
        p: Pawn = self.actor

        p.set_vel(self.next_move if self.next_move else (0, 0))
        p.look_towards(pos=self.optimal_lead)

        if self.next_attack:
            self.next_attack()
            p.clear_attack()

        if self.will_use_shield_next:
            p.use_shield()
