from actors import pawn as pawn_actor
from models import evo_neuro_brain as en_brain
from models import evolutionary_neural_net as enn
import environment
import arcade
import random
import numpy as np
import math

POP_SIZE = 180
assert POP_SIZE % 2 == 0, "Population size MUST be even."

GENERATIONS = 5

INPUT_NODE_COUNT = 19
HIDDEN_NODE_COUNT = 20
OUTPUT_NODE_COUNT = 9

pop = []


def create_pawn(nn):
    brain = en_brain.NEBrain(nn)
    pawn = pawn_actor.Pawn(brain,
                           random.random() * environment.SCREEN_WIDTH,
                           random.random() * environment.SCREEN_HEIGHT)
    brain.set_pawn(pawn)
    return pawn


def generate_random_population():
    # Generate initial population
    for i in range(POP_SIZE):
        pawn = create_pawn(enn.EvolutionaryNN(
            INPUT_NODE_COUNT, HIDDEN_NODE_COUNT, OUTPUT_NODE_COUNT))
        pop.append(pawn)


def on_restart(env):
    """
    This method is called when all current match ups have completed.
    """
    env.pop = natural_selection(env)
    reset_matchups(env)
    env.current_gen += 1


def on_end(env):
    # Save training data to file & end.

    response = input("Would you like to save the training data? (y/n): ")
    if response == "y":
        file_name = input("What file name should I save the data?: ")
        save_data(file_name, env)


def save_data(file_name, env):
    print("Saving data under " + file_name)
    # TODO


def best_pawn():
    best_fitness = float('-inf')
    out = None

    for pawn in pop:
        f = pawn.calculate_fitness()
        if f > best_fitness:
            best_fitness = f
            out = pawn

    return out


def random_pawn():
    """
    Randomly select a pawn from the population. (fitness is taken into consideration)
    """

    fitness_sum = 1

    for pawn in pop:
        fitness_sum += pawn.calculate_fitness()

    r = random.randrange(start=0, stop=math.floor(fitness_sum))

    running_sum = 0

    for pawn in pop:
        running_sum += pawn.calculate_fitness()
        if r < running_sum:
            return pawn

    return pop[0]


def natural_selection(env):
    new_pop = [best_pawn()]  # Get best net without any mutations

    # Natural selection (50% pop size)
    for i in range(POP_SIZE-1):
        nn = None

        if i < POP_SIZE / 2:
            nn = env.pop[i].brain.nn.clone()
        else:
            nn = env.pop[i].brain.nn.crossover(random_pawn().brain.nn)

        pawn = create_pawn(nn.mutate(0.1))
        pawn.set_env(env)
        new_pop.append(pawn)

    return new_pop


def reset_matchups(env):
    new_match_ups = []

    for i in range(0, len(pop), 2):
        new_match_ups.append([
            pop[i],
            pop[i+1]
        ])

    assert len(env.match_ups) == len(new_match_ups), (
        "New match ups are " + str(len(new_match_ups)) +
        "| Old match ups are " + str(len(env.match_ups)))

    env.match_ups.clear()
    env.match_ups = new_match_ups


def run_matches():
    match_ups = []

    for i in range(0, len(pop), 2):
        match_ups.append([
            pop[i],
            pop[i+1]
        ])

    env = environment.Environment(*match_ups)
    env.on_restart = on_restart
    env.pop_size = POP_SIZE
    env.pop = pop
    env.on_end = on_end
    arcade.run()


if __name__ == "__main__":
    generate_random_population()
    run_matches()
