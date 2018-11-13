from actors import pawn


class ShortRangePawn(pawn.Pawn):
    def __init__(self, x, y, mcontrols=None, dcontrols=None, acontrol=None):
        super().__init__(x, y, mcontrols, dcontrols, acontrol)

        # Stat Modifiers

        # 130% Speed
        self.speed *= 1.3

        # 60% Laser Life
        self.laser_life *= 0.6

        # 70% Health
        self.max_health *= 0.7

        # 115% Damage
        self.laser_damage *= 1.15
