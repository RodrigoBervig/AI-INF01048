Nome | Cartão | Turma
---|:---:|:---:
Fernando Zanutto | 00302340 | A
Gabriel Fagundes da Fonseca | 00301151 | A
Rodrigo Bergiv Rocha | 00301709 | A


## Heurísticas:
	Foram utilzadas heurísticas baseadas no artigo An Analysis of Heuristics in Othello, de V. Sannidhanam e M. Annamalai. Elas são utilizadas toda vez que o algoritmo alcança um estado terminal, ou quando avaliação chega na profundidade máxima definida pela constante CURRENT_MAX_DEPTH
	Os pesos das heurísticas foram fortemente baseado no pesos relatado no mesmo artigo.

# Mobility:
	A heurística Mobility parte da ideia de maximizar a mobilidade do player e restringir a mobilidade do oponente, de forma a diminuir as oportunidades dele colocar peças que possibilitem o aumento de controle na região. A mobilidade atual é calculada examinando o tabuleiro e contando o número de movimentos legais para o player.
	100 * (PlayerPossibleMoves - OponentPossibleMoves)/(PlayerPossibleMoves + OponenetPossibleMoves)

# Corners Captured:
	A heurística Corners Captured utiliza do princípio que os cantos do tabuleiro no jogo othello são posições fortes, pois uma vez capturados eles não podem ser recapturados pelo adversário. Corners Captured é calculado examinando os cantos e contando quantos cantos o player possui e quantos cantos o openente possui. A diferença dos dois é dividida pela soma dos cantos capturados e multiplicada por 100.
	100 * (PlayerCorners - OponentCorners) / (PlayerCorners + OponentCorners)

# Coin Difference:
	A heurística Coin Difference simplesmente avalia a atual posição do tabuleiro e calcula a diferença de pontos entre os 	jogadores.
	100 * (PlayerPoints - OponentPoints) / (PlayerPoints + OponentPoints)

# Coin Parity:
	A heurística Coin Parity estima quem será o jogador a fazer o último lance conforme o tabuleiro atual, essa heurística possui pesos que são incrementados conforme o passar da partida, pois a chance da estimativa estar certa aumenta conforme o jogo chega ao fim.
	Ela é calculada da seguinte forma:
	if (64 - (PlayerPoints + OponentPoints)) % 2 == -1
		return 1
	else
		return 0

