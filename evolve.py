from actors import pawn as pawn_actor
from models import evo_neuro_brain as en_brain
from models import evolutionary_neural_net as enn
import environment
import arcade
import random
import numpy as np
import os
import math

POP_SIZE = 200
AUTO_SAVE_INTERVAL = 10  # Every 10 generations, force save.
assert POP_SIZE % 2 == 0, "Population size MUST be even."

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
    print("Training Gen " + str(env.current_gen))
    if env.current_gen % AUTO_SAVE_INTERVAL == 0:
        save_data(env, force=True)


def on_end(env):
    # Save training data to file & end.

    save_data(env)


def save_data(env, force=False):
    if force or input("Would you like to save this population? (y/n): ") == "y":
        for i, pawn in enumerate(env.pop):
            pawn.brain.nn.save_to_file(env.pop_name + "/" + str(i))

    print("Save Successful.")


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
    new_pop = [best_pawn().reset()]  # Get best net without any mutations

    # Natural selection (50% pop size)
    for i in range(POP_SIZE-1):
        nn = None

        if i < POP_SIZE / 2:
            nn = env.pop[i].brain.nn.clone()
        else:
            nn = env.pop[i].brain.nn.clone().crossover(
                random_pawn().brain.nn.clone())

        pawn = create_pawn(nn.mutate(0.05))
        pawn.set_env(env)
        new_pop.append(pawn)

    return new_pop


def reset_matchups(env):
    new_match_ups = []

    for i in range(0, len(env.pop), 2):
        new_match_ups.append([
            env.pop[i],
            env.pop[i+1]
        ])

    for i, mu in enumerate(new_match_ups):
        for pawn in mu:
            pawn.match_index = i
            pawn.set_env(env)
            env.match_up_data[i]["dead_pawns"].clear()
            env.match_up_data[i]["starting"][pawn] = (
                pawn.get_pos(), pawn.get_dir())

    assert len(env.match_ups) == len(new_match_ups), (
        "New match ups are " + str(len(new_match_ups)) +
        "| Old match ups are " + str(len(env.match_ups)))

    env.match_ups.clear()
    env.match_ups = new_match_ups


def run_matches(pop_name):
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
    env.pop_name = pop_name
    env.on_end = on_end
    arcade.run()


def save_population(env, containing_folder):
    pop = env.pop

    for i, pawn in enumerate(pop):
        pawn.brain.nn.save_to_file(containing_folder + "/" + str(i) + ".txt")

    print("Finished saving population.")


def load_population(containing_folder):
    loaded = []

    for filename in os.listdir(containing_folder):
        if filename.endswith(".npy"):
            print(filename)
            loaded.append(create_pawn(
                enn.load_from_file(containing_folder + "/" + filename)
            ))

    return loaded


if __name__ == "__main__":
    resp = input("Would you like to load a population? (y/n): ")
    pop_name = None

    if resp == "y":
        pop_name = input(
            "What is the name of the population?: ")

        if(os.path.isdir(direc)):
            pop = load_population(direc)
        else:
            print("Loading failed. Direcotry \'" +
                  direc + "\' does not exist.")
            exit()
    else:
        pop_name = input(
            "Ok, what would you like to name this new population?: ")

    generate_random_population()
    run_matches(pop_name)
