from environments.environment import *


class FreeplayEnvironment(Environment):
    gen_based: bool = False

    def __str__(self):
        return 'Time Elapsed: %is' % round(self.frame_count / 60)

    def on_reset(self):
        """No resets."""
        pass
