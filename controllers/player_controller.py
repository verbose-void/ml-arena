from controllers.controller import *


class PlayerController(Controller):
    def on_key_press(self, symbol):
        if symbol in DEFAULT_MAP.keys():
            self.submit_action(DEFAULT_MAP[symbol])

    def on_key_release(self, symbol):
        if symbol in DEFAULT_MAP.keys():
            self.undo_action(DEFAULT_MAP[symbol])
