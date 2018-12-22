from controllers.controller import *
from actors.pawns.pawn import *
from util.neural_network import *
from util.match_up import *
from actors.actions import *

# Reason for redefinition: __dict__ is not constant ordering
ACTION_LIST = [
    Actions.MOVE_LEFT,
    Actions.MOVE_RIGHT,
    Actions.MOVE_UP,
    Actions.MOVE_DOWN,

    Actions.LOOK_LEFT,
    Actions.LOOK_RIGHT,

    Actions.USE_SHIELD,

    Actions.LONG_ATTACK,
    Actions.SHORT_ATTACK
]

NETWORK_DIMENSIONS = (
    5,
    7,
    len(ACTION_LIST)
)


class CreatureController(Controller):

    pawn: Pawn
    neural_network: NeuralNetwork

    inputs: list
    outputs: list

    def __init__(self, pawn: Pawn, neural_network=None):
        super().__init__(pawn)
        self.pawn = pawn

        if neural_network == None:

            self.neural_network = NeuralNetwork(NETWORK_DIMENSIONS)

        else:
            self.neural_network = neural_network

    def look(self, match_up: MatchUp):
        """Create neural net inputs"""
        p: Pawn = self.pawn

        imminent: Laser = match_up.get_most_imminent_laser(p)
        enemy: Pawn = match_up.get_closest_opponent(p)

        max_angle = math.pi * 2

        self.inputs = [
            1/math.sqrt(p.dist_squared(actor=imminent)
                        ) if imminent != None else 1,
            p.angle_to(actor=imminent)/max_angle if imminent != None else 1,

            1/math.sqrt(p.dist_squared(actor=enemy)) if enemy != None else 1,
            p.angle_to(actor=enemy)/max_angle if enemy != None else 1,

            p.get_direc()/max_angle
        ]

    def think(self):
        self.outputs = self.neural_network.output(self.inputs)

    def act(self):
        """React to neural network outputs"""
        for i, action in enumerate(ACTION_LIST):
            if self.outputs[i] > REACTION_THRESHOLD:
                self.submit_action(action)
            else:
                self.undo_action(action)
