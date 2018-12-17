# Import base variables.
from actors.actor import *
from typing import Tuple

import arcade

"""
External Base Variables:
	BASE_MOVEMENT_SPEED
	BASE_DIRECTIONAL_SPEED
"""

# Base Variables
BASE_MAX_HEALTH = 100
BASE_MAX_SHIELD_COUNT = 5
BASE_SHIELD_STRENGTH = 10

BASE_LONG_ATTACK_RANGE: Tuple[float] = (250, 800)
BASE_SHORT_ATTACK_RANGE: Tuple[float] = (0, 400)

BASE_LONG_ATTACK_DAMAGE = 12
BASE_SHORT_ATTACK_DAMAGE = 8

BASE_LONG_ATTACK_SPEED = 600
BASE_SHORT_ATTACK_SPEED = 500

# Slomo Lasers
# BASE_LONG_ATTACK_SPEED = 100
# BASE_SHORT_ATTACK_SPEED = 100

BASE_LONG_LASER_COOLDOWN = 0.45
BASE_SHORT_LASER_COOLDOWN = 0.3


class StatBias:
    movement_speed: float
    directional_speed: float

    max_health: float
    max_shield_count: int
    shield_strength: float

    long_attack_range: Tuple[float]
    short_attack_range: Tuple[float]

    long_attack_damage: float
    short_attack_damage: float

    short_attack_speed: float
    long_attack_speed: float

    short_attack_cooldown: float
    long_attack_cooldown: float

    short_attack_color = arcade.color.BLUE
    long_attack_color = arcade.color.RED


class Normal(StatBias):
    """Makes no modifications to any base variables."""
    movement_speed: float = BASE_MOVEMENT_SPEED
    directional_speed: float = BASE_DIRECTIONAL_SPEED

    max_health: float = BASE_MAX_HEALTH
    max_shield_count: int = BASE_MAX_SHIELD_COUNT
    shield_strength: float = BASE_SHIELD_STRENGTH

    long_attack_range: Tuple[float] = BASE_LONG_ATTACK_RANGE
    short_attack_range: Tuple[float] = BASE_SHORT_ATTACK_RANGE

    long_attack_damage: float = BASE_LONG_ATTACK_DAMAGE
    short_attack_damage: float = BASE_SHORT_ATTACK_DAMAGE

    short_attack_speed: float = BASE_SHORT_ATTACK_SPEED
    long_attack_speed: float = BASE_LONG_ATTACK_SPEED

    long_attack_cooldown: float = BASE_LONG_LASER_COOLDOWN
    short_attack_cooldown: float = BASE_SHORT_LASER_COOLDOWN


class ShortRanged(Normal):
    movement_speed: float = Normal.movement_speed * 1.2
    directional_speed: float = Normal.directional_speed * 1.2

    short_attack_range: Tuple[float] = (
        Normal.short_attack_range[0],
        Normal.short_attack_range[1] * 1.2
    )

    short_attack_speed = Normal.short_attack_speed * 1.2

    long_attack_range: Tuple[float] = (
        Normal.long_attack_range[0] * 1.2,
        Normal.long_attack_range[1]
    )

    long_attack_speed = Normal.short_attack_speed * 0.8


class LongRanged(Normal):
    movement_speed: float = Normal.movement_speed * 0.9
    directional_speed: float = Normal.directional_speed * 0.9

    short_attack_range: Tuple[float] = (
        Normal.short_attack_range[0],
        Normal.short_attack_range[1] * 0.9
    )

    short_attack_speed = Normal.short_attack_speed * 0.9

    long_attack_range: Tuple[float] = (
        Normal.long_attack_range[0] * 0.9,
        Normal.long_attack_range[1]
    )

    long_attack_speed = Normal.short_attack_speed * 1.2
