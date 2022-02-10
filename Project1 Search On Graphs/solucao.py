from heapq import heapify, heappush, heappop


class Nodo:
    """
    Implemente a classe Nodo com os atributos descritos na funcao init
    """

    def __init__(self, estado, pai, acao, custo, custo_f=0):
        """
        Inicializa o nodo com os atributos recebidos
        :param estado:str, representacao do estado do 8-puzzle
        :param pai:Nodo, referencia ao nodo pai, (None no caso do nó raiz)
        :param acao:str, acao a partir do pai que leva a este nodo (None no caso do nó raiz)
        :param custo:int, custo do caminho da raiz até este nó
        """
        # substitua a linha abaixo pelo seu codigo
        self.estado = estado
        self.pai = pai
        self.acao = acao
        self.custo = custo
        self.custo_f = custo_f

    def path_to_root(self) -> list[str]:
        path = []
        current = self
        while current.pai is not None:
            path.insert(0, current.acao)
            current = current.pai

        return path

    def is_objective(self) -> bool:
        return self.estado == "12345678_"

    def __lt__(self, other):
        if self.custo_f == other.custo_f:
            return self.estado < other.estado
        return self.custo_f < other.custo_f

    def __str__(self) -> str:
        return "State: {}   Parent: {}   Action: {}   Cost: {}".format(self.estado, self.pai, self.acao, self.custo)


def sucessor(estado: str):
    """
    Recebe um estado (string) e retorna uma lista de tuplas (ação,estado atingido)
    para cada ação possível no estado recebido.
    Tanto a ação quanto o estado atingido são strings também.
    :param estado:
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    reachable = []
    index = estado.find('_')

    # indexes:
    # _____________
    # | 0 | 1 | 2 |
    # | 3 | 4 | 5 |
    # | 6 | 7 | 8 |
    # -------------

    if index % 3 <= 1:
        reachable.append(("direita", transition(estado, "direita", index)))

    if index % 3 >= 1:
        reachable.append(("esquerda", transition(estado, "esquerda", index)))

    if index >= 3:
        reachable.append(("acima", transition(estado, "acima", index)))

    if index <= 5:
        reachable.append(("abaixo", transition(estado, "abaixo", index)))

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
    elif action == "acima":
        return (swap(state, index, index - 3))
    elif action == "abaixo":
        return (swap(state, index, index + 3))


def expande(nodo):
    """
    Recebe um nodo (objeto da classe Nodo) e retorna um iterable de nodos.
    Cada nodo do iterable é contém um estado sucessor do nó recebido.
    :param nodo: objeto da classe Nodo
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    children = []

    for state in sucessor(nodo.estado):
        children.append(
            Nodo(state[1], nodo, state[0], nodo.custo + 1)
        )

    return children


def bfs(estado: str) -> list[str]:
    """
    Recebe um estado (string), executa a busca em LARGURA e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    visitados = {estado}
    fronteira = [Nodo(estado, None, "", 0)]

    while True:
        if len(fronteira) == 0:
            return None

        current_node = fronteira.pop(0)

        if current_node.is_objective():
            return current_node.path_to_root()

        for i in expande(current_node):
            if i.estado not in visitados:
                fronteira.append(i)
                visitados.add(i.estado)


def dfs(estado: str):
    """
    Recebe um estado (string), executa a busca em PROFUNDIDADE e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    # substituir a linha abaixo pelo seu codigo
    visitados = {estado}
    fronteira = [Nodo(estado, None, "", 0)]

    while True:
        if len(fronteira) == 0:
            return None

        current_node = fronteira.pop(0)

        if current_node.is_objective():
            return current_node.path_to_root()

        for i in expande(current_node):
            if i.estado not in visitados:
                fronteira.insert(0, i)
                visitados.add(i.estado)


def astar(estado, heuristica):
    """
    Recebe um estado (string), executa a busca A* com h(n) = heuristica(n) e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    visitados = {estado}
    fronteira = []
    heapify(fronteira)
    heappush(fronteira, Nodo(estado, None, "", 0))

    while True:
        if len(fronteira) == 0:
            return None

        current_node = heappop(fronteira)

        if current_node.is_objective():
            return current_node.path_to_root()

        for i in expande(current_node):
            if i.estado not in visitados:
                i.custo_f = i.custo + heuristica(i.estado)
                heappush(fronteira, i)
                visitados.add(i.estado)


def astar_hamming(estado):
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Hamming e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    def hamming(estado):
        fora_do_lugar = 0
        for i in range(0, 9):
            if estado[i] != '_' and estado[i] != str(i+1):
                fora_do_lugar += 1

        return fora_do_lugar

    return astar(estado, hamming)


def astar_manhattan(estado):
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Manhattan e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    def distManhattan(bloco, pos):
        if(bloco == '_'):
            x = ((pos-1) % 3) + 1  # Posição horizontal do bloco
            y = (pos-1)/3 + 1  # Posição vertical do bloco
            return abs(x-3) + abs(y-3)
        else:
            bloco = int(bloco)
            x = ((pos-1) % 3) + 1  # Posição horizontal do bloco
            y = (pos-1)/3 + 1  # Posição vertical do bloco
            # Posição horizontal onde bloco deve estar
            xx = ((bloco-1) % 3) + 1
            yy = (pos-1)/3 + 1  # Posição vertical onde bloco deve estar
            return abs(x-xx) + abs(y-yy)
    # substituir a linha abaixo pelo seu codigo

    def manhattan(estado):
        soma_dist = 0
        for i in range(0, 8):
            if estado[i] != str(i+1):
                soma_dist += distManhattan(estado[i], i+1)

        return soma_dist

    return astar(estado, manhattan)
