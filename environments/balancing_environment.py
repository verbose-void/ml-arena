from environments.environment import *
from util.match_up import *


class BalancingEnvironment(Environment):
    match_ups: set = None
    best_match_up: MatchUp = None

    def __init__(self, match_ups: set):
        super().__init__(match_ups)

    def calculate_best_match_up(self):
        """Sets the 'best_match_up' property based on the first open matchup."""
        for match_up in self.match_ups:
            if len(match_up) > 1:
                self.best_match_up = match_up
                break

    def __str__(self):
        return "Matches Running: %i/%i" % (self.running_matches_count(), len(self.match_ups))
