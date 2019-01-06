import arcade
from util.evolutionary_neural_network import *
from test.goal import *

THRESHOLD = 0.7


class Genome(EvoNeuralNetwork):
    input_neuron_labels = [
        'Angle To Goal',
        'Bias'
    ]

    output_neuron_labels = [
        'LEFT',
        'RIGHT',
        'UP',
        'DOWN'
    ]

    start_pos: tuple
    pos: list
    vel: list
    speed = 2
    radius = 8

    goal: Goal = None
    dist_traveled = 0

    is_dead = False
    won = False

    input_values: list
    output_values: list

    def __init__(self, start_x, start_y, network=None):
        if network != None:
            self.__dict__ = network.__dict__

        self.start_pos = (start_x, start_y)
        self.pos = list(self.start_pos)
        super().__init__((1, 4))

    def reset(self):
        self.pos = list(self.start_pos)
        self.is_dead = False
        self.won = False

    def at_goal(self):
        return self.dist_to_goal() <= self.goal.radius + self.radius

    def max_dist_to_goal(self):
        return math.sqrt((self.goal.pos[0] - self.start_pos[0]) ** 2 +
                         (self.goal.pos[1] - self.start_pos[1]) ** 2)

    def dist_to_goal(self):
        return math.sqrt((self.goal.pos[0] - self.pos[0]) ** 2 +
                         (self.goal.pos[1] - self.pos[1]) ** 2)

    def on_draw(self):
        color = arcade.color.WHITE

        if self.is_dead:
            color = arcade.color.RED
        elif self.won:
            color = arcade.color.GREEN

        arcade.draw_circle_filled(
            self.pos[0], self.pos[1], self.radius, color
        )

        arcade.draw_text(
            str(round(self.calculate_fitness())),
            self.pos[0], self.pos[1],
            arcade.color.RED,
            align='center',
            anchor_x='center',
            anchor_y='center',
            font_size=10
        )

    def clone(self):
        return Genome(self.start_pos[0], self.start_pos[1], super().clone())

    def crossover(self, other: 'Genome'):
        nets = super().crossover(other)
        return (
            Genome(self.start_pos[0], self.start_pos[1], nets[0]),
            Genome(self.start_pos[0], self.start_pos[1], nets[1])
        )

    def on_update(self, goal: Goal):
        self.goal = goal

        if self.at_goal():
            self.won = True

        if self.is_dead or self.won:
            return

        self.look()
        self.think()
        self.act()

        prev_pos = list(self.pos)

        self.pos[0] += self.vel[0] * self.speed
        self.pos[1] += self.vel[1] * self.speed

        self.dist_traveled += (prev_pos[0] - self.pos[0]
                               ) ** 2 + (prev_pos[1] - self.pos[1]) ** 2

    def calculate_fitness(self):
        if self.goal is None:
            return 0
        fit = self.max_dist_to_goal() / self.dist_to_goal()

        if self.won:
            fit *= 2.5

        return fit

    def kill(self):
        self.is_dead = True

    def look(self):
        # Get the angle to the goal.

        position = self.goal.pos

        vec = (
            self.pos[0] - position[0],
            self.pos[1] - position[1]
        )

        d = math.atan2(vec[1], vec[0]) + (math.pi)

        if d < 0:
            # Convert to [0, 2pi] range
            d = math.pi + (-d)

        self.input_values = [d/(2*math.pi)]

    def think(self):
        self.output_values = self.output(self.input_values)

    def act(self):
        # 0 = left
        # 1 = right
        # 2 = up
        # 4 = down

        new_vel = [0, 0]

        # Left
        if self.output_values[0] > THRESHOLD:
            new_vel[0] = -1

        # Right
        elif self.output_values[1] > THRESHOLD:
            new_vel[0] = 1

        # Up
        if self.output_values[2] > THRESHOLD:
            new_vel[1] = 1

        # Down
        elif self.output_values[3] > THRESHOLD:
            new_vel[1] = -1

        self.vel = new_vel
