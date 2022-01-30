from node import Node
from sucessor import sucessor
from state import State

def expande(node):
    children = []

    for state in sucessor(node.state):
        children.append(Node(
            parent=node,
            action=state[0],
            cost=node.cost+1,
            state=state[1],
        ))

    return children