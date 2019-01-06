from controllers.controller import *
import util.stat_biases as sb
import random

STAT_BIASES = [
    sb.Normal,
    sb.LongRanged,
    sb.ShortRanged
]


DEBUG = False


class ShiftingStatsController(Controller):
    shifting_rate = 2500
    current_index = -1

    def act(self):
        if self.act_cycles % self.shifting_rate == 0:
            self.act_cycles = 1

            while(True):
                r = random.randint(0, len(STAT_BIASES)-1)
                if r != self.current_index:
                    break

            self.current_index = r
            self.actor.stat_bias = STAT_BIASES[r]

            if DEBUG:
                print('Shifting Strats, new: %s' % self.actor.stat_bias)

        super().act()
