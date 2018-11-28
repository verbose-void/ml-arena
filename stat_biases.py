class Normal:
    def __init__(self):
        # normal short range stats
        self.short_laser_life_mod = 1
        self.short_laser_damage_mod = 1
        self.short_laser_speed_mod = 1

        # normal long range stats
        self.long_laser_life_mod = 1
        self.long_laser_damage_mod = 1
        self.long_laser_speed_mod = 1

        # normal speed
        self.speed_mod = 1


class ShortRanged:
    def __init__(self):
        # 20% increase in short range stats
        self.short_laser_life_mod = 1.2
        self.short_laser_damage_mod = 1.2
        self.short_laser_speed_mod = 1.2

        # 20% decrease in long range stats
        self.long_laser_life_mod = 0.8
        self.long_laser_damage_mod = 0.8
        self.long_laser_speed_mod = 0.8

        # 20% increase in speed
        self.speed_mod = 1.2


class LongRanged:
    def __init__(self):
        # 20% decrease in short range stats
        self.short_laser_life_mod = 0.8
        self.short_laser_damage_mod = 0.8
        self.short_laser_speed_mod = 0.8

        # 20% increase in long range stats
        self.long_laser_life_mod = 1.2
        self.long_laser_damage_mod = 1.2
        self.long_laser_speed_mod = 1.2

        # 20% decrease in speed
        self.speed_mod = 0.8
