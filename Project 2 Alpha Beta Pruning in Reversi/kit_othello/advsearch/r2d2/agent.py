from math import inf
import random
import numpy as np

from turtle import pos
from ..othello import board
from time import time
from .heuristics import *

INITIAL_TIME = 0.0
MAX_TIME_IN_SECONDS = 4.6
CURRENT_MAX_DEPTH = 3
INITIAL_DEPTH = 3
AGENT_COLOR = ""
OPPONENT_COLOR = ""

position_values = np.matrix([
    [4, -3, 2, 2, 2, 2, -3, 4],
    [-3, -4, -1, -1, -1, -1, -4, -3],
    [2, -1, 1, 0, 0, 1, -1, 2],
    [2, -1, 0, 1, 1, 0, -1, 2],
    [2, -1, 0, 1, 1, 0, -1, 2],
    [2, -1, 1, 0, 0, 1, -1, 2],
    [-3, -4, -1, -1, -1, -1, -4, -3],
    [4, -3, 2, 2, 2, 2, -3, 4]
])


def make_move(board: board.Board, agent_color: str) -> tuple[int, int]:
    """
    Returns an Othello move
    :param the_board: a board.Board object with the current game state
    :param color: a character indicating the color to make the move ('B' or 'W')
    :return: (int, int) tuple with x, y indexes of the move (remember: 0 is the first row/column)
    """
    global INITIAL_TIME, AGENT_COLOR, OPPONENT_COLOR
    INITIAL_TIME = time()

    AGENT_COLOR = agent_color
    OPPONENT_COLOR = board.opponent(agent_color)

    possible_moves = get_ordered_possible_moves(board, agent_color)

    if len(possible_moves) == 0:
        return (-1, -1)

    best_move = get_best_move(board.__str__(), possible_moves)

    history_file = open("depths.txt", 'a')
    history_file.write('MOVES: {} - DEPTH: {} - TIME: {}\n'.format(
        len(possible_moves), CURRENT_MAX_DEPTH, time() - INITIAL_TIME))
    history_file.close()
    return best_move



# trying to put best moves first:
def sort_funciton(move):
    return position_values[move[1], move[0]]

def get_ordered_possible_moves(board: board.Board,
                               color: str) -> list[tuple[int, int]]:

    ordered_moves = board.legal_moves(color)

    ordered_moves.sort(key=sort_funciton)

    return ordered_moves


def heuristic(board: board.Board) -> int:
    points = get_points(board, AGENT_COLOR)

    if board.is_terminal_state():
        if points[0] > points[1]:
            return inf  # win
        elif points[0] < points[1]:
            return -inf  # loss

    total_points = points[0] + points[1]

    if total_points <= 20: # "early game"
        return 5 * get_corner(board, AGENT_COLOR) + 25 * get_mobility(board, AGENT_COLOR) + 25 * get_potential_mobility(board, AGENT_COLOR)
    if total_points <= 50: # "middle game"
        return 30 * get_corner(board, AGENT_COLOR) + 20 * get_mobility(board, AGENT_COLOR) + 20 * get_potential_mobility(board, AGENT_COLOR) + 25 * get_coin_difference(board, AGENT_COLOR) + 5 * get_coin_parity(board)
    # "end game"
    return 30 * get_corner(board, AGENT_COLOR) + 15 * get_mobility(board, AGENT_COLOR) + 15 * get_mobility(board, AGENT_COLOR)  + 25 * get_coin_difference(board, AGENT_COLOR) + 25 * get_coin_parity(board)


def get_best_move(cur_state: str, possible_moves: list[tuple[int, int]]) -> tuple[int, int]:
    global CURRENT_MAX_DEPTH
    CURRENT_MAX_DEPTH = INITIAL_DEPTH

    # killer move: always grab the corner:
    for move in possible_moves:
        if move == (0, 0) or move == (0, 7) or move == (7, 0) or move == (7, 7):
            #print("KILLER MOVE!!!!!!")
            return move

    best_move = (-1, -1)
    best_value = -inf

    accumulated_time = 0.0
    while True:
        if accumulated_time > 3:
            break

        initial_time = time()
        alpha = -inf
        beta = inf

        for move in possible_moves:
            move_board = board.from_string(cur_state)
            move_board.process_move(move, AGENT_COLOR)
            move_value = get_min_value(move_board.__str__(), alpha, beta, 2)
            if move_value > best_value:
                best_value = move_value
                best_move = move

            alpha = max(alpha, best_value)
            if alpha >= beta:
                break

        if best_value == -inf:
            # we reached the end of the tree and all moves are losing moves (it's impossible to win)
            # then we choose a random move
            best_move = random.choice(possible_moves)

        if best_value == inf:
            # there is a winning move, no need to run anymore
            break

        CURRENT_MAX_DEPTH += 1
        accumulated_time += time() - initial_time

    return best_move


def get_max_value(cur_state: str, alpha: float, beta: float, cur_depth: int) -> int:
    cur_board = board.from_string(cur_state)

    if cur_depth > CURRENT_MAX_DEPTH:
        return heuristic(cur_board)

    if time() - INITIAL_TIME > MAX_TIME_IN_SECONDS:
        # we don't have enought time to finish the processing of this iteration
        # so we shouldn't consider this iteration
        return -inf

    v = -inf
    legal_moves = get_ordered_possible_moves(cur_board, AGENT_COLOR)

    if len(legal_moves) == 0:
        if cur_board.is_terminal_state():
            # print('estado terminal max', heuristic(cur_board, AGENT_COLOR))
            return heuristic(cur_board)
        else:
            return get_min_value(cur_state, alpha, beta, cur_depth)

    for move in legal_moves:
        move_board = board.from_string(cur_state)
        move_board.process_move(move, AGENT_COLOR)
        v = max(
            v,
            get_min_value(move_board.__str__(), alpha, beta, cur_depth + 1)
        )
        alpha = max(alpha, v)
        if alpha >= beta:
            break

    return v


def get_min_value(cur_state: str, alpha: float, beta: float, cur_depth: int) -> int:
    cur_board = board.from_string(cur_state)

    if cur_depth > CURRENT_MAX_DEPTH:
        return heuristic(cur_board)

    if time() - INITIAL_TIME > MAX_TIME_IN_SECONDS:
        # we don't have enought time to finish the processing of this iteration
        # so we shouldn't consider this iteration
        return -inf

    legal_moves = get_ordered_possible_moves(cur_board, OPPONENT_COLOR)

    if len(legal_moves) == 0:
        if cur_board.is_terminal_state():
            # print('estado terminal min', heuristic(cur_board, agent_color))
            return heuristic(cur_board)
        else:
            return get_max_value(cur_state, alpha, beta, cur_depth)

    v = inf
    for move in legal_moves:
        move_board = board.from_string(cur_state)
        move_board.process_move(move, OPPONENT_COLOR)
        v = min(
            v,
            get_max_value(move_board.__str__(), alpha, beta, cur_depth + 1)
        )

        beta = min(beta, v)
        if beta <= alpha:
            break

    return v
