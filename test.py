import arcade
import random

from test.path_environment import *
from test.goal import *
from test.genome import *
from test.genome_population import *

# ----------------------------------------
#               Assertions
# ----------------------------------------

net1 = EvoNeuralNetwork(dimensions=(14, 14, 9))
net2 = EvoNeuralNetwork(dimensions=(14, 14, 9))

assert not np.array_equiv(
    net1, net2), 'Randomly generated networks MUST differ.'

net1_clone = net1.clone()
net2_clone = net2.clone()

assert_near_equal(net1, net1_clone)
assert_near_equal(net2, net2_clone)

inputs1 = list(np.random.randn(14))
inputs2 = list(np.copy(inputs1))

net1_outputs = np.array(net1.output(inputs1))
net1_clone_outputs = np.array(net1_clone.output(inputs2))

assert np.array_equal(net1_outputs, net1_clone_outputs), \
    'Outputs for same inputs of clones MUST be the same.'
print('Assertion passed for net clone outputs.')

net1_clone.mutate(0.5)
assert_near_equal(net1, net1_clone, inverse=True)
print('Assertion passed for mutations being made independently of clones.')

net2_children = net2.crossover(net2_clone)
assert_near_equal(net2_children[0], net2_children[1], inverse=True)
print('Assertion passed for children being different.')


W = np.array([
    [-1.58686978,  1.40257049,  0.06003039, -0.36521968],
    [-2.20114997, -0.6549252, -0.32541635, -1.12067112],
    [0.6381669,  0.48953871, -0.38381631, -1.49400033]
])

# Test outputs of networks.
net1 = EvoNeuralNetwork(
    layer_weights=[np.copy(W)]
)

Xb = np.array([[-2.14874928],
               [0.44031005],
               [0.74149018],
               [1]])  # bias

X = [-2.14874928,  # no bias
     0.44031005,
     0.74149018]

Y = np.array([-4.84501693, -1.76813063, -1.69051381])

EvoNeuralNetwork.activate_layer(Y)
Yhat = net1.output(X)
YhatActual = W.dot(Xb).flatten()
EvoNeuralNetwork.activate_layer(YhatActual)

assert np.allclose(
    YhatActual, Yhat, 0.0001), 'Fixed predictions & Lib Net predictions MUST be equal.'


# ----------------------------------------
#             End Assertions
# ----------------------------------------

START_X = SCREEN_WIDTH / 2
START_Y = SCREEN_HEIGHT / 2


def gen_genomes(amount):
    out = []
    for i in range(amount):
        out.append(Genome(START_X, START_Y))
    return out


goal = Goal()
goal.randomize(SCREEN_WIDTH, SCREEN_HEIGHT)

env = PathEnvironment(
    goal,
    GenomePopulation(
        *gen_genomes(100)
    )
)

arcade.run()

# parentA = EvoNeuralNetwork((3, 1))
# parentB = EvoNeuralNetwork((3, 1))

# children = parentA.crossover(parentB)
# print()
# print(parentA.layer_weights)
# print()
# print(parentB.layer_weights)
# print()
# print(children[0].layer_weights)
# print()
# print(children[1].layer_weights)
