from node import Nodo
from sucessor import sucessor

def expande(node: Nodo) -> list[Nodo]:
    children = []

    for state in sucessor(node.estado):
        children.append(
            Nodo(
                parent=node,
                action=state[0],
                cost=node.custo + 1,
                state=state[1],
            )
        )

    return children