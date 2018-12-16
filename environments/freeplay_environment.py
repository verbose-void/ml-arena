from environments.environment import *


class FreeplayEnvironment(Environment):
    gen_based: bool = False

    def __str__(self):
        return 'Time Elapsed/Allotted: %is' % round(time.time() - self.start_time)

    def on_reset(self):
        """No resets."""
        pass
