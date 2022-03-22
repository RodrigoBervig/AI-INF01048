import numpy as np


def compute_mse(theta_0, theta_1, data):
    """
    Calcula o erro quadratico medio
    :param theta_0: float - intercepto da reta
    :param theta_1: float -inclinacao da reta
    :param data: np.array - matriz com o conjunto de dados, x na coluna 0 e y na coluna 1
    :return: float - o erro quadratico medio
    """
    mse = 0.0
    for dt in data:
        mse += ((theta_0 + theta_1*dt[0]) - dt[1]) ** 2

    mse /= len(data)
    return mse


def step_gradient(theta_0, theta_1, data, alpha):
    """
    Executa uma atualização por descida do gradiente  e retorna os valores atualizados de theta_0 e theta_1.
    :param theta_0: float - intercepto da reta
    :param theta_1: float -inclinacao da reta
    :param data: np.array - matriz com o conjunto de dados, x na coluna 0 e y na coluna 1
    :param alpha: float - taxa de aprendizado (a.k.a. tamanho do passo)
    :return: float,float - os novos valores de theta_0 e theta_1, respectivamente
    """
    derivTheta_0 = 0.0
    derivTheta_1 = 0.0
    for dt in data:
        derivTheta_0 += (theta_0 + theta_1*dt[0])-dt[1]
        derivTheta_1 += ((theta_0 + theta_1*dt[0])-dt[1]) * dt[0]

    derivTheta_0 *= 2/len(data)
    derivTheta_1 *= 2/len(data)

    newTheta_0 = theta_0 - alpha*derivTheta_0
    newTheta_1 = theta_1 - alpha*derivTheta_1
    return newTheta_0,newTheta_1


def fit(data, theta_0, theta_1, alpha, num_iterations):
    """
    Para cada época/iteração, executa uma atualização por descida de
    gradiente e registra os valores atualizados de theta_0 e theta_1.
    Ao final, retorna duas listas, uma com os theta_0 e outra com os theta_1
    obtidos ao longo da execução (o último valor das listas deve
    corresponder à última época/iteração).

    :param data: np.array - matriz com o conjunto de dados, x na coluna 0 e y na coluna 1
    :param theta_0: float - intercepto da reta
    :param theta_1: float -inclinacao da reta
    :param alpha: float - taxa de aprendizado (a.k.a. tamanho do passo)
    :param num_iterations: int - numero de épocas/iterações para executar a descida de gradiente
    :return: list,list - uma lista com os theta_0 e outra com os theta_1 obtidos ao longo da execução
    """
    newTheta_0 = theta_0
    newTheta_1 = theta_1
    listTheta_0 = [theta_0]
    listTheta_1 = [theta_1]
    for i in range(num_iterations):
        newTheta_0, newTheta_1 = step_gradient(newTheta_0, newTheta_1, data, alpha)
        listTheta_0.append(newTheta_0)
        listTheta_1.append(newTheta_1)

    return listTheta_0, listTheta_1

'''
if __name__ == "__main__":
        data = np.genfromtxt('alegrete.csv', delimiter=',')
        print(step_gradient(1, 1, np.array([
            [1, 3],
            [2, 4],
            [3, 4],
            [4, 2]
        ])
, alpha=0.1))
        print(compute_mse(0,0,data))
        theta_0,theta_1 = fit(data, 0, 0, 0.1, 10)
        print(theta_0,theta_1)
'''
