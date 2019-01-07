from actors.pawns.pawn import *


class FitnessPawn(Pawn):
    total_hits: int = 0
    total_attacks: int = 1
    total_hits_taken: int = 1

    def calculate_fitness(self):
        # attacks_missed = self.total_attacks - self.total_hits
        # numerator = self.total_hits ** 2
        # denominator = 7 * (self.total_hits_taken + attacks_missed)
        # return numerator / denominator

        # hits_weighted = self.total_hits_taken * 0.7
        # attacks_weighted = self.total_attacks * 0.3
        # detriment = hits_weighted + attacks_weighted
        # return max(0, self.total_hits - detriment)

        return max(0, self.total_hits - (self.total_hits_taken * 0.2))

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
