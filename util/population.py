from typing import List
from util.evolutionary_neural_network import *
from controllers.creature_controller import *
from actors.pawns.fitness_pawn import *
from util.match_up import *

import math
import random


def generate_random_networks(size) -> List[EvoNeuralNetwork]:
    out = []

    for i in range(size):
        out.append(
            EvoNeuralNetwork(NETWORK_DIMENSIONS)
        )

    return out


class Population:
    neural_networks = List[EvoNeuralNetwork]
    creatures_to_nets: dict
    opponent_factory: Callable = None

    def __init__(self, networks: List[EvoNeuralNetwork]):
        self.neural_networks = networks
        self.generate_creatures()

    def __init__(self, size: int):
        self.neural_networks = generate_random_networks(size)
        self.generate_creatures()

    def set_opponent_factory(self, factory: Callable):
        self.opponent_factory = factory

    def get(self, i: int) -> EvoNeuralNetwork:
        """Returns the neural network at the given index."""
        return self.neural_networks[i]

    def get_network(self, creature: FitnessPawn):
        return self.creatures_to_nets[creature]

    def best_network(self) -> EvoNeuralNetwork:
        best = None
        best_fit = float('-inf')

        for pawn in self.creatures_to_nets.keys():
            fit = pawn.calculate_fitness()
            if fit > best_fit:
                best_fit = fit
                best = self.creatures_to_nets[pawn]

        return best

    def pick_random(self) -> EvoNeuralNetwork:
        fitness_sum = 1

        for pawn in self.creatures_to_nets.keys():
            fitness_sum += pawn.calculate_fitness()

        r = random.randrange(start=0, stop=math.floor(fitness_sum))
        running_sum = 1

        for pawn in self.creatures_to_nets.keys():
            running_sum += pawn.calculate_fitness()
            if r < running_sum:
                return self.creatures_to_nets[pawn]

        raise Exception('This shouldn\'t be possible..')

    def size(self):
        return len(self.neural_networks)

    def build_match_ups(self):
        """Converts the current creature set into a set of MatchUps"""
        match_ups: Set[MatchUp] = set()

        for creature_pawn in self.creatures_to_nets.keys():
            match_ups.add(
                MatchUp(
                    creature_pawn,
                    self.opponent_factory()
                )
            )

        return match_ups

    def generate_creatures(self):
        """Generates creatures that use the current Neural Network set."""
        self.creatures_to_nets = dict()

        for neural_network in self.neural_networks:
            # Create a new creature for this Neural Network.
            new_creature = FitnessPawn()
            new_creature.set_controller(
                CreatureController(
                    new_creature,
                    neural_network
                )
            )

            # Put back into dict.
            self.creatures_to_nets[new_creature] = neural_network

    def natural_selection(self):
        """Uses natural selection to alter the current Neural Network population."""
        # Get best net without any mutations
        new_nets = [self.best_network()]

        for i in range(len(self.neural_networks)-1):
            new_net = None
            random_clone = self.pick_random().clone()

            if i < self.size() / 2:
                new_net = random_clone
            else:
                new_net = random_clone.crossover(
                    self.pick_random().clone())

            # Mutate & Reset Neural Network
            new_net.mutate(0.1)
            new_nets.append(new_net)

        self.neural_networks = new_nets
