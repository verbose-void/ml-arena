from environments.environment import *


class EvolutionEnvironment(Environment):
    current_gen: int = 1

    def reset(self):
        super().reset()

        self.current_gen += 1

    def __str__(self):
        spacer = ' | '

        if self.best_match_up:
            best = self.best_match_up.get_best_pawn_based_on_fitness()

            if best:
                max_alive_fitness = best.calculate_fitness()
            else:
                max_alive_fitness = -1
        else:
            max_alive_fitness = 0

        out = 'Generation: %i' % self.current_gen
        out += spacer

        out += super().__str__()
        out += spacer

        out += 'Max Alive Fitness: %i' % round(max_alive_fitness)
        out += spacer

        out += 'Max Overall Fitness: %i' % round(self.absolute_max_fitness)

        return out
