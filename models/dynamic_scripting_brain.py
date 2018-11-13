import time
import math
import arcade


class DynamicBrain:
    def __init__(self, pawn):
        self.pawn = pawn

    def on_tick(self):
        enemy = self.get_closest_enemy()
        self.look_towards(enemy.get_pos())

    def get_closest_enemy(self):
        min_dist = float("inf")
        dist_sqrd = None
        closest = None

        for enemy in self.pawn.get_pawns():
            dist_sqrd = self.pawn.dist_squared(enemy.get_pos())
            if min_dist > dist_sqrd:
                min_dist = dist_sqrd
                closest = enemy

        return closest

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
        if d > 0:
            pawn.look("left")
        elif d < 0:
            pawn.look("right")
        else:
            pawn.look(None)
