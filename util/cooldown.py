import time


class Cooldown:
    start: float = 0
    length: float = 0

    def __init__(self, cooldown_length_in_seconds: float):
        self.set_cooldown_time(cooldown_length_in_seconds)
        self.start = -10000

    def reset(self, frame):
        self.start = frame

    def set_cooldown_time(self, cooldown_length_in_frames: float):
        assert cooldown_length_in_frames > 0, 'Cooldown length MUST be positive.'
        self.length = cooldown_length_in_frames

    def on_cooldown(self, frame) -> bool:
        return frame - self.start < self.length
