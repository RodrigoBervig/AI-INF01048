from hashlib import new


class State:

    def __init__(self, state):
        self.state = state

    def swap(self, pos1, pos2):
        new_state = list(self.state)
        temp = new_state[pos1]
        new_state[pos1] = new_state[pos2]
        new_state[pos2] = temp
        return "".join(new_state)

    def transition(self, action, index):
        if action == "esquerda":
            return State(self.swap(index, index-1))
        if action == "direita":
            return State(self.swap(index, index + 1))
        if action == "cima":
            return State(self.swap(index, index - 3))
        return State(self.swap(index, index + 3))
