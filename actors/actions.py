from enum import Enum
import arcade


class Actions(Enum):
    # Movement
    MOVE_LEFT = 1
    MOVE_UP = 2
    MOVE_RIGHT = 3
    MOVE_DOWN = 4

    # Directional
    LOOK_LEFT = 5
    LOOK_RIGHT = 6

    # Actions
    SHORT_ATTACK = 7
    LONG_ATTACK = 8
    USE_SHIELD = 9


class PlayerActions(Enum):
    """Defines the possible inputs for a player driven Actor."""

    # Admin
    END_GAME = 10
    END_ROUND = 11
    SHOW_ALL_MATCH_UPS = 12
    SHOW_CONNECTIONS = 13
    SHOW_TRACERS = 14
    SHOW_NETWORKS = 15
    SPEED_UP = 16


DEFAULT_MAP = {
    arcade.key.W: Actions.MOVE_UP,
    arcade.key.A: Actions.MOVE_LEFT,
    arcade.key.S: Actions.MOVE_DOWN,
    arcade.key.D: Actions.MOVE_RIGHT,

    arcade.key.RIGHT: Actions.LOOK_RIGHT,
    arcade.key.LEFT: Actions.LOOK_LEFT,

    arcade.key.SPACE: Actions.SHORT_ATTACK,
    arcade.key.LSHIFT: Actions.LONG_ATTACK,
    arcade.key.Q: Actions.USE_SHIELD,

    arcade.key.ESCAPE: PlayerActions.END_GAME,
    arcade.key.BACKSPACE: PlayerActions.END_ROUND,
    arcade.key.BRACKETLEFT: PlayerActions.SHOW_ALL_MATCH_UPS,
    arcade.key.BRACKETRIGHT: PlayerActions.SHOW_CONNECTIONS,
    arcade.key.BACKSLASH: PlayerActions.SHOW_TRACERS,
    arcade.key.N: PlayerActions.SHOW_NETWORKS,
    arcade.key.P: PlayerActions.SPEED_UP
}
