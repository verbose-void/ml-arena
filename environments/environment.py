

import arcade
import time
from actors.actions import *

PA = PlayerActions

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

from util.match_up import *


def max_helper(match_up):
    best = match_up.get_best_pawn_based_on_fitness()
    if best:
        return best.calculate_fitness()

    return -1


class Environment(arcade.Window):
    match_ups: set = None
    best_match_up: MatchUp = None
    absolute_max_fitness: float = 0

    draw_best = True
    draw_match_connections = False
    draw_dead = False
    draw_tracers = False

    start_time: float
    started = False

    max_game_length: int = 45  # 45 seconds

    frame_count: int = 0
    print_str: str = ''

    def __init__(self, *match_ups: MatchUp):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT)
        arcade.set_background_color(arcade.color.BLACK)
        self.start_time = time.time()
        self.match_ups = set(match_ups)
        self.calculate_best_match_up()
        self.print_str = self.__str__()

    def run(self):
        if self.started:
            raise Exception('Environment has already begun.')
        self.started = True
        arcade.run()

    def calculate_best_match_up(self):
        """Sets the 'best_match_up' property based on each pawn's fitness."""

        self.best_match_up = max(
            self.match_ups, key=max_helper)
        return self.best_match_up

    def on_draw(self):
        arcade.start_render()

        if self.draw_best:
            if self.best_match_up:
                self.best_match_up.draw(draw_dead=self.draw_dead,
                                        draw_tracers=self.draw_tracers)

        else:
            match_up: MatchUp

            for match_up in self.match_ups:
                if match_up.is_still_going():
                    match_up.draw(draw_dead=self.draw_dead,
                                  draw_tracers=self.draw_tracers)

                    if self.draw_match_connections:
                        prev = None

                        for pawn in match_up.get_alive_pawns():
                            if prev != None:
                                arcade.draw_line(
                                    prev.pos[0], prev.pos[1], pawn.pos[0], pawn.pos[1], arcade.color.RED_DEVIL)

                            prev = pawn

        arcade.draw_text(
            self.print_str,
            10,
            SCREEN_HEIGHT - 20,
            arcade.color.WHITE
        )

    def on_update(self, delta_time):
        if (not self.are_match_ups_still_going()) or \
                (self.max_game_length > 0 and time.time() - self.start_time > self.max_game_length):

            return self.reset()

        self.frame_count += 1

        if self.frame_count % 60 == 0:
            self.calculate_best_match_up()
            self.print_str = self.__str__()

        match_up: MatchUp
        for match_up in self.match_ups:
            match_up.update(delta_time)
            best_pawn = match_up.get_best_pawn_based_on_fitness()

            if best_pawn:
                # Set the absolute max fitness
                self.absolute_max_fitness = \
                    max(self.absolute_max_fitness,
                        best_pawn.calculate_fitness())

    def reset(self):
        """Calls reset on each MatchUp & resets start_time."""
        match_up: MatchUp
        for match_up in self.match_ups:
            match_up.reset()

        self.start_time = time.time()
        self.frame_count = 0

    def are_match_ups_still_going(self):
        return self.running_matches_count() > 0

    def running_matches_count(self):
        running = 0

        match_up: MatchUp
        for match_up in self.match_ups:
            if match_up.is_still_going():
                running += 1

        return running

    def on_key_press(self, symbol, modifiers):
        # Handle Global Keys
        if symbol in DEFAULT_MAP:
            action = DEFAULT_MAP.get(symbol)

            if action == PA.END_GAME:
                self.end()
                return

            elif action == PA.END_ROUND:
                self.reset()
                return

            elif action == PA.SHOW_ALL_MATCH_UPS:
                self.draw_best = False
                return

            elif action == PA.SHOW_CONNECTIONS:
                self.draw_match_connections = True
                return

            elif action == PA.SHOW_TRACERS:
                self.draw_tracers = True
                return

        match_up: MatchUp

        for match_up in self.match_ups:
            match_up.on_key_press(symbol)

    def on_key_release(self, symbol, modifiers):
        # Handle Global Keys
        if symbol in DEFAULT_MAP:
            action = DEFAULT_MAP.get(symbol)

            if action == PA.SHOW_ALL_MATCH_UPS:
                self.draw_best = True
                return

            elif action == PA.SHOW_CONNECTIONS:
                self.draw_match_connections = False
                return

            elif action == PA.SHOW_TRACERS:
                self.draw_tracers = False
                return

        match_up: MatchUp

        for match_up in self.match_ups:
            match_up.on_key_release(symbol)

    def end(self):
        """Called on game end."""
        exit()

    def __str__(self):
        spacer = ' | '
        out = ''

        out += 'Matches: %i/%i' % \
            (self.running_matches_count(), len(self.match_ups))
        out += spacer

        out += 'Time: %i/%is' % \
            (round(time.time() - self.start_time), self.max_game_length)

        return out


if __name__ == '__main__':
    match_ups = set()
    match_up = MatchUp(
        Pawn(None, 100, 100),
        Pawn(None, 200, 100),
        Pawn(None, 100, 200),
        Pawn(None, 200, 200)
    )

    match_ups.add(match_up)

    env = Environment(match_ups)
    env.run()
