def pickAndMakeMove(game, agent):
    state = game.state()
    index = pickMove(agent, state)
    game.playMove(index)

def pickMove(agent, state):
    output = agent.activate(state)
    return sorted(range(len(output)), key=lambda x: output[x])[-1]

