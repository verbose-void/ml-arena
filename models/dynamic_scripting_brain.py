import time
import math
import arcade
import random

DEBUG = False


class DynamicBrain:
    def __init__(self, pawn):
        self.pawn = pawn

        # Define shield usage strategy
        shield_strats = [
            # Shields are used throughout the game in a spread out manner.
            "spread",
            # Shields are used when the pawn is low health as a "panic" action.
            "panic"
        ]

        # Initialize shield strategy at random.
        self.shield_strat = random.choice(shield_strats)

        # print("Dynamic Brain initialized with a " +
        #       self.shield_strat + " shield strategy.")

    def on_tick(self, dt):
        if self.pawn.env == None:
            return

        pawn = self.pawn
        enemy = self.pawn.env.get_closest_enemy(self.pawn)

        if enemy == None:
            pawn.move(0, 0)
            pawn.look(None)
            return

        if self.shield_strat == "spread":
            if pawn.health < pawn.max_health / pawn.max_shield_count * pawn.shield_count:
                # Use shields periodically throughout gameplay.
                pawn.use_shield()
        elif self.shield_strat == "panic":
            if pawn.health < pawn.long_laser_damage * 4:
                # Use shields when health is critical.
                pawn.use_shield()

        dist_sqrd = pawn.dist_squared(enemy.get_pos())

        if pawn.env.__frame_count__ % 10 == 0:
            self.move_to_expected_best()

        # Look towards their current position
        # self.look_towards(enemy.get_pos())

        attack_type = None
        bias = 100

        if dist_sqrd <= pawn.short_laser_life ** 2:
            attack_type = "short"
            bias = 200
        elif dist_sqrd <= pawn.long_laser_life**2:
            attack_type = "long"
        else:
            # Move towards enemy
            pawn.move(
                enemy.pos[0] - pawn.pos[0],
                enemy.pos[1] - pawn.pos[1])

            self.look_towards(
                self.get_best_aim_position(enemy, dist_sqrd, bias=bias))
            return

        # Look towards their expected next position
        self.look_towards(
            self.get_best_aim_position(enemy, dist_sqrd, bias=bias))

        if attack_type:
            pawn.attack(attack_type)
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

    def move_to_expected_best(self):
        """
        Analyzes all enemy laser paths and chooses the path of least resistance.

        Does NOT take into consideration delta time, because it is calculating the best
        future reward, not necessarily immediately following the current frame.
        """

        pawn = self.pawn
        lasers = pawn.env.get_lasers(pawn)  # All enemy lasers

        has_to_move = False
        possible = []

        # These help when the pawn has no place to go
        # that is completely safe.
        best_move = None
        max_dist = float("-inf")

        # Loop through every possible move
        for i in range(-1, 2):
            for j in range(-1, 2):

                # Loop through every laser and get if it's heading towards
                # the current testing position

                dx = pawn.pos[0] + i * pawn.radius * 1.5
                dy = pawn.pos[1] + j * pawn.radius * 1.5

                if DEBUG:
                    # Draw each path of testing for debugging
                    arcade.draw_line(
                        pawn.pos[0], pawn.pos[1], dx, dy, arcade.color.WHITE, 2)

                for laser in lasers:

                    dist = laser.get_dist_if_in_path((dx, dy), pawn.radius)
                    if dist <= -1:
                        possible.append((i, j))
                    else:
                        has_to_move = True
                        if max_dist < dist:
                            best_move = (i, j)
                            max_dist = dist

        if DEBUG:
            arcade.finish_render()

        if len(possible) > 0:
            if has_to_move:
                if best_move != None:
                    pawn.move(best_move[0], best_move[1])
                else:
                    c = random.choice(possible)
                    pawn.move(c[0], c[1])

        else:
            enemy = self.pawn.env.get_closest_enemy(self.pawn)
            if random.random() < 0.5:
                pawn.move(enemy.vel[1], enemy.vel[0])
            else:
                pawn.move(enemy.pos[0] - pawn.pos[0],
                          enemy.pos[1] - pawn.pos[1])

    def get_best_aim_position(self, pawn, dist_squared, bias=100):
        """
        Args:
            dist_squared (float): Squared distance from this pawn to the enemy.

        Returns:
            The best position to aim with the given params.
        """

        pos = pawn.get_pos()
        vel = pawn.get_vel()
        dist = math.sqrt(dist_squared)

        if dist < pawn.short_laser_life * pawn.bias.short_laser_life_mod:
            scalar = dist/pawn.short_laser_speed*bias
        else:
            scalar = dist/pawn.long_laser_speed*bias

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
