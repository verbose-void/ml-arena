from actors.pawns.pawn import *
import math

HIT_RATE_COEFFICIENT = 2


class FitnessPawn(Pawn):
    total_hits: int = 0
    total_attacks: int = 1
    total_hits_taken: int = 1

    def calculate_fitness(self):
        hit_rate = self.total_hits / (math.log(self.total_attacks) + 0.1)
        fit = hit_rate * HIT_RATE_COEFFICIENT - math.log(self.total_hits_taken)
        return max(0, fit)

    def log_hit(self):
        self.total_hits += 1

    def long_attack(self):
        if super().long_attack():
            self.total_attacks += 1

    def short_attack(self):
        if super().short_attack():
            self.total_attacks += 1

    def take_damage(self, amount):
        self.total_hits_taken += 1
        return super().take_damage(amount)

    def kill(self):
        self.death_time = time.time()
        super().kill()

    def reset(self):
        self.total_hits = 0
        self.total_attacks = 1
        self.total_hits_taken = 1

        super().reset()
