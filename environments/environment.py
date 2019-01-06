

import arcade
import time
from actors.actions import *

PA = PlayerActions

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

from util.match_up import *


def max_helper(match_up):
    best = match_up.get_best_pawn_based_on_fitness()
    if best:
        return best.calculate_fitness()

    return -1


USE_DELTA_TIME = True


class Environment(arcade.Window):
    match_ups: set = None
    best_match_up: MatchUp = None
    absolute_max_fitness: float = 0

    draw_best = True
    draw_match_connections = False
    draw_dead = False
    draw_tracers = False
    draw_networks = False
    started = False

    speed_up = False
    speed_up_cycles = 10
    max_game_length: int = 2700  # 45 seconds if 1 second = 60 frames

    frame_count: int = 0
    print_str: str = ''

    def __init__(self, *match_ups: MatchUp):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT)
        arcade.set_background_color(arcade.color.BLACK)
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
        if self.frame_count % 60 == 0:
            self.calculate_best_match_up()

        self.print_str = self.__str__()
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
        for i in range(1 if not self.speed_up else self.speed_up_cycles):
            self.frame_count += 1
            if (not self.are_match_ups_still_going()):
                return self.reset()

            if self.speed_up:
                if self.max_game_length > 0 and self.frame_count > self.max_game_length:
                    return self.reset()

            match_up: MatchUp
            for match_up in self.match_ups:
                match_up.update(delta_time if USE_DELTA_TIME else 1)
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

            elif action == PA.SPEED_UP:
                self.speed_up = not self.speed_up
                return

            if action == PA.SHOW_NETWORKS:
                self.draw_networks = not self.draw_networks
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
            (round(self.frame_count / 60),
             round(self.max_game_length / 60))

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
