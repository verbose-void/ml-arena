from environments.environment import *
from actors.pawns.pawn import *
from controllers.controller import *
from controllers.player_controller import *

DEBUG = True
FRAMES_BETWEEN_DECISIONS = 10


class MatchUp:
    """Defines the structure for a set of pawns that will be aware of each other's presence."""

    pawns: set
    dead_pawns: set
    frames: int = 0

    def __init__(self, *pawns: Pawn):
        self.pawns = set(pawns)
        self.dead_pawns = set()

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

    def draw(self, draw_dead=False, draw_tracers=False):
        """Draws all pawns & lasers contained in this matchup."""

        pawn_set = self.get_alive_pawns() if not draw_dead else self.pawns
        pawn: Pawn

        player_pawn: Pawn = None
        imminent_laser: Laser = None

        if DEBUG:
            for pawn in pawn_set:
                if issubclass(type(pawn.controller), PlayerController):
                    player_pawn = pawn
                    imminent_laser = self.get_most_imminent_laser(player_pawn)

        # Draw all lasers first
        for pawn in pawn_set:
            pawn.draw_lasers(imminent_laser)

        # Then draw all pawn bodies
        for pawn in pawn_set:
            pawn.draw(draw_tracers=draw_tracers)

        # This way, pawn bodies will always overlay lasers.

    def update(self, delta_time, update_dead=False):
        """Updates all pawns & lasers contained in this matchup."""
        if not self.is_still_going():
            return

        self.frames += 1
        pawn_set = self.get_alive_pawns() if not update_dead else self.pawns
        pawn: Pawn
        controller: Controller

        for pawn in pawn_set:
            # Returns false if pawn is KIA
            if not pawn.update(self, delta_time):
                self.kill(pawn)
                break

            pawn.update_lasers(self, delta_time)

            # For now, look, think, and act every frame.

            if self.frames % FRAMES_BETWEEN_DECISIONS == 0:
                controller = pawn.controller

                controller.look(self)
                controller.think()
                controller.act()

    def get_best_pawn_based_on_fitness(self, include_dead=False):
        if not self.is_still_going() and not include_dead:
            return None

        pawn_set = self.get_alive_pawns() if not include_dead else self.pawns
        return max(pawn_set, key=lambda p: p.calculate_fitness())

    def get_closest_opponent(self, pawn: Pawn) -> Pawn:
        opponents = self.get_opponents_for(pawn)
        opponent: Pawn

        closest = None
        closest_dist = float('inf')

        for opponent in opponents:
            dist = pawn.dist_squared(actor=opponent)
            if closest_dist > dist:
                closest_dist = dist
                closest = opponent

        return closest

    def get_most_imminent_laser(self, pawn: Pawn) -> Laser:
        lasers = self.get_lasers(pawn)
        laser: Laser

        imminent: Laser = None
        any_on_route = False
        min_dist = float('inf')

        # If one is on route, they are immediately the most imminent
        # Unless... there is another laser on route that is closer.

        for laser in lasers:
            dist = laser.get_dist_if_in_path(pawn.get_pos(), BODY_RADIUS)

            if dist > 0:
                # ON ROUTE

                # If there weren't any on route before, disregard all previous calculations.
                if not any_on_route:
                    min_dist = dist
                    imminent = laser

                any_on_route = True

                if dist < min_dist:
                    imminent = laser
                    min_dist = dist

        return imminent

    def reset(self):
        self.dead_pawns.clear()

        pawn: Pawn
        for pawn in self.pawns:
            pawn.reset()

        self.frames = 0

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
