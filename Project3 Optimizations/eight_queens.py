from random import random, choice, choices

def evaluate(individual: list[int]):
    """
    Recebe um indivíduo (lista de inteiros) e retorna o número de ataques
    entre rainhas na configuração especificada pelo indivíduo.
    Por exemplo, no individuo [2,2,4,8,1,6,3,4], o número de ataques é 9.

    :param individual:list
    :return:int numero de ataques entre rainhas no individuo recebido
    """

    total_attacks = 0

    for queen_column in range(8):
        queen_line = individual[queen_column]

        for other_column, other_line in enumerate(individual):
            if queen_column == other_column:
                continue

            if queen_line == other_line:
                total_attacks += 1
                continue

            column_diff = queen_column - other_column
            line_diff = queen_line - other_line
            if abs(column_diff) == abs(line_diff):
                total_attacks += 1
                continue

    return total_attacks // 2
            
    
def sort_function(participant: list[int]):
    return evaluate(participant)


def tournament(participants: list[list[int]]):
    """
    Recebe uma lista com vários indivíduos e retorna o melhor deles, com relação
    ao numero de conflitos
    :param participants:list - lista de individuos
    :return:list melhor individuo da lista recebida
    """
    sorted_participants = sorted(participants, key = sort_function)

    return sorted_participants[0]


def crossover(parent1: list[int], parent2: list[int], index: int):
    """
    Realiza o crossover de um ponto: recebe dois indivíduos e o ponto de
    cruzamento (indice) a partir do qual os genes serão trocados. Retorna os
    dois indivíduos com o material genético trocado.
    Por exemplo, a chamada: crossover([2,4,7,4,8,5,5,2], [3,2,7,5,2,4,1,1], 3)
    deve retornar [2,4,7,5,2,4,1,1], [3,2,7,4,8,5,5,2].
    A ordem dos dois indivíduos retornados não é importante
    (o retorno [3,2,7,4,8,5,5,2], [2,4,7,5,2,4,1,1] também está correto).
    :param parent1:list
    :param parent2:list
    :param index:int
    :return:list,list
    """
    
    return parent1[0:index] + parent2[index:], parent2[0:index] + parent1[index:]


def mutate(individual: list[int], m: float):
    """
    Recebe um indivíduo e a probabilidade de mutação (m).
    Caso random() < m, sorteia uma posição aleatória do indivíduo e
    coloca nela um número aleatório entre 1 e 8 (inclusive).
    :param individual:list
    :param m:int - probabilidade de mutacao
    :return:list - individuo apos mutacao (ou intacto, caso a prob. de mutacao nao seja satisfeita)
    """

    if random() < m:
        index = choice(range(8))

        individual[index] = choice(range(8))

    return individual

def selection(participants, k):
    sorted_participants = sorted(choices(participants, k = k), key = sort_function)

    return sorted_participants[0], sorted_participants[1]
    
def run_ga(g: int, n: int, k: int, m: float, e: bool):
    """
    Executa o algoritmo genético e retorna o indivíduo com o menor número de ataques entre rainhas
    :param g:int - numero de gerações
    :param n:int - numero de individuos
    :param k:int - numero de participantes do torneio
    :param m:float - probabilidade de mutação (entre 0 e 1, inclusive)
    :param e:bool - se vai haver elitismo
    :return:list - melhor individuo encontrado
    """

    population = []
    for _ in range(n):
        population.append([choice(range(8)) for _ in range(8)])
    
    for _ in range(g):
        pop2 = []
        if e:
            pop2.append(tournament(population))

        while len(pop2) < n:
            p1, p2 = selection(population, k)
            o1, o2 = crossover(p1, p2, choice(range(8)))
            o1 = mutate(o1, m)
            o2 = mutate(o2, m)
            
            pop2.append(o1)
            pop2.append(o2)
        
        population = pop2

    return tournament(population)
