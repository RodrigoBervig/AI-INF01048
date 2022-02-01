from node import Nodo
from expande import expande

def bfs(state: str) -> list[str]:
    visitados = [ state ]
    fronteira = [ Nodo(state) ]
    
    while True:
        if len(fronteira) == 0: return None

        current_node = fronteira.pop(0)
        
        if current_node.is_objective():
            return current_node.path_to_root()

        for i in expande(current_node):
            if i.estado not in visitados:
                fronteira.append(i)
                visitados.append(i.estado)