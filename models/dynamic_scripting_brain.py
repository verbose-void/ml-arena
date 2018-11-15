import time
import math
import arcade
import random


class DynamicBrain:
    def __init__(self, pawn):
        self.pawn = pawn

    def on_tick(self, dt):
        pawn = self.pawn
        enemy = self.get_closest_enemy()

        if enemy == None:
            pawn.move(0, 0)
            pawn.look(None)
            return

        optimal_dist_sqrd = math.pow(pawn.get_laser_life() * 0.85, 2)
        dist_sqrd = pawn.dist_squared(enemy.get_pos())

        # Look towards their current position
        # self.look_towards(enemy.get_pos())

        attack_type = None
        bias = 100

        if dist_sqrd <= math.pow(pawn.get_short_range_dist(), 2):
            attack_type = "short"
            bias = 200
        else:
            attack_type = "long"

        # Look towards their expected next position
        self.look_towards(
            self.get_best_aim_position(enemy, dist_sqrd, bias=bias))

        if dist_sqrd > optimal_dist_sqrd:
            # MOVE TOWARDS ENEMY

            pos = pawn.get_pos()
            e_pos = enemy.get_pos()

            vec = [
                -pos[0]+e_pos[0],
                -pos[1]+e_pos[1]
            ]

            pawn.move(vec[0], vec[1])
        else:
            pawn.attack(attack_type)
            self.move_to_expected_best()
            # # Random movements to simulate "strafing"
            # if round(time.time()) % 2 != 0:
            #     e_vel = enemy.get_vel()
            #     xv = random.randint(-1, 1)
            #     yv = random.randint(-1, 1)

            #     if xv == 0 and yv == 0:
            #         xv = 1

            #     pawn.move(xv, yv)

            # m = self.get_best_move()
            # pawn.move(m[0], m[1])

    def get_closest_enemy(self):
        """
        Returns the closest pawn to the given pawn.
        """

        min_dist = float("inf")
        dist_sqrd = None
        closest = None

        for enemy in self.pawn.get_pawns():
            dist_sqrd = self.pawn.dist_squared(enemy.get_pos())
            if min_dist > dist_sqrd:
                min_dist = dist_sqrd
                closest = enemy

        return closest

    def move_to_expected_best(self):
        """
        Analyzes all enemy laser paths and chooses the path of least resistance.

        Does NOT take into consideration delta time, because it is calculating the best
        future reward, not necessarily immediately following the current frame.
        """

        pawn = self.pawn
        lasers = pawn.env.get_lasers(pawn)  # All enemy lasers

        possible = []

        # Loop through every possible move
        for i in range(-1, 1):
            for j in range(-1, 1):

                # Loop through every laser and get if it's heading towards
                # the current testing position

                for laser in lasers:
                    on_route = laser.is_in_path(
                        (pawn.pos[0] + i * pawn.radius*2, pawn.pos[1] + j * pawn.radius*2), pawn.radius)
                    if not on_route:
                        possible.append((i, j))

        if len(possible) > 0:
            c = random.choice(possible)
        else:
            c = (random.randint(-1, 1), random.randint(-1, 1))
        pawn.move(c[0], c[1])

    def get_best_aim_position(self, pawn, dist_squared, bias=100):
        """
        @param dist_squared Squared distance from this pawn to the enemy.
        @return Returns the best position to aim with the given params.
        """

        pos = pawn.get_pos()
        vel = pawn.get_vel()
        dist = math.sqrt(dist_squared)
        scalar = dist/pawn.laser_speed*bias

        return [
            pos[0] + vel[0]*scalar,
            pos[1] + vel[1]*scalar
        ]

    def look_towards(self, pos):
        """
        Make the pawn look towards a given position.
        """

        pawn = self.pawn
        p_pos = pawn.get_pos()
        di = pawn.get_dir()

        # A = (x1, y1)
        A = (math.cos(di)+p_pos[0], math.sin(di)+p_pos[1])

        # B = (x2, y2)
        B = (-math.cos(di)+p_pos[0], -math.sin(di)+p_pos[1])

        # P = (x, y)

        # d=(x−x1)(y2−y1)−(y−y1)(x2−x1)
        d = (pos[0]-A[0])*(B[1]-A[1])-(pos[1]-A[1])*(B[0]-A[0])
        if d > 0.5:
            pawn.look("left")
        elif d < 0.5:
            pawn.look("right")
        else:
            pawn.look(None)
