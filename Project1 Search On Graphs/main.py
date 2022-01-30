from state import State
from sucessor import sucessor
from expande import expande
from node import Node

s = State("2_3541687")

nodo = Node(s, None, None, 0)

print(nodo.state)

for node in expande(nodo):
    print(node)
