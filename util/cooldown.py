import time


class Cooldown:
    start: float = 0
    length: float = 0

    def __init__(self, cooldown_length_in_seconds: float):
        self.set_cooldown_time(cooldown_length_in_seconds)
        self.start = -10000

    def reset(self):
        self.start = time.time()

    def set_cooldown_time(self, cooldown_length_in_seconds: float):
        assert cooldown_length_in_seconds > 0, 'Cooldown length MUST be positive.'
        self.length = cooldown_length_in_seconds

    def on_cooldown(self) -> bool:
        return time.time() - self.start < self.length
