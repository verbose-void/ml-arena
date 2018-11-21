from actors import pawn as pawn_actor
from models import evo_neuro_brain as en_brain
from models import evolutionary_neural_net as enn
import environment
import arcade
import random
import numpy as np
import os
import math

AUTO_SAVE_INTERVAL = 10  # Every 10 generations, force save.

INPUT_NODE_COUNT = 19
HIDDEN_NODE_COUNT = 40
OUTPUT_NODE_COUNT = 9

TRAINING_DIR = "training_data"


def create_pawn(nn):
    brain = en_brain.NEBrain(nn)
    pawn = pawn_actor.Pawn(brain,
                           random.random() * environment.SCREEN_WIDTH,
                           random.random() * environment.SCREEN_HEIGHT)
    brain.set_pawn(pawn)
    return pawn


def generate_random_population(size):
    assert size % 2 == 0, "Population size MUST be even."
    assert size > 0, "Population size MUST be positive."

    out = []

    # Generate initial population
    for i in range(size):
        pawn = create_pawn(enn.EvolutionaryNN(
            INPUT_NODE_COUNT, HIDDEN_NODE_COUNT, OUTPUT_NODE_COUNT))
        out.append(pawn)

    return out


def on_restart(env):
    """
    This method is called when all current match ups have completed.
    """

    env.pop = natural_selection(env)
    env.match_ups = convert_pop_to_match_ups(
        env.pop, env.training_type, env=env)
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


def random_pawn(env):
    """
    Randomly select a pawn from the population. (fitness is taken into consideration)
    """

    fitness_sum = 1

    for pawn in env.pop:
        fitness_sum += pawn.calculate_fitness()

    r = random.randrange(start=0, stop=math.floor(fitness_sum))

    running_sum = 0

    for pawn in env.pop:
        running_sum += pawn.calculate_fitness()
        if r < running_sum:
            return pawn

    return env.pop[0]


def natural_selection(env):
    new_pop = [best_pawn().reset()]  # Get best net without any mutations

    for i in range(env.pop_size-1):
        nn = None

        if i < env.pop_size / 2:
            nn = random_pawn(env).brain.nn.clone()
        else:
            nn = random_pawn(env).brain.nn.clone().crossover(
                random_pawn(env).brain.nn.clone())

        pawn = create_pawn(nn.mutate(0.1))
        pawn.set_env(env)
        new_pop.append(pawn)

    return new_pop


def convert_pop_to_match_ups(pop, training_type, env=None):
    out = []

    if training_type == "self":
        for i in range(0, size, 2):
            pop[i] = pop[i].reset()
            p1 = pop[i]
            p1.match_index = math.floor(i/2)

            pop[i+1] = pop[i+1].reset()
            p2 = pop[i+1]
            p2.match_index = math.floor(i/2)

            out.append([
                p1,
                p2
            ])
    else:
        for i in range(size):
            pop[i] = pop[i].reset()
            p1 = pop[i]
            p1.match_index = i

            p2 = environment.dynamic_scripting_pawn(
                random.random() * environment.SCREEN_WIDTH,
                random.random() * environment.SCREEN_HEIGHT
            )
            p2.match_index = i

            if env != None:
                p2.env = env

            out.append([
                p1,
                p2
            ])

    return out


def run_matches(pop, pop_name, size, training_type):
    match_ups = convert_pop_to_match_ups(pop, training_type)
    env = environment.Environment(*match_ups)
    env.training_type = training_type
    env.on_restart = on_restart
    env.pop_size = size
    env.pop = pop
    env.pop_name = pop_name
    env.on_end = on_end
    arcade.run()


def load_population(containing_folder):
    loaded = []

    for filename in os.listdir(containing_folder):
        if filename.endswith(".npy"):
            print("Loading %s..." % filename)
            loaded.append(create_pawn(
                enn.load_from_file(containing_folder + "/" + filename)
            ))

    return loaded


if __name__ == "__main__":
    existing_data = []

    if os.path.isdir(TRAINING_DIR):
        for f in os.listdir(TRAINING_DIR):
            if os.path.isdir(TRAINING_DIR + "/" + f):
                existing_data.append(f)

    resp = "n"

    print("")
    print("---------------------------------------------------------")
    if len(existing_data) > 0:
        print("There are currently %i existing populations." %
              len(existing_data))
        resp = input("Would you like to load one? (y/n): ")

        if resp == "no":
            print("Ok, let's generate a new one.")
        else:
            print("---------------------------------------------------------")
    else:
        print("No populations currently exist, let's generate a new one.")
        print("---------------------------------------------------------")

    pop_name = None

    if resp == "y":
        print("")
        print("----------------------")
        print("Available populations:")
        for p in existing_data:
            print(p)

        print("----------------------")
        print("")

        pop_name = input(
            "Which one?: ")

        if(os.path.isdir(TRAINING_DIR + "/" + pop_name)):
            pop = load_population(TRAINING_DIR + "/" + pop_name)
            size = len(pop)
        else:
            print("Loading failed. Direcotry \'" +
                  direc + "\' does not exist.")
            exit()
    else:
        print("")
        print("---------------------------------------------------------")
        pop_name = TRAINING_DIR + "/" + input(
            "What should we name it?: ")
        size = int(input("How many agents per generation? (even int): "))
        print("---------------------------------------------------------")
        pop = generate_random_population(size)

    print("")
    print("---------------------------------------------------------")
    print("How would you like to train it?")
    print("Types: [dynamic, self]")
    training_type = input("Choice: ")

    if training_type != "dynamic" and training_type != "self":
        print("")
        print("Invalid Training Type.")
        print("")
        exit()

    print("")
    print("")
    print("-----------------------------------------------")
    print("")
    print("            Beginning Simulation...            ")
    print("")
    print("-----------------------------------------------")
    print("")
    print("")
    run_matches(pop, pop_name, size, training_type)
