

import arcade
import time

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

from util.match_up import *

MAX_GAME_LENGTH = 150  # 1.5 minutes


class Environment(arcade.Window):
    match_ups: set = None
    best_match_up: MatchUp = None
    absolute_max_fitness: float = 0

    draw_best = True
    draw_match_connections = False
    draw_dead = False

    current_gen: int = 0
    start_time: float
    on_reset = None
    started = False

    gen_based: bool = True

    def __init__(self, *match_ups: MatchUp):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT)
        arcade.set_background_color(arcade.color.BLACK)
        self.start_time = time.time()

        self.match_ups = set(match_ups)

    def run(self):
        if self.started:
            raise Exception('Environment has already begun.')
        self.started = True
        arcade.run()

    def calculate_best_match_up(self):
        """Sets the 'best_match_up' property based on each pawn's fitness."""

        self.best_match_up = max(
            self.match_ups, key=lambda mu: mu.get_best_pawn().calculate_fitness())
        return self.best_match_up

    def on_draw(self):
        arcade.start_render()

        if self.draw_best:
            if self.best_match_up:
                self.best_match_up.draw()

        else:
            match_up: MatchUp

            for match_up in self.match_ups:
                if match_up.is_still_going():
                    match_up.draw(draw_dead=self.draw_dead)

                    if self.draw_match_connections:
                        prev = None

                        for pawn in match_up.get_alive_pawns():
                            if prev != None:
                                arcade.draw_line(
                                    prev.pos[0], prev.pos[1], pawn.pos[0], pawn.pos[1], arcade.color.RED_DEVIL)

                            prev = pawn

        arcade.draw_text(
            self.__str__(),
            10,
            SCREEN_HEIGHT - 20,
            arcade.color.WHITE
        )

    def on_update(self, delta_time):
        if not self.are_match_ups_still_going() or \
                time.time() - self.start_time > MAX_GAME_LENGTH:

            return self.reset()

        self.calculate_best_match_up()

        match_up: MatchUp
        for match_up in self.match_ups:
            match_up.update(delta_time)

            # Set the absolute max fitness
            self.absolute_max_fitness = \
                max(self.absolute_max_fitness,
                    match_up.get_best_pawn().calculate_fitness())

    def reset(self):
        if self.on_reset != None:
            self.on_reset()
        else:
            match_up: MatchUp
            for match_up in match_ups:
                match_up.reset()

        if self.gen_based:
            self.current_gen += 1
            self.start_time = time.time()

    def are_match_ups_still_going(self):
        return self.running_matches_count() > 0

    def running_matches_count(self):
        running = 0

        match_up: MatchUp
        for match_up in self.match_ups:
            if match_up.is_still_going():
                running += 1

        return running

    def set_on_reset(self, func):
        if not callable(func):
            raise Exception('on_reset MUST be a function.')

        self.on_reset = func

    def on_key_press(self, symbol, modifiers):
        match_up: MatchUp

        for match_up in self.match_ups:
            match_up.on_key_press(symbol)

    def on_key_release(self, symbol, modifiers):
        match_up: MatchUp

        for match_up in self.match_ups:
            match_up.on_key_release(symbol)

    def __str__(self):
        if self.best_match_up:
            max_alive_fitness = self.best_match_up.get_best_pawn_based_on_fitness().calculate_fitness()
        else:
            max_alive_fitness = 0

        spacer = ' | '
        out = ''

        out += 'Gen: %i' % self.current_gen
        out += spacer

        out += 'Matches: %i/%i' % \
            (self.running_matches_count(), len(self.match_ups))
        out += spacer

        out += 'Max Alive Fitness: %i' % round(max_alive_fitness)
        out += spacer

        out += 'Max Overall Fitness: %i' % round(self.absolute_max_fitness)
        out += spacer

        out += 'Time Elapsed/Allotted: %i/%is' % \
            (round(time.time() - self.start_time), MAX_GAME_LENGTH)

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
