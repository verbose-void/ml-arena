from environments.environment import *
from environments.balancing_environment import *
from environments.freeplay_environment import *
from environments.evolution_environment import *
from environments.adversarial_evolution_environment import *

from util.match_up import *
from util.population import *
from actors.pawns.pawn import *
from actors.actions import *
from controllers.controller import *
from controllers.player_controller import *
from controllers.dynamic_controller import *
from controllers.creature_controller import *

from typing import Callable, Set

import util.stat_biases as stat_biases

EXIT_STR = 'exit'


def spacer():
    print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')


def get_str_choice(i_prompt, *acceptable):
    acceptable = set(acceptable)

    prompt = '\n---------------------------\n'
    prompt += i_prompt + '\n'
    prompt += 'Choices: '

    for acc in acceptable:
        prompt += acc + ', '

    prompt += 'or exit'
    prompt += '\nChoice: '

    while True:
        choice = input(prompt)
        spacer()

        for potential in acceptable:
            if potential.startswith(choice):
                return potential

        if choice == EXIT_STR:
            print('Exiting...')
            exit()

        print('\nInvalid choice %s.' % choice)


def get_int_choice(i_prompt, min_range: int = 0, max_range: int = 10):
    prompt = '\n---------------------------\n'
    prompt += i_prompt + '\n'
    prompt += 'Choices: %i-%i or %s' % (min_range, max_range, EXIT_STR)
    prompt += '\nChoice: '

    while True:
        choice = input(prompt)
        spacer()

        if choice == EXIT_STR:
            print('Exiting...')
            exit()

        try:
            choice = int(choice)
        except:
            print('\nInvalid choice. MUST be an integer.')
            continue

        if choice >= min_range and choice <= max_range:
            return choice

        print('\nInvalid choice. Must be between %i and %i' %
              (min_range, max_range))


def build_balancing_environment():
    # P1 stat bias choice
    p1_stat_choice = get_str_choice(
        'P1 bias choice', *biases.keys())
    p1_stat_choice = biases[p1_stat_choice]()

    # P2 stat bias choice
    p2_stat_choice = get_str_choice(
        'P2 bias choice', *biases.keys())
    p2_stat_choice = biases[p2_stat_choice]()

    concurrent = get_int_choice(
        'How many concurrent matches?', min_range=1, max_range=250)

    match_ups = []

    # Build matchups
    for _ in range(concurrent):
        match_ups.append(
            MatchUp(
                build_dynamic_pawn(p1_stat_choice),
                build_dynamic_pawn(p2_stat_choice)
            )
        )

    return BalancingEnvironment(*match_ups)


def build_freeplay_environment():
    # P1 type choice
    p1_pawn = get_str_choice(
        'P1 type', *pawn_types.keys())
    p1_pawn = pawn_types[p1_pawn]()

    # P2 type choice
    p2_pawn = get_str_choice(
        'P2 type', *pawn_types.keys())
    p2_pawn = pawn_types[p2_pawn]()

    match_up = MatchUp(p1_pawn, p2_pawn)
    return FreeplayEnvironment(match_up)


def get_genome_to_load():
    if len(Population.get_valid_populations()) < 1:
        print('No populations exist.')
        return None

    print(Population.list_all_saved())

    while True:
        name = input('Choice (or exit): ')

        if name == EXIT_STR:
            print('Exiting...')
            exit()

        if Population.is_valid_population_directory(name):
            break
        else:
            print('\nInvalid choice.\n')

    path = os.path.join(POPULATION_DIRECTORY, name)

    genome_number = get_int_choice(
        'Which genome would you like to sample?',
        min_range=0,
        max_range=len(os.listdir(path))-2
    )

    return NeuralNetwork.load_from_file(os.path.join(path, '%i.npy' % genome_number))


def get_population_to_load(prompt: str):
    if len(Population.get_valid_populations()) < 1:
        print('No populations exist.')
        return None

    if get_str_choice(prompt, 'yes', 'no') == 'no':
        return None

    print(Population.list_all_saved())

    while True:
        name = input('Choice (or exit): ')

        if name == EXIT_STR:
            print('Exiting...')
            exit()

        if Population.is_valid_population_directory(name):
            break
        else:
            print('\nInvalid choice.\n')

    return Population.load_from_dir(name)


def build_evolution_environment():
    sim_type = get_str_choice('Training Type?', 'adversarial', 'other')

    if sim_type == 'other':

        population = get_population_to_load('Load from file?')

        if population == None:
            size = get_int_choice(
                'New Population Size?', min_range=1, max_range=250
            )

            population = Population(input('New Population Name?: '), size=size)

        against = get_str_choice(
            'Training Opponent', *training_opponent_types.keys()
        )

        population.set_opponent_factory(training_opponent_types[against])
        return EvolutionEnvironment(population)

    population1 = get_population_to_load('Load first population from file?')
    size = -1

    if population1 == None:
        size = get_int_choice(
            'Population Size?', min_range=1, max_range=125
        )

        population1 = Population(input('First Population Name?: '), size=size)

    population2 = get_population_to_load('Load second population from file?')

    if population2 == None:
        spacer()
        population2 = Population(
            input('Second Population Name?: '), size=population1.size())

    if population1.size() != population2.size():
        print('\n\nPopulation sizes MUST be the same.')
        exit()

    return AdversarialEvolutionEnvironment(population1, population2)


def build_player_pawn():
    pawn = Pawn()
    pawn.set_controller(PlayerController)
    return pawn


def build_dynamic_pawn(stat_bias=None):
    pawn = Pawn()

    if stat_bias != None:
        pawn.set_stat_bias(stat_bias)

    pawn.set_controller(DynamicController)
    return pawn


def build_genome_pawn():
    pawn = Pawn()
    controller = CreatureController(
        pawn,
        get_genome_to_load()
    )

    pawn.set_controller(controller)
    return pawn


biases = {
    'normal': stat_biases.Normal,
    'short': stat_biases.ShortRanged,
    'long': stat_biases.LongRanged
}

pawn_types = {
    'brainless': Pawn,
    'player': build_player_pawn,
    'dynamic': build_dynamic_pawn,
    'genome': build_genome_pawn
}

training_opponent_types = {
    'brainless': Pawn,
    'dynamic': build_dynamic_pawn
}

if __name__ == '__main__':
    spacer()
    # Get choice of simulation
    choice = get_str_choice(
        'What simulation would you like to run?', 'freeplay', 'balance', 'evolution')

    env = None

    if choice == 'balance':
        env = build_balancing_environment()

    if choice == 'freeplay':
        env = build_freeplay_environment()

    if choice == 'evolution':
        env = build_evolution_environment()

    assert env != None, 'Environment CANNOT be NoneType.'
    env.run()
