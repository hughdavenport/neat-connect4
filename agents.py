from game import ConnectFour
import random

class RandomAgent:

    def activate(self, inputs):
        game = ConnectFour._createFromState(inputs)
        possibles = game.possibleMoves()
        return [random.random() if index in possibles else 0.0 for index in range(0, 7)]

class PerfectAgent:

    def __init__(self, player):
        self._player = player

    def activate(self, inputs):
        game = ConnectFour._createFromState(inputs)
        winners = game._almostWinners()
        # FIXME TODO


class LosingAgent:

    def activate(self, inputs):
        game = ConnectFour._createFromState(inputs)
        winners = game._almostWinners()
        possibles = game.possibleMoves()
        moves = [random.random() if index in possibles and winners[index] is None else 0.0 for index in range(0, 9)]
        if moves.count(0.0) == 9:
            return [random.random() if index in possibles else 0.0 for index in range(0, 9)]
        return moves
