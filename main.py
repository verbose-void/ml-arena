from environments.environment import *
from environments.balancing_environment import *
from environments.freeplay_environment import *

from util.match_up import *
from actors.pawns.pawn import *
from actors.actions import *
from controllers.controller import *
from controllers.player_controller import *

import util.stat_biases as stat_biases

EXIT_STR = 'exit'


def spacer():
    print('\n\n\n\n\n\n\n\n\n\n\n')


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

        if choice in acceptable:
            return choice

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
    p1_stat_choice = biases[p1_stat_choice]

    # P2 stat bias choice
    p2_stat_choice = get_str_choice(
        'P2 bias choice', *biases.keys())
    p2_stat_choice = biases[p2_stat_choice]

    concurrent = get_int_choice(
        'How many concurrent matches?', min_range=1, max_range=250)

    # Build matchups
    for _ in range(concurrent):
        # TODO
        pass


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


def build_player_pawn():
    pawn = Pawn()
    pawn.set_controller(PlayerController)
    return pawn


biases = {
    'normal': stat_biases.Normal,
    'short': stat_biases.ShortRanged,
    'long': stat_biases.LongRanged
}

pawn_types = {
    'brainless': Pawn,
    'player': build_player_pawn
}

if __name__ == '__main__':
    spacer()
    # Get choice of simulation
    choice = get_str_choice(
        'What simulation would you like to run?', 'freeplay', 'balance')

    env = None

    if choice == 'balance':
        env = build_balancing_environment()

    if choice == 'freeplay':
        env = build_freeplay_environment()

    assert env != None, 'Environment CANNOT be NoneType.'
    env.run()
