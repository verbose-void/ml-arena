from environments.environment import *
from util.population import *


class EvolutionEnvironment(Environment):
    population1: Population
    current_session_generation_count = 0
    max_iterations = None

    def __init__(self, population1: Population):
        self.population1 = population1
        self.reset(build_new_gen=False)
        super().__init__(*self.match_ups)

    def reset(self, build_new_gen=True):
        pop = self.population1

        if build_new_gen:

            # Verbose
            print()
            print('Building new population...')
            print('Current Iteration: %i/%i (%.1f' % (
                self.current_session_generation_count,
                self.max_iterations,
                self.current_session_generation_count/self.max_iterations*100
            ) + '%' + ' complete!)')
            if self.all_dead:
                dr = 'All Dead'
            else:
                c = self.running_matches_count()
                l = len(self.match_ups)
                dr = 'Time Limit Reached. Alive: %i/%i' % (
                    c,
                    l
                )

                dr += ' (%.1f' % (c/l*100) + '%' + ')'
            g = 'Generation: %i' % pop.current_gen
            try:
                g += '-' % self.population2.current_gen
            except:
                pass
            print(g)
            print('Termination Reason: %s' % dr)
            print('Max Overall Fitness: %i' % self.absolute_max_fitness)
            print('Generational Max Fitness: %i' %
                  self.current_gen_max_fitness)

            self.current_session_generation_count += 1
            if pop.current_gen > 0 and pop.current_gen % 5 == 0:
                pop.save_to_dir()

            pop.natural_selection()
            pop.generate_creatures()
            pop.current_gen += 1
            super().reset()

        self.match_ups = pop.build_match_ups()
        self.calculate_best_match_up()

    def run(self, generations=10):
        res = Environment.run(self)
        if res:
            return

        assert generations > 0, 'Generation count MUST be larger than 0.'
        self.max_iterations = generations
        print('Running Sim Non-Graphically For %i Generations.' % generations)
        # Run manual sim
        while self.current_session_generation_count <= generations:
            if self.frame_count > self.max_game_length and self.frame_count % 5000 == 0:
                print('Exceeded max game length... Frame count: %i' %
                      self.frame_count)
            self.do_logic()

        print('\nTraining Session Complete!')

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
