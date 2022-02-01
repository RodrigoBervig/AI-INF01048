from node import Nodo


def sucessor(state: str) -> list[tuple]:
    reachable = []
    index = state.find('_')

    # indexes:
    # _____________
    # | 0 | 1 | 2 |
    # | 3 | 4 | 5 |
    # | 6 | 7 | 8 |
    # -------------

    if index % 3 <= 1:
        reachable.append(("direita", transition(state, "direita", index)))
    
    if index % 3 >= 1:
        reachable.append(("esquerda", transition(state, "esquerda", index)))

    if index >= 3:
        reachable.append(("cima", transition(state, "cima", index)))
    
    if index <= 5:
        reachable.append(("abaixo", transition(state, "abaixo", index)))

    return reachable


def swap(state: str, pos1: int, pos2: int):
        new_state = list(state)
        temp = new_state[pos1]
        new_state[pos1] = new_state[pos2]
        new_state[pos2] = temp
        return "".join(new_state)

def transition(state: str, action: str, index: int):
    if action == "esquerda":
        return (swap(state, index, index - 1))
    elif action == "direita":
        return (swap(state, index, index + 1))
    elif action == "cima":
        return (swap(state, index, index - 3))
    elif action == "abaixo":
        return (swap(state, index, index + 3))

