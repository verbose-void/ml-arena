import numpy as np
import math
import random
import arcade
from typing import List, Tuple
from environments.environment import *

NEURON_DIST = 70
VERBOSE_NEURON_SPACING_X = 70
VERBOSE_NEURON_SPACING_Y = 26
VERBOSE_NEURON_RADIUS = 12
VERBOSE_NEURON_TEXT_SIZE = 12
VERBOSE_MAX_SYNAPSE_WEIGHT = 5


class NeuralNetwork:
    layer_weights: list
    neuron_weights: list = None  # Stored here for verbose
    neuron_screen_locations: list = None

    def __init__(
        self,
        dimensions: Tuple[int] = None,
        layer_weights: list = None
    ):
        """
        Randomly initialize a Neural Network with the given dimensions.

        len(dimensions) = layer count.
        dimensions[i] = neurons at layer i.
        """

        assert dimensions or layer_weights, 'Neural Network must be initialized with either dimensions or weights'

        if dimensions:
            self.layer_weights = []
            for i in range(len(dimensions)-1):
                self.layer_weights.append(
                    np.random.uniform(
                        size=(dimensions[i], dimensions[i+1])
                    )
                )
            return

        self.layer_weights = list(layer_weights)

    def clone(self):
        return NeuralNetwork(
            layer_weights=self.layer_weights
        )

    def sigmoid(self, x, derivative=False):
        return x*(1-x) if derivative else 1/(1+np.exp(-x))

    def activate_layer(self, layer: list):
        for x in np.nditer(layer, op_flags=['readwrite']):
            x[...] = self.sigmoid(x)

    def output(self, inputs: list):
        """Calculates the output for the given inputs."""

        # Column matrix
        # inputs = np.reshape(inputs, (len(inputs), 1))

        self.neuron_weights = []
        self.neuron_weights.append(np.array((inputs)))
        output = inputs

        for weight_layer in self.layer_weights:
            output = np.matmul(output, weight_layer)
            self.activate_layer(output)
            self.neuron_weights.append(output)

        return output

    def draw_neurons(self):
        if self.neuron_weights == None:
            return

        x = SCREEN_WIDTH - len(self.neuron_weights) * VERBOSE_NEURON_SPACING_X

        self.neuron_screen_locations = []

        for i, layer in enumerate(self.neuron_weights):
            y = SCREEN_HEIGHT / 2 - \
                ((len(layer) / 2) * VERBOSE_NEURON_SPACING_Y)

            self.neuron_screen_locations.append([])

            # All weights will be normalized. Use radial representation.
            for weight in np.nditer(layer, op_flags=['readwrite']):

                self.neuron_screen_locations[i].append((x, y))

                arcade.draw_circle_filled(
                    x,
                    y,
                    VERBOSE_NEURON_RADIUS,
                    arcade.color.WHITE
                )

                arcade.draw_circle_outline(
                    x,
                    y,
                    VERBOSE_NEURON_RADIUS,
                    arcade.color.WHITE
                )

                arcade.draw_text(
                    '%.1f' % weight, x, y,
                    arcade.color.BLACK,
                    font_size=VERBOSE_NEURON_TEXT_SIZE,
                    align='center',
                    anchor_x='center',
                    anchor_y='center')

                y += VERBOSE_NEURON_SPACING_Y

            x += VERBOSE_NEURON_SPACING_X

    def draw_weights(self):
        if self.neuron_screen_locations == None:
            return

        for i, layer_weight_set in enumerate(self.layer_weights):
            layer1_neuron_locations = self.neuron_screen_locations[i]
            layer2_neuron_locations = self.neuron_screen_locations[i+1]

            for j, weight_layer in enumerate(layer_weight_set):
                neuron1 = layer1_neuron_locations[j]

                for k, weight in enumerate(layer_weight_set[j]):
                    neuron2 = layer2_neuron_locations[k]

                    arcade.draw_line(
                        neuron1[0],
                        neuron1[1],
                        neuron2[0],
                        neuron2[1],
                        arcade.color.WHITE,
                        border_width=VERBOSE_MAX_SYNAPSE_WEIGHT * weight
                    )


if __name__ == '__main__':
    nn1 = NeuralNetwork(dimensions=(5, 2, 3))
    out1 = nn1.output([1, 2, 3, 4, 5])

    nn2 = NeuralNetwork(layer_weights=nn1.layer_weights)
    out2 = nn2.output([1, 2, 3, 4, 5])

    assert np.array_equal(out1, out2), 'Outputs MUST be the same.'
