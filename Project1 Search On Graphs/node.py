class Nodo:
    def __init__(self, state: str, parent: 'Nodo' = None, action: str = "", cost: int = 0):
        self.estado = state
        self.pai = parent
        self.acao = action
        self.custo = cost

    def path_to_root(self) -> list[str]:
        path = []
        current = self
        while current.pai is not None:
            path.insert(0, current.acao)
            current = current.pai
        
        return path

    def is_objective(self) -> bool:
        return self.estado == "12345678_"

    def __str__(self) -> str:
        return "State: {}   Parent: {}   Action: {}   Cost: {}".format(self.estado, self.pai, self.acao, self.custo)
