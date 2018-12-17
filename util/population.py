from typing import List
from util.neural_network import *
from controllers.creature_controller import *


def generate_random_networks(size) -> List[NeuralNetwork]:
    out = []

    for i in range(size):
        out.append(
            NeuralNetwork(
                INPUT_NODES,
                HIDDEN_NODES,
                OUTPUT_NODES
            )
        )

    return out


class Population:
    neural_networks = List[NeuralNetwork]

    def __init__(self, networks: List[NeuralNetwork]):
        self.neural_networks = networks

    def __init__(self, size: int):
        self.neural_networks = generate_random_networks(size)

    def get(self, i: int) -> NeuralNetwork:
        """Returns the neural network at the given index."""
        return self.neural_networks[i]

    def size(self):
        return len(self.neural_networks)
