from state import State
from node import Node


def sucessor(state):
    reachable = []
    index = state.state.find('_')

    if index % 3 == 0:
        reachable.append(["direita", state.transition("direita", index)])
    elif index % 3 == 2:
        reachable.append(["esquerda", state.transition("esquerda", index)])
    else:
        reachable.append(["direita", state.transition("direita", index)])
        reachable.append(["esquerda", state.transition("esquerda", index)])

    if index >= 3:
        reachable.append(["cima", state.transition("cima", index)])
    
    if index <= 5:
        reachable.append(["abaixo", state.transition("abaixo", index)])

    return reachable

