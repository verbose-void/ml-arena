from environments.evolution_environment import *
from environments.environment import *
from util.population import *


class AdversarialEvolutionEnvironment(EvolutionEnvironment):
    population1: Population
    population2: Population
    opponent_index: int = 0

    def __init__(self, population1: Population, population2: Population):
        self.population1 = population1
        self.population2 = population2
        super().__init__(population1)
        self.reset(build_new_gen=False)

    def reset(self, build_new_gen=True):
        pop = self.population1
        pop2 = self.population2

        if build_new_gen:
            pop.natural_selection()
            pop.generate_creatures()
            pop.current_gen += 1

            if pop.current_gen % 5 == 0:
                pop.save_to_dir()

            pop2.natural_selection()
            pop2.generate_creatures()
            pop2.current_gen += 1

            if pop2.current_gen % 5 == 0:
                pop2.save_to_dir()

        self.start_time = time.time()
        self.match_ups = pop.build_match_ups(other_population=pop2)
        self.calculate_best_match_up()

    def on_draw(self):
        Environment.on_draw(self)

        if self.draw_networks:
            # Draw best neural network graphically
            if self.draw_best:
                if self.best_match_up != None:
                    for pawn in self.best_match_up.pawns:

                        net1 = self.population1.get_network(pawn)
                        if net1 != None:
                            net1.draw_weights()
                            net1.draw_neurons(offset_y=SCREEN_HEIGHT/2)

                        net2 = self.population2.get_network(pawn)
                        if net2 != None:
                            net2.draw_weights()
                            net2.draw_neurons()

    def end(self):
        arcade.close_window()
        self.population1.save_to_dir()
        if self.population1.dir_name == self.population2.dir_name:
            self.population2.save_to_dir(self.population1.dir_name + '(1)')
        else:
            self.population2.save_to_dir()

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

        out = 'Generations: %i-%i' % (
            self.population1.current_gen, self.population2.current_gen)
        out += spacer

        out += Environment.__str__(self)
        out += spacer

        out += 'Max Alive Fitness: %i' % round(max_alive_fitness)
        out += spacer

        out += 'Max Overall Fitness: %i' % round(self.absolute_max_fitness)

        return out
