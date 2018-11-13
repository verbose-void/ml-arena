import arcade
import sys
import math
from actors import pawn, short_range_pawn, long_range_pawn
from models import brain, dynamic_scripting_brain

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600


class Environment(arcade.Window):
    def __init__(self, pawns):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT)
        arcade.set_background_color(arcade.color.BLACK)

        for pawn in pawns:
            pawn.set_env(self)

        self.pawns = pawns
        self.lasers = []

    def on_draw(self):
        """
        Called every cycle prior to update.
        """

        arcade.start_render()

        for pawn in self.pawns:
            pawn.draw_lasers()
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

        self.pawns.remove(pawn)

    def update(self, delta_time):
        """
        Called every cycle prior to on_draw.
        """

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
        return super().on_key_press(symbol, modifiers)

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

    return pawn.Pawn(None, SCREEN_WIDTH * 0.2, SCREEN_HEIGHT / 2, (arcade.key.A, arcade.key.W, arcade.key.D, arcade.key.S), (arcade.key.LEFT, arcade.key.RIGHT), arcade.key.SPACE)


def default_mindless_pawn():
    """
    Generates a stagnant, brainless pawn.
    """

    out = pawn.Pawn(brain.Brain, SCREEN_WIDTH * 0.8, SCREEN_HEIGHT / 2)
    out.dir = math.pi
    return out


def dynamic_scripting_pawn():
    """
    Generates a pawn with responses pre-programmed.
    """

    out = pawn.Pawn(dynamic_scripting_brain.DynamicBrain,
                    SCREEN_WIDTH * 0.8, SCREEN_HEIGHT / 2)
    out.dir = 2
    return out


if __name__ == "__main__":
    env = Environment([default_player_pawn(), dynamic_scripting_pawn()])
    arcade.run()
