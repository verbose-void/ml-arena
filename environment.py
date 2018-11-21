import arcade
import sys
import time
import math
import random
from actors import pawn
from models import brain, dynamic_scripting_brain

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

MAX_GAME_LENGTH = 8  # 8 seconds


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

        self.draw_best = True

        self.match_ups = list(match_ups)
        self.__frame_count__ = 0
        self.on_restart = None
        self.best_match_up = 0
        self.on_end = None
        self.current_gen = 1
        self.print_string = ""
        self.start_time = time.time()

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

        self.start_time = time.time()

        self.__frame_count__ = 0

        if self.on_restart != None:
            self.on_restart(self)
        else:
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

        # Draw only the best pawn
        if self.draw_best and self.best_match_up != None:
            match_up = self.match_ups[self.best_match_up]
            l = len(match_up)
            for pawn in match_up:
                pawn.draw_lasers()

                if l <= 1:
                    # If this pawn is the winner, then color them green.
                    pawn.draw(arcade.color.GREEN)
                else:
                    pawn.draw()

            for pawn in self.match_up_data[self.best_match_up]["dead_pawns"]:
                pawn.draw()

        else:
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

        # Display how many matches are running
        arcade.draw_text(self.print_string, 10,
                         SCREEN_HEIGHT-20, arcade.color.WHITE)

    def update_print_string(self):
        best_alive_fitness = -1
        running = 0
        best_overall_fitness = -1

        for i, match_up in enumerate(self.match_ups):
            l = len(match_up)
            if l > 1:
                running += 1

            for pawn in match_up:
                if pawn.brain_constructor == None:

                    fit = pawn.calculate_fitness()

                    if l > 1:
                        if fit > best_alive_fitness:
                            best_alive_fitness = fit
                            self.best_match_up = i

                    if fit > best_overall_fitness:
                        best_overall_fitness = fit

            for pawn in self.match_up_data[i]['dead_pawns']:
                if pawn.brain_constructor == None:

                    fit = pawn.calculate_fitness()

                    if fit > best_overall_fitness:
                        best_overall_fitness = fit

        self.print_string = ""

        self.print_string += "Generation: " + \
            str(self.current_gen) + " | "

        self.print_string += "Matches Running: " + \
            str(running) + "/" + str(round(self.pop_size/2)) + " | "

        self.print_string += "Best Alive Fitness: " + \
            str(round(best_alive_fitness)) + " | "

        self.print_string += "Best Overall Fitness: " + \
            str(round(best_overall_fitness)) + " | "

        self.print_string += "Time Elapsed/Allotted: " + \
            str(round(time.time() - self.start_time)) + \
            "/" + str(MAX_GAME_LENGTH)

    def get_lasers(self, pawn):
        """
        Returns a list of all lasers in their match that are not owned by the given pawn.

        Args:
            pawn (Pawn): The pawn that is requesting the lasers.
        """

        lasers = []

        try:
            for lpawn in self.match_ups[pawn.match_index]:
                if lpawn != pawn:
                    for l in lpawn.get_lasers():
                        lasers.append(l)
        except:
            print("exc")
            print(pawn.match_index)
            print(len(self.match_ups))

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

        if time.time() - self.start_time > MAX_GAME_LENGTH or self.are_all_episodes_over():
            self.restart()

        self.__frame_count__ += 1

        # if self.__frame_count__ % 60 == 0:
        #     best_fitness = float('-inf')
        #     best_match = None

        #     # Pick a best pawn
        #     for i, match_up in enumerate(self.match_ups):
        #         if len(match_up) <= 1:
        #             match_up[0].won = True
        #             continue

        #         p = match_up[0]
        #         fit = p.calculate_fitness()
        #         if fit > best_fitness:
        #             best_fitness = fit
        #             best_match = i

        #     if best_match != None:
        #         self.best_match_up = best_match

        # Update all pawns in all match ups

        for i, match_up in enumerate(self.match_ups):
            for pawn in match_up:

                if pawn.match_index < 0:
                    continue

                lasers = self.get_lasers(pawn)
                pawn.update(lasers, delta_time)
                pawns_killed = pawn.update_lasers(delta_time)

                if len(pawns_killed) > 0:
                    for pawn in pawns_killed:
                        self.kill_pawn(pawn)

        if self.on_restart != None:
            self.update_print_string()

    def on_key_press(self, symbol, modifiers):
        """
        Called when a key is pressed. Then passed to each pawn to check if it's in their control scheme.
        """

        if symbol == arcade.key.ESCAPE:
            # End the game.
            arcade.close_window()
            if self.on_end != None:
                self.on_end(self)
            return

        if symbol == arcade.key.BRACKETLEFT:
            self.draw_best = False
            print("ENABLE SHOW ALL")

        for match_up in self.match_ups:
            for pawn in match_up:
                pawn.press(symbol)

    def on_key_release(self, symbol, modifiers):
        """
        Called when a key is released. Then passed to each pawn to check if it's in their control scheme.
        """

        if symbol == arcade.key.BRACKETLEFT:
            self.draw_best = True
            print("DISABLE SHOW ALL")

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


def player_from_str(s):
    if s == "player":
        return default_player_pawn()
    elif s == "dynamic":
        return dynamic_scripting_pawn(random.random() * SCREEN_WIDTH, random.random() * SCREEN_HEIGHT)
    elif s == "mindless":
        return default_mindless_pawn()

    return None


def prompt_for_player(pid):
    print("")
    print("-------------------------------")
    print("What player should be player " + pid + "?")
    print("Hint: You can choose between:")
    print(" [player, dynamic, mindless]")
    print("-------------------------------")
    print("")


if __name__ == "__main__":
    prompt_for_player("1")
    p1 = player_from_str(input("P1 Choice: "))

    if p1 == None:
        print("That isn't a valid player.")
        exit()

    prompt_for_player("2")
    p2 = player_from_str(input("P2 Choice: "))

    if p2 == None:
        print("That isn't a valid player.")
        exit()

    env = Environment([p1, p2])
    arcade.run()
