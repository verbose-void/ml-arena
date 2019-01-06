from environments.environment import *
from util.population import *


class EvolutionEnvironment(Environment):
    population1: Population

    def __init__(self, population1: Population):
        self.population1 = population1
        self.reset(build_new_gen=False)
        super().__init__(*self.match_ups)

    def reset(self, build_new_gen=True):
        pop = self.population1

        if build_new_gen:
            pop.natural_selection()
            pop.generate_creatures()
            pop.current_gen += 1
            if pop.current_gen % 5 == 0:
                pop.save_to_dir()
            super().reset()

        self.match_ups = pop.build_match_ups()
        self.calculate_best_match_up()

    def on_draw(self):
        super().on_draw()

        if self.draw_networks:
            # Draw best neural network graphically
            if self.draw_best:
                if self.best_match_up != None:
                    best_creature = self.best_match_up.get_best_pawn_based_on_fitness(
                        include_dead=True
                    )

                    if best_creature != None:
                        net = self.population1.get_network(best_creature)
                        if net != None:
                            net.draw_weights()
                            net.draw_neurons()

    def end(self):
        arcade.close_window()
        self.population1.save_to_dir()
        Environment.end(self)

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

        out = 'Generation: %i' % self.population1.current_gen
        out += spacer

        out += Environment.__str__(self)
        out += spacer

        out += 'Max Alive Fitness: %.1f' % max_alive_fitness
        out += spacer

        out += 'Max Overall Fitness: %.1f' % self.absolute_max_fitness

        return out
