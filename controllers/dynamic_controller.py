from controllers.controller import *
from enum import Enum
import random


class ShieldStrat(Enum):
    SPREAD = 0
    PANIC = 1


class DynamicController(Controller):

    shield_strat: ShieldStrat

    def __init__(self):
        self.shield_strat = random.choice(list(ShieldStrat))

    def think(self):
        pass
