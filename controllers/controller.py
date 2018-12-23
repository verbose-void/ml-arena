from actors.actions import *
from actors.actor import *
import arcade

PA = PlayerActions
A = Actions


class Controller:
    """Default controller class"""
    actor: Actor
    active_actions: set = None

    def __init__(self, actor: Actor):
        assert actor != None, 'Actor must NOT be NoneType.'
        self.actor = actor
        self.active_actions = set()

    def on_key_press(self, symbol):
        """Does nothing for a basic controller."""
        pass

    def on_key_release(self, symbol):
        """Does nothing for a basic controller."""
        pass

    def submit_action(self, action: 'PlayerActions'):
        """Does the given action."""
        a: Pawn = self.actor

        if a.is_dead:
            return

        # Movement
        if action == A.MOVE_LEFT:
            a.set_vel((-1, None))

        elif action == A.MOVE_RIGHT:
            a.set_vel((1, None))

        elif action == A.MOVE_UP:
            a.set_vel((None, 1))

        elif action == A.MOVE_DOWN:
            a.set_vel((None, -1))

        # Directional
        elif action == A.LOOK_LEFT:
            a.set_looking(-1)

        elif action == A.LOOK_RIGHT:
            a.set_looking(1)

        elif action == A.SHORT_ATTACK:
            a.short_attack()

        elif action == A.LONG_ATTACK:
            a.long_attack()

        elif action == A.USE_SHIELD:
            a.use_shield()

        self.active_actions.add(action)

    def undo_action(self, action: 'PlayerActions'):
        """Undoes the given action."""
        a = self.actor

        # Movement
        if action == A.MOVE_LEFT or action == A.MOVE_RIGHT:
            a.set_vel((0, None))

        elif action == A.MOVE_UP or action == A.MOVE_DOWN:
            a.set_vel((None, 0))

        # Directional
        elif action == A.LOOK_LEFT or action == A.LOOK_RIGHT:
            a.set_looking(0)

        elif action == A.SHORT_ATTACK or action == A.LONG_ATTACK:
            a.clear_attack()

        self.active_actions.discard(action)

    def look(self, match_up):
        """Observes data from the environment."""
        pass

    def think(self):
        """Transforms data / makes a decision."""
        pass

    def act(self):
        """Acts on decision."""
        pass
