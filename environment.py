import arcade
import imp

pawn = imp.load_source("pawn", "actors/pawn.py")

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600


class Environment(arcade.Window):
    def __init__(self, pawns):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT)
        arcade.set_background_color(arcade.color.BLACK)
        self.pawns = pawns

    def setup(self):
        # Set up your game here
        pass

    def on_draw(self):
        arcade.start_render()

        # Your drawing code goes here
        for pawn in self.pawns:
            pawn.draw()

    def update(self, delta_time):
        for pawn in self.pawns:
            pawn.update()
        pass

    def on_key_press(self, symbol, modifiers):
        for pawn in self.pawns:
            pawn.press(symbol)
        return super().on_key_press(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        for pawn in self.pawns:
            pawn.release(symbol)
        return super().on_key_release(symbol, modifiers)


if __name__ == "__main__":
    rightPawn = pawn.Pawn(SCREEN_WIDTH * 0.8, SCREEN_HEIGHT / 2)

    leftPawn = pawn.Pawn(SCREEN_WIDTH * 0.2, SCREEN_HEIGHT / 2,
                         (arcade.key.A, arcade.key.W, arcade.key.D,
                          arcade.key.S),
                         (arcade.key.LEFT, arcade.key.RIGHT))

    env = Environment([leftPawn, rightPawn])
    arcade.run()
