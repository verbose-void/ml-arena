from actors.pawns.pawn import *


class FitnessPawn(Pawn):
    total_hits: int = 0
    total_hits_taken: int = 0

    def calculate_fitness(self):
        return 10

    def log_hit(self):
        self.total_hits += 1

    def take_damage(self, amount):
        self.total_hits_taken += 1
        super().take_damage(amount)

    def reset(self):
        self.total_hits = 0
        self.total_hits_taken = 0
        super().reset()
