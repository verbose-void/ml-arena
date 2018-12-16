from actors.actions import *
from actors.actor import *
import arcade

PA = PlayerActions


class Controller:
    """Default controller class"""
    actor: Actor

    def __init__(self, actor: Actor):
        assert actor != None, 'Actor must NOT be NoneType.'
        self.actor = actor

    def on_key_press(self, symbol):
        """Does nothing for a basic controller."""
        pass

    def on_key_release(self, symbol):
        """Does nothing for a basic controller."""
        pass

    def submit_action(self, action: 'PlayerActions'):
        """Does the given action."""
        a = self.actor

        # Movement
        if action == PA.MOVE_LEFT:
            a.set_vel((-1, None))

        elif action == PA.MOVE_RIGHT:
            a.set_vel((1, None))

        elif action == PA.MOVE_UP:
            a.set_vel((None, 1))

        elif action == PA.MOVE_DOWN:
            a.set_vel((None, -1))

        # Directional
        elif action == PA.LOOK_LEFT:
            a.set_looking(-1)

        elif action == PA.LOOK_RIGHT:
            a.set_looking(1)

        elif action == PA.SHORT_ATTACK:
            a.short_attack()

        elif action == PA.LONG_ATTACK:
            a.long_attack()

        elif action == PA.USE_SHIELD:
            a.use_shield()

    def undo_action(self, action: 'PlayerActions'):
        """Undoes the given action."""
        a = self.actor

        # Movement
        if action == PA.MOVE_LEFT or action == PA.MOVE_RIGHT:
            a.set_vel((0, None))

        elif action == PA.MOVE_UP or action == PA.MOVE_DOWN:
            a.set_vel((None, 0))

        # Directional
        elif action == PA.LOOK_LEFT or action == PA.LOOK_RIGHT:
            a.set_looking(0)

        elif action == PA.SHORT_ATTACK or action == PA.LONG_ATTACK:
            a.clear_attack()

    def look(self, match_up):
        """Observes data from the environment."""
        pass

    def think(self):
        """Transforms data / makes a decision."""
        pass

    def act(self):
        """Acts on decision."""
        pass
