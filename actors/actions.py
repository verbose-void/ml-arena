from enum import Enum
import arcade


class PlayerActions(Enum):
    """Defines the possible inputs for a player driven Actor."""

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

    # Admin
    END_GAME = 10
    END_ROUND = 11
    SHOW_ALL_MATCH_UPS = 12
    SHOW_CONNECTIONS = 13
    SHOW_TRACERS = 14


DEFAULT_MAP = {
    arcade.key.W: PlayerActions.MOVE_UP,
    arcade.key.A: PlayerActions.MOVE_LEFT,
    arcade.key.S: PlayerActions.MOVE_DOWN,
    arcade.key.D: PlayerActions.MOVE_RIGHT,

    arcade.key.RIGHT: PlayerActions.LOOK_RIGHT,
    arcade.key.LEFT: PlayerActions.LOOK_LEFT,

    arcade.key.SPACE: PlayerActions.SHORT_ATTACK,
    arcade.key.LSHIFT: PlayerActions.LONG_ATTACK,
    arcade.key.Q: PlayerActions.USE_SHIELD,

    arcade.key.ESCAPE: PlayerActions.END_GAME,
    arcade.key.RETURN: PlayerActions.END_ROUND,
    arcade.key.BRACKETLEFT: PlayerActions.SHOW_ALL_MATCH_UPS,
    arcade.key.BRACKETRIGHT: PlayerActions.SHOW_CONNECTIONS,
    arcade.key.BACKSLASH: PlayerActions.SHOW_TRACERS
}
