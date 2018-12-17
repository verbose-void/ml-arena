from environments.environment import *


class EvolutionEnvironment(Environment):
    current_gen: int = 0

    def reset(self):
        super().reset()

        self.current_gen += 1

    def __str__(self):
        spacer = ' | '

        if self.best_match_up:
            max_alive_fitness = self.best_match_up.get_best_pawn_based_on_fitness().calculate_fitness()
        else:
            max_alive_fitness = 0

        out = 'Generation: %i' % self.current_gen
        out += spacer

        out += super().__str__()
        out += spacer

        out += 'Max Alive Fitness: %i' % round(max_alive_fitness)
        out += spacer

        out += 'Max Overall Fitness: %i' % round(self.absolute_max_fitness)
        out += spacer

        return out
