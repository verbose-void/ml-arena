from environments.environment import *
from util.population import *


class EvolutionEnvironment(Environment):
    current_gen: int = 0
    population: Population

    def __init__(self, population: Population):
        self.population = population
        self.reset(build_new_gen=False)
        super().__init__()

    def reset(self, build_new_gen=True):
        pop = self.population

        if build_new_gen:
            pop.natural_selection()
            pop.generate_creatures()
            self.current_gen += 1
            super().reset()

        self.match_ups = pop.build_match_ups()
        self.calculate_best_match_up()

    def on_draw(self):
        super().on_draw()

        # Draw best neural network graphically
        if self.draw_best:
            if self.best_match_up != None:
                best_creature = self.best_match_up.get_best_pawn_based_on_fitness(
                    include_dead=True
                )

                if best_creature != None:
                    net = self.population.get_network(best_creature)
                    net.draw_weights()
                    net.draw_neurons()

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
