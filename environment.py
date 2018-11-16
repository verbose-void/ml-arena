import arcade
import sys
import math
import random
from actors import pawn
from models import brain, dynamic_scripting_brain

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600


class Environment(arcade.Window):
    def __init__(self, pawns):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT)
        arcade.set_background_color(arcade.color.BLACK)

        self.starting_data = dict()

        for pawn in pawns:
            pawn.set_env(self)
            self.starting_data[pawn] = (pawn.get_pos(), pawn.get_dir())

        self.pawns = pawns
        self.dead_pawns = []

        self.__death_anim_count__ = 100
        self.__frame_count__ = 0

    def restart(self):
        """
        Restarts to beginning game state.
        """

        if self.__death_anim_count__ > 0:
            self.__death_anim_count__ -= 1
            return

        self.__death_anim_count__ = 100
        self.__frame_count__ = 0

        new_pawns = []

        for pawn in self.dead_pawns:
            new_pawns.append(pawn.reset())

        self.dead_pawns.clear()

        for pawn in self.pawns:
            new_pawns.append(pawn.reset())

        self.pawns = new_pawns

    def on_draw(self):
        """
        Called every cycle prior to update.
        """

        arcade.start_render()

        for pawn in self.pawns:
            pawn.draw_lasers()
            pawn.draw()

        for pawn in self.dead_pawns:
            pawn.draw()

    def get_lasers(self, pawn):
        """
        @return Returns a list of all lasers that are not owned by the given pawn.
        """

        lasers = []

        for lpawn in self.pawns:
            if lpawn != pawn:
                for l in lpawn.get_lasers():
                    lasers.append(l)
        return lasers

    def get_pawns(self, pawn):
        """
        Returns all opposing pawns.
        @param pawn The calling pawn.
        """

        pawns = []

        for p in self.pawns:
            if p != pawn:
                pawns.append(p)

        return pawns

    def kill_pawn(self, pawn):
        """
        Removes the given pawn from the players list, effectively killing it.
        """

        if pawn in self.pawns:
            self.pawns.remove(pawn)
            self.dead_pawns.append(pawn)

    def update(self, delta_time):
        """
        Called every cycle prior to on_draw.
        """
        self.__frame_count__ += 1

        if len(self.pawns) <= 1:
            self.restart()

        for pawn in self.pawns:
            lasers = self.get_lasers(pawn)
            pawn.update(lasers, delta_time)
            pawns_killed = pawn.update_lasers(delta_time)

            if len(pawns_killed) > 0:
                for pawn in pawns_killed:
                    self.kill_pawn(pawn)

    def on_key_press(self, symbol, modifiers):
        """
        Called when a key is pressed. Then passed to each pawn to check if it's in their control scheme.
        """

        for pawn in self.pawns:
            pawn.press(symbol)

    def on_key_release(self, symbol, modifiers):
        """
        Called when a key is released. Then passed to each pawn to check if it's in their control scheme.
        """

        for pawn in self.pawns:
            pawn.release(symbol)
        return super().on_key_release(symbol, modifiers)


def default_player_pawn():
    """
    Generates a default player-controlled pawn with a default controller scheme.
    """

    return pawn.Pawn(None, SCREEN_WIDTH * 0.2, SCREEN_HEIGHT / 2, 0,
                     # Movement
                     (arcade.key.A, arcade.key.W, arcade.key.D, arcade.key.S),
                     # Directional
                     (arcade.key.LEFT, arcade.key.RIGHT),
                     # Attacks & Shield
                     (arcade.key.LSHIFT, arcade.key.SPACE, arcade.key.Q))


def default_mindless_pawn():
    """
    Generates a stagnant, brainless pawn.
    """

    out = pawn.Pawn(brain.Brain, SCREEN_WIDTH *
                    0.8, SCREEN_HEIGHT / 2, math.pi)
    return out


def dynamic_scripting_pawn(x, y, rot=math.pi):
    """
    Generates a pawn with responses pre-programmed.
    """

    # out = pawn.Pawn(dynamic_scripting_brain.DynamicBrain, x, y, 1)
    out = pawn.Pawn(
        dynamic_scripting_brain.DynamicBrain, x, y, rot)
    return out


def dynamic_vs_dynamic_game():
    """
    Creates and runs a Dynamic Brain vs another Dynamic Brain game.
    """

    env = Environment([dynamic_scripting_pawn(SCREEN_WIDTH * 0.2, SCREEN_HEIGHT / 2, 0), dynamic_scripting_pawn(
        SCREEN_WIDTH * 0.8, SCREEN_HEIGHT / 2)])
    arcade.run()


def player_vs_dynamic_game():
    """
    Creates and runs a Player vs Dynamic Brain game.
    """

    env = Environment([default_player_pawn(), dynamic_scripting_pawn(
        SCREEN_WIDTH * 0.8, SCREEN_HEIGHT / 2)])
    arcade.run()


def player_vs_mindless():
    """
    Creates and runs a Player vs Stagnant Pawn game.
    """

    env = Environment([default_player_pawn(), default_mindless_pawn()])
    arcade.run()


def dynamic_royale(amount):
    pawns = []
    for i in range(amount):
        pawns.append(dynamic_scripting_pawn(
            random.randint(100, SCREEN_WIDTH - 100),
            random.randint(100, SCREEN_HEIGHT - 100)))
    env = Environment(pawns)
    arcade.run()
    return env


if __name__ == "__main__":
    # player_vs_mindless()
    player_vs_dynamic_game()
    # dynamic_vs_dynamic_game()
    # dynamic_royale(50)
