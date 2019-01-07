from util.neural_network import *
import random
import numpy as np
from typing import Tuple


class EvoNeuralNetwork(NeuralNetwork):
    def crossover(self, other: 'EvoNeuralNetwork') -> Tuple['EvoNeuralNetwork']:
        child1_layers = []
        child2_layers = []

        parentA_layer: np.ndarray
        for i, parentA_layer in enumerate(self.layer_weights):
            parentB_layer = other.layer_weights[i]
            rows = len(parentA_layer)
            cols = len(parentA_layer[0])

            cutoff = (
                np.random.randint(0, high=rows),
                np.random.randint(0, high=cols)
            )

            child1_layer = np.zeros((rows, cols))
            child2_layer = np.zeros((rows, cols))

            for j in range(rows):
                for k in range(cols):

                    # This will copy all nodes from parent 1 until the cutoff is reached,
                    # then it will switch over to parent 2.
                    # does this for both children, which will effectively have the inverse of
                    # each other's genes with respect to the parents.

                    if j < cutoff[0] or (j == cutoff[0] and k <= cutoff[1]):
                        child1_layer[j, k] = parentA_layer[j, k]
                        child2_layer[j, k] = parentB_layer[j, k]
                    else:
                        child1_layer[j, k] = parentB_layer[j, k]
                        child2_layer[j, k] = parentA_layer[j, k]

            child1_layers.append(child1_layer)
            child2_layers.append(child2_layer)

        return (
            EvoNeuralNetwork(layer_weights=child1_layers),
            EvoNeuralNetwork(layer_weights=child2_layers)
        )

    def clone(self):
        copied_weights = []

        for layer in self.layer_weights:
            copied_weights.append(np.copy(layer))

        out = EvoNeuralNetwork(
            layer_weights=copied_weights
        )

        return out

    def mutate(self, mutation_rate=0.1):
        for layer in self.layer_weights:
            for x in np.nditer(layer, op_flags=['readwrite']):
                if random.random() < mutation_rate:
                    ox = float(x)
                    nx = x + np.random.normal(loc=0, scale=0.1)
                    x[...] = min(1, max(-1, nx))
        return self

    def load_from_file(path: str):
        return EvoNeuralNetwork(layer_weights=NeuralNetwork.load_from_file(path).layer_weights)
