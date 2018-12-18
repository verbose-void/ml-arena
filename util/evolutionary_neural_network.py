from util.neural_network import *
import random


class EvoNeuralNetwork(NeuralNetwork):
    def crossover(self, other: 'EvoNeuralNetwork'):

        child_layer_weights = []

        parentA_layer: np.ndarray
        for i, parentA_layer in enumerate(self.layer_weights):
            parentB_layer = other.layer_weights[i]
            rows = len(parentA_layer)
            cols = len(parentA_layer[0])

            cutoff = (
                np.random.randint(0, high=rows),
                np.random.randint(0, high=cols)
            )

            child_layer = np.zeros((rows, cols))

            for i in range(rows):
                for j in range(cols):

                    # This will copy all nodes from parent 1 until the cutoff is reached,
                    # then it will switch over to parent 2.

                    if i < cutoff[0] or (i == cutoff[0] and j <= cutoff[1]):
                        child_layer[i, j] = parentA_layer[i, j]
                    else:
                        child_layer[i, j] = parentB_layer[i, j]

            child_layer_weights.append(child_layer)

        return EvoNeuralNetwork(layer_weights=child_layer_weights)

    def clone(self):
        return EvoNeuralNetwork(
            layer_weights=self.layer_weights
        )

    def mutate(self, mutation_rate=0.1):
        for layer in self.layer_weights:
            for x in np.nditer(layer, op_flags=['readwrite']):
                if random.random() < mutation_rate:
                    x[...] = random.random()
