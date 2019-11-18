from __future__ import print_function
import pickle       # pip install cloudpickle
import os
import sys

from game import ConnectFour
import agents

from utilities import pickMove, pickAndMakeMove

game = ConnectFour()
if sys.argv > 2:
    with open(sys.argv[1], 'rb') as output:
        opponent = pickle.load(f)
else:
    opponent = agents.RandomAgent()

while not game.isFinished():
    if game.isOurTurn():
        print(game)
        possibles = game.possibleMoves()
        column = input("Which column {}?".format(possibles))
        try:
            game.playMove(column)
        except e:
            print("error occurred", e)
    else:
        column = pickMove(opponent, state)
        try:
            pickAndMakeMove(game, opponent)
        except e:
            print("AI chose invalid move, trying random")
            pickAndMakeMove(game, agents.RandomAgent())
    print(game)
