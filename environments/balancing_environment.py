from environments.environment import *
from util.match_up import *


class BalancingEnvironment(Environment):
    match_ups: set = None
    best_match_up: MatchUp = None
    max_game_length: int = -1

    def calculate_best_match_up(self):
        """Sets the 'best_match_up' property based on the first open matchup."""
        for match_up in self.match_ups:
            if len(match_up.get_alive_pawns()) > 1:
                self.best_match_up = match_up
                break

    def reset(self):
        """Ends this simulation."""
        self.end()

    def end(self):
        d = dict()
        pawn: Pawn = None
        total = 0

        for match_up in self.match_ups:
            alive_count = 0

            for pawn in match_up.pawns:
                if not pawn.is_dead:
                    alive_count += 1
                    total += 1

                    name = type(pawn.stat_bias).__name__

                    if name in d:
                        d[name] += 1
                    else:
                        d[name] = 1

            if alive_count > 1:
                print(
                    '\n\n\n\n\n\n\n\nEarly termination. Cannot provide accurate results.')
                Environment.end(self)
                return

        print('\n\n\n\n\n\n\n\nStatBias : Alive Pawn Count')
        print('------------------')
        for sb in d:
            print('%s: %i (%.1f' %
                  (sb, d[sb], d[sb] / total * 100) + '%' + ')')

        Environment.end(self)

    def __str__(self):
        return "Matches Running: %i/%i" % (self.running_matches_count(), len(self.match_ups))
