from state import State


class Node:

    def __init__(self, state, parent, action, cost):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost

    def __str__(self) -> str:
        return "estado: " + self.state.state + "\n" + "acao: " + self.action + "\n" + "custo: " + self.cost
