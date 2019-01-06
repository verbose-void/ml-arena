import arcade
from test.goal import *
from test.genome_population import *
import time

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

MAX_TIME = 15  # seconds


class PathEnvironment(arcade.Window):
    goal: Goal
    population: GenomePopulation
    start_time: float = 0

    frame_count = 0
    print_str = ''
    best_genome = None

    def __init__(self, goal: Goal, population: GenomePopulation):
        self.goal = goal
        self.population = population
        arcade.set_background_color(arcade.color.BLACK)
        start_time = time.time()
        return super().__init__(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)

    def reset(self):
        self.frame_count = 0
        self.start_time = time.time()
        self.population.generation += 1

        self.population.natural_selection()

        for genome in self.population.genomes:
            genome.reset()

    def on_update(self, delta_time):
        self.frame_count += 1
        if time.time() - self.start_time >= MAX_TIME:
            return self.reset()

        if self.frame_count % 60 == 0:
            self.print_str = str(self)
            self.best_genome = self.population.best()

        for genome in self.population.genomes:
            genome.on_update(self.goal)
            pos = genome.pos
            if pos[0] < 0 or pos[0] > SCREEN_WIDTH or pos[1] > SCREEN_HEIGHT or pos[1] < 0:
                genome.kill()
        return super().on_update(delta_time)

    def on_draw(self):
        arcade.start_render()
        genome: Genome

        for genome in self.population.genomes:
            genome.on_draw()

        self.goal.on_draw()

        if self.best_genome is not None:
            self.best_genome.draw_weights()
            self.best_genome.draw_neurons()

        arcade.draw_text(self.print_str, 0, SCREEN_HEIGHT -
                         20, arcade.color.WHITE)
        return super().on_draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.BACKSPACE:
            self.reset()

        elif symbol == arcade.key.ESCAPE:
            self.goal.randomize(SCREEN_WIDTH, SCREEN_HEIGHT)

    def count_alive(self):
        c = 0
        for genome in self.population.genomes:
            if not genome.is_dead:
                c += 1
        return c

    def __str__(self):
        winners = 0

        for genome in self.population.genomes:
            if genome.won:
                winners += 1

        return 'Gen: %i Time: %.1f/%.1fs Alive: %i/%i Winners: %i' % (
            self.population.generation,
            time.time() - self.start_time,
            MAX_TIME,
            self.count_alive(),
            self.population.size(),
            winners
        )
