from environments.environment import *
from util.population import *
import matplotlib.pyplot as plt


class EvolutionEnvironment(Environment):
    population1: Population
    current_session_generation_count = 0
    max_iterations = 1

    generational_fitnesses = None
    alive_after_time = None

    def __init__(self, population1: Population):
        self.population1 = population1
        self.reset(build_new_gen=False)
        self.generational_fitnesses = []
        self.alive_after_time = []
        super().__init__(*self.match_ups)

    def build_iteration_report(self):
        s = 'Current Iteration: %i/%i (%.1f' % (
            self.current_session_generation_count,
            self.max_iterations,
            self.current_session_generation_count/self.max_iterations*100
        ) + '%' + ' complete!)'

        s += '\nMax Overall Fitness: %i' % self.absolute_max_fitness
        s += '\nGenerational Max Fitness: %i' % \
            self.current_gen_max_fitness

        return s

    def build_population_report(self, pop):
        s = 'Building new population for \"%s\".' % pop.dir_name
        s += '\nGeneration: %i' % pop.current_gen
        s += '\nAlive: %i' % pop.count_alive()

        return s

    def verbose(self):
        pop = self.population1
        print()
        print(self.build_iteration_report())
        print('----------------------------------')
        print(self.build_population_report(pop))

        # Graph data
        self.generational_fitnesses.append(self.current_gen_max_fitness)

    def reset(self, build_new_gen=True):
        pop = self.population1

        if build_new_gen:
            self.verbose()
            self.current_session_generation_count += 1
            if pop.current_gen > 0 and pop.current_gen % 5 == 0:
                pop.save_to_dir()

            pop.natural_selection()
            pop.generate_creatures()
            pop.current_gen += 1
            super().reset()

        self.match_ups = pop.build_match_ups()
        self.calculate_best_match_up()

    def run(self, iterations=10):
        res = Environment.run(self)
        if res:
            return

        assert iterations > 0, 'Generation count MUST be larger than 0.'
        self.max_iterations = iterations
        print('Running Sim Non-Graphically For %i iterations.' % iterations)
        # Run manual sim
        while self.current_session_generation_count <= iterations:
            if self.frame_count > self.max_game_length and self.frame_count % 5000 == 0:
                print('Exceeded max game length... Frame count: %i' %
                      self.frame_count)
            self.do_logic()

        print('\nTraining Session Complete!')

        # Graph data
        plt.plot(self.alive_after_time)
        plt.xlabel('Alive Amount')
        plt.ylabel('Generation')
        plt.figtext(.02, .02,
                    'Depicts the amount of creatures that survived any given generation.')
        plt.legend()
        plt.show()

        plt.plot(self.generational_fitnesses, label='Generational Fitnesses')
        plt.xlabel('Max Generational Fitness')
        plt.ylabel('Generation')
        plt.figtext(.02, .02,
                    'Depicts the highest scoring creature per generation.')
        plt.legend()
        plt.show()

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
