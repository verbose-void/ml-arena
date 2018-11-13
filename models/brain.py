class Brain:
    """
    This class acts as an abstract class that allows the injection of predictive models,
    dynamic scripts, random jargon, and everything in between. Gives direct access to the assigned
    pawn's API.
    """

    def __init__(self, pawn):
        self.pawn = pawn

    def on_tick(self):
        """
        This method will be called every time the game loop calls update. Should encapsulate all brain logic.
        """

        pass
