from actors import pawn


class LongRangePawn(pawn.Pawn):
    def __init__(self, brain, x, y, mcontrols=None, dcontrols=None, acontrol=None):
        super().__init__(brain, x, y, mcontrols, dcontrols, acontrol)

        # Stat Modifiers

        # 80% Speed
        self.speed *= 0.8

        # 170% Laser Life
        self.laser_life *= 1.75

        # 120% Health
        self.max_health *= 1.2

        # 85% Damage
        self.laser_damage *= 0.85
