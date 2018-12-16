from environments.environment import *
from actors.pawns.pawn import *


class MatchUp:
    """Defines the structure for a set of pawns that will be aware of each other's presence."""

    pawns: set = set()
    dead_pawns: set = set()

    def __init__(self, *pawns: Pawn):
        self.pawns = set(pawns)

    def is_still_going(self):
        """Checks if this match up has a winner yet."""
        return len(self.pawns) - len(self.dead_pawns) > 1

    def kill(self, pawn: Pawn):
        self.dead_pawns.add(pawn)

    def get_lasers(self, pawn: Pawn) -> set:
        """Returns a set of all lasers in their match that are not owned by the given pawn."""

        opponents: set = self.get_opponents_for(pawn)
        opponent: Pawn
        lasers = set()

        for opponent in opponents:
            lasers.update(opponent.get_lasers())

        return lasers

    def get_alive_pawns(self):
        return self.pawns.copy().difference(self.dead_pawns)

    def get_opponents_for(self, pawn: Pawn) -> set:
        """Returns all ALIVE pawns that are not the given one."""

        # Remove implicitly raises an exception if pawn is not contained.
        alive = self.get_alive_pawns()
        alive.remove(pawn)
        return alive

    def draw(self, draw_dead=False):
        """Draws all pawns & lasers contained in this matchup."""

        pawn_set = self.get_alive_pawns() if not draw_dead else self.pawns
        pawn: Pawn

        for pawn in pawn_set:
            pawn.draw_lasers()
            pawn.draw()

    def update(self, delta_time, update_dead=False):
        """Updates all pawns & lasers contained in this matchup."""

        pawn_set = self.get_alive_pawns() if not update_dead else self.pawns
        pawn: Pawn

        for pawn in pawn_set:
            pawn.update(self, delta_time)
            pawn.update_lasers(self, delta_time)

    def get_best_pawn_based_on_fitness(self, include_dead=False):
        pawn_set = self.get_alive_pawns() if not include_dead else self.pawns
        return max(pawn_set, key=lambda p: p.calculate_fitness())

    def reset(self):
        self.dead_pawns.clear()
        new_pawns = set()

        pawn: Pawn
        for pawn in self.pawns:
            new_pawns.add(pawn.reset())

        self.pawns = new_pawns

    def on_key_press(self, symbol):
        pawn: Pawn
        for pawn in self.get_alive_pawns():
            pawn.on_key_press(symbol)

    def on_key_release(self, symbol):
        pawn: Pawn
        for pawn in self.get_alive_pawns():
            pawn.on_key_release(symbol)


if __name__ == '__main__':
    p1 = Pawn(None, 0, 0)
    p2 = Pawn(None, 0, 0)

    mu = MatchUp(p1, p2)
    print(mu.pawns)
