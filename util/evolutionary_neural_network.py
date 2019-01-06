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

            for i in range(rows):
                for j in range(cols):

                    # This will copy all nodes from parent 1 until the cutoff is reached,
                    # then it will switch over to parent 2.
                    # does this for both children, which will effectively have the inverse of
                    # each other's genes with respect to the parents.

                    if i < cutoff[0] or (i == cutoff[0] and j <= cutoff[1]):
                        child1_layer[i, j] = parentA_layer[i, j]
                        child2_layer[i, j] = parentB_layer[i, j]
                    else:
                        child1_layer[i, j] = parentB_layer[i, j]
                        child2_layer[i, j] = parentA_layer[i, j]

            child1_layers.append(child1_layer)
            child2_layers.append(child2_layer)

        return (
            EvoNeuralNetwork(layer_weights=child1_layers),
            EvoNeuralNetwork(layer_weights=child2_layers)
        )

    def clone(self):
        return EvoNeuralNetwork(
            layer_weights=np.copy(self.layer_weights)
        )

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
