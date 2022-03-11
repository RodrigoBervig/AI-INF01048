Nome | Cartão | Turma
---|:---:|:---:
Fernando Zanutto | 00302340 | A
Gabriel Fagundes da Fonseca | 00301151 | A
Rodrigo Bervig Rocha | 00301709 | A

# Implementação:

# Condições de parada:
	Limitamos o tempo de processamento em 4.6 segundos para dar uma margem segura dos 5 segundos limite. Outra condição de parada é a profundidade máxima do Iterative Deepening.
# Alpha Beta prunning - Iterative Deepening:
	Implementamos o Iterative Deepening rodando inicialmente com profundidade máxima 3, e incrementando em 1 a cada iteração. Também ordenamos os movimentos possíveis a partir de pesos estáticos para cada posição, afim de minimizar o número de nodos expandidos.

# Heurísticas:
	Foram utilzadas heurísticas baseadas no artigo An Analysis of Heuristics in Othello, de V. Sannidhanam e M. Annamalai. Elas são utilizadas toda vez que o algoritmo alcança um estado terminal, ou quando avaliação chega na profundidade máxima definida pela constante CURRENT_MAX_DEPTH
	Os pesos das heurísticas foram fortemente baseado no pesos relatado no mesmo artigo.

## Mobility:
	A heurística Mobility parte da ideia de maximizar a mobilidade do player e restringir a mobilidade do oponente, de forma a diminuir as oportunidades dele colocar peças que possibilitem o aumento de controle na região. A mobilidade atual é calculada examinando o tabuleiro e contando o número de movimentos legais para o player.
	100 * (PlayerPossibleMoves - OponentPossibleMoves)/(PlayerPossibleMoves + OponenetPossibleMoves)
	Além de mobilidade, calculamos a mobilidade potencial, que mede no logo prazo qual será a mobilidade de cada jogador, essa heurística é calculada a partir do número de células adjacentes em branco as peças de um jogador, o calculo se dá da mesma maneira

## Corners Captured:
	A heurística Corners Captured utiliza do princípio que os cantos do tabuleiro no jogo othello são posições fortes, pois uma vez capturados eles não podem ser recapturados pelo adversário. Corners Captured é calculado examinando os cantos e contando quantos cantos o player possui e quantos cantos o openente possui. A diferença dos dois é dividida pela soma dos cantos capturados e multiplicada por 100.
	100 * (PlayerCorners - OponentCorners) / (PlayerCorners + OponentCorners)

## Coin Difference:
	A heurística Coin Difference simplesmente avalia a atual posição do tabuleiro e calcula a diferença de pontos entre os 	jogadores.
	100 * (PlayerPoints - OponentPoints) / (PlayerPoints + OponentPoints)

## Coin Parity:
	A heurística Coin Parity estima quem será o jogador a fazer o último lance conforme o tabuleiro atual, essa heurística possui pesos que são incrementados conforme o passar da partida, pois a chance da estimativa estar certa aumenta conforme o jogo chega ao fim.
	Ela é calculada da seguinte forma:
	if (64 - (PlayerPoints + OponentPoints)) % 2 == -1
		return 1
	else
		return 0

# Fontes:
- https://www.ffothello.org/livres/othello-book-Brian-Rose.pdf
- http://home.datacomm.ch/t_wolf/tw/misc/reversi/html/index.html
- https://www.ultraboardgames.com/othello/opening-moves.php
- https://skatgame.net/mburo/log.html -- Database de aberturas
- https://barberalec.github.io/pdf/An_Analysis_of_Othello_AI_Strategies.pdf -- Heuristicas
- https://courses.cs.washington.edu/courses/cse573/04au/Project/mini1/RUSSIA/Final_Paper.pdf
- http://ceur-ws.org/Vol-1107/paper2.pdf -- Potential Mobility
