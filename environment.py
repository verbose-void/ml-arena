import arcade
import sys
import math
import random
from actors import pawn
from models import brain, dynamic_scripting_brain

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600


class Environment(arcade.Window):
    def __init__(self, *match_ups):
        """
        Create an instance of an Arena environment.

        Args:
            *match_ups (array of pawns): Each argument under 'match_ups' should be an array containing the participating pawns for that fight.
        """

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT)
        arcade.set_background_color(arcade.color.BLACK)

        self.match_up_data = dict()

        for i, match_up in enumerate(match_ups):
            # Initialize game-unique data
            self.match_up_data[i] = {
                "starting": dict(),
                "dead_pawns": []
            }

            for pawn in match_up:
                pawn.match_index = i
                pawn.set_env(self)
                self.match_up_data[i]["starting"][pawn] = (
                    pawn.get_pos(), pawn.get_dir())

        self.match_ups = list(match_ups)
        self.__frame_count__ = 0

    def get_closest_enemy_laser(self, pawn):
        """
        Returns the closest enemy laser to the given pawn.
        """

        lasers = self.get_lasers(pawn)
        min_dist = float("inf")
        dist_sqrd = None
        closest = None

        for laser in lasers:
            dist_sqrd = pawn.dist_squared(laser.pos)
            if dist_sqrd < min_dist:
                min_dist = dist_sqrd
                closest = laser

        return closest

    def get_closest_enemy(self, pawn):
        """
        Returns the closest pawn to the given pawn.
        """

        min_dist = float("inf")
        dist_sqrd = None
        closest = None

        for enemy in self.match_ups[pawn.match_index]:
            if pawn != enemy:
                dist_sqrd = pawn.dist_squared(enemy.get_pos())
                if min_dist > dist_sqrd:
                    min_dist = dist_sqrd
                    closest = enemy

        return closest

    def restart(self):
        """
        Restarts all games to beginn   ing states.
        """

        self.__frame_count__ = 0

        for i, match_up in enumerate(self.match_ups):

            new = list()

            for pawn in match_up:
                new.append(pawn.reset())

            # Put all dead pawns back in their respective alive container
            # and reset them.
            for pawn in self.match_up_data[i]["dead_pawns"]:
                new.append(pawn.reset())

            # Clear dead pawns
            self.match_up_data[i]["dead_pawns"].clear()
            self.match_ups[i] = new

    def on_draw(self):
        """
        Called every cycle prior to update.
        """

        arcade.start_render()

        # Draw all matches
        for i, match_up in enumerate(self.match_ups):
            l = len(match_up)
            for pawn in match_up:
                pawn.draw_lasers()

                if l <= 1:
                    # If this pawn is the winner, then color them green.
                    pawn.draw(arcade.color.GREEN)
                else:
                    pawn.draw()

            for pawn in self.match_up_data[i]["dead_pawns"]:
                pawn.draw()

    def get_lasers(self, pawn):
        """
        Returns a list of all lasers in their match that are not owned by the given pawn.

        Args:
            pawn (Pawn): The pawn that is requesting the lasers.
        """

        lasers = []

        for lpawn in self.match_ups[pawn.match_index]:
            if lpawn != pawn:
                for l in lpawn.get_lasers():
                    lasers.append(l)

        return lasers

    def get_pawns(self, pawn):
        """
        Returns all opposing pawns.

        Args:
            pawn (Pawn): The pawn that is requesting the enemies.
        """

        pawns = []

        for p in self.match_ups[pawn.match_index]:
            if p != pawn:
                pawns.append(p)

        return pawns

    def kill_pawn(self, pawn):
        """
        Removes the given pawn from the players list, effectively killing it.

        Args:
            pawn (Pawn): The pawn that is to be killed.
        """

        match_up = self.match_ups[pawn.match_index]

        if pawn in match_up:
            match_up.remove(pawn)
            self.match_up_data[pawn.match_index]["dead_pawns"].append(pawn)
            pawn.on_death()

    def are_all_episodes_over(self):
        """
        Checks if all current matches are over.
        """

        for match_up in self.match_ups:
            if len(match_up) > 1:
                return False

        return True

    def update(self, delta_time):
        """
        Called every cycle prior to on_draw.
        """

        self.__frame_count__ += 1

        if self.are_all_episodes_over():
            self.restart()

        # Update all pawns in all match ups

        for i, match_up in enumerate(self.match_ups):
            for pawn in match_up:
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

        for match_up in self.match_ups:
            for pawn in match_up:
                pawn.press(symbol)

    def on_key_release(self, symbol, modifiers):
        """
        Called when a key is released. Then passed to each pawn to check if it's in their control scheme.
        """

        for match_up in self.match_ups:
            for pawn in match_up:
                pawn.release(symbol)


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
                    random.random(), SCREEN_HEIGHT * random.random(), math.pi)
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


if __name__ == "__main__":
    # player_vs_mindless()
    # player_vs_dynamic_game()
    # dynamic_vs_dynamic_game()

    env = Environment([default_player_pawn(), default_mindless_pawn()],
                      [default_mindless_pawn(), dynamic_scripting_pawn(200, 200)])

    # env = Environment(
    #     [dynamic_scripting_pawn(500, 200), dynamic_scripting_pawn(200, 200)])
    arcade.run()
