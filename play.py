from __future__ import print_function
import pickle       # pip install cloudpickle
import os
import sys

from game import ConnectFour
import agents

from utilities import pickMove, pickAndMakeMove

game = ConnectFour()
if len(sys.argv) >= 2:
    print("Using opponent from {}".format(sys.argv[1]))
    with open(sys.argv[1], 'rb') as output:
        opponent = pickle.load(output)
else:
    print("Using random agent")
    opponent = agents.RandomAgent()

while not game.isFinished():
    if game.isOurTurn():
        print(game)
        possibles = game.possibleMoves()
        column = input("Which column {}? ".format(possibles))
        try:
            game.playMove(int(column))
        except Exception as e:
            print("error occurred", e)
    else:
        try:
            pickAndMakeMove(game, opponent)
        except Exception:
            print("AI chose invalid move, trying random")
            pickAndMakeMove(game, agents.RandomAgent())
print(game)
