from math import inf
from pickle import BINPERSID
import random
import sys
from ..othello import board
# Voce pode criar funcoes auxiliares neste arquivo
# e tambem modulos auxiliares neste pacote.
#
# Nao esqueca de renomear 'your_agent' com o nome
# do seu agente.


def make_move(board: board.Board, color) -> tuple[int, int]:
    """
    Returns an Othello move
    :param the_board: a board.Board object with the current game state
    :param color: a character indicating the color to make the move ('B' or 'W')
    :return: (int, int) tuple with x, y indexes of the move (remember: 0 is the first row/column)
    """

    MAX_DEPTH = 5

    move_to_make = get_max_value(board.__str__(), -inf, inf, MAX_DEPTH, 0, color)[1]

    return move_to_make


def heuristic(board: board.Board, agent_color: str) -> int:
    points = get_points(board, agent_color)
    return points[0] - points[1]

def get_points(board: board.Board, agent_color: str) -> tuple[int, int]:
    """
    Returns a tuple (a,b) where a is the agent's points, and b is the opponent's points
    """
    oponent_color = 'B' if agent_color == 'W' else 'W'
    p1_score = sum([1 for char in str(board) if char == agent_color])
    p2_score = sum([1 for char in str(board) if char == oponent_color])

    return (p1_score, p2_score)


def get_max_value(state: str, alpha, beta, max_depth, cur_depth, agent_color) -> tuple[int, tuple[int,int]]:
    cur_board: board.Board = board.from_string(state)

    if cur_depth == max_depth: 
        return (heuristic(cur_board, agent_color), (-1,-1))

    v = -inf
    best_move = (-1, -1)
    for move in cur_board.legal_moves(agent_color):
        move_board: board.Board = board.from_string(state)
        move_board.process_move(move, agent_color)
        move_value = get_min_value(move_board.__str__(), alpha, beta, max_depth, cur_depth + 1, move_board.opponent(agent_color))[0]
        if move_value > v:
            v = move_value
            best_move = move

        alpha = max(alpha, v)
        if alpha >= beta:
            break

    return (v, best_move)


def get_min_value(state: str, alpha, beta, max_depth, cur_depth, agent_color) -> tuple[int, tuple[int,int]]:
    cur_board: board.Board = board.from_string(state)

    if cur_depth == max_depth: 
        return (heuristic(cur_board, agent_color), (-1,-1))

    v = inf
    best_move = (-1, -1)
    for move in cur_board.legal_moves(agent_color):
        move_board: board.Board = board.from_string(state)
        move_board.process_move(move, agent_color)
        move_value = get_max_value(move_board.__str__(), alpha, beta, max_depth, cur_depth + 1, move_board.opponent(agent_color))[0]
        if move_value < v:
            v = move_value
            best_move = move

        beta = min(beta, v)
        if beta <= alpha: 
            break

    return (v, best_move)


if __name__ == '__main__':
    b = board.from_string("""BBBBBBBB
BBBBBBBB
BWBWWBBW
BWWWWWWW
BWBBBBW.
BBBWBWW.
BBWBBWWB
BBBBBW..""")
    move = make_move(b, 'B')
    print(f'A random move for black in the initial state: {move}')
    print('Resulting state:')
    b.process_move(move, 'B')
    b.print_board()