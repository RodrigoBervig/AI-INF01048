from math import inf
import numpy as np

from ..othello import board
from time import time
from .heuristics import *
from .openings import OpeningBook

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

    book = OpeningBook(board, agent_color)
    move = book.get_next_move()
    if move is not None:
        print("got this move from the opening")
        if move in possible_moves:
            return move
    
    if len(possible_moves) == 0:
        return (-1, -1)

    best_move = get_best_move(board.__str__(), possible_moves)

    return best_move



# trying to put best moves first:
def sort_funciton(move):
    return -position_values[move[1], move[0]]

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
    global CURRENT_MAX_DEPTH, INITIAL_TIME
    CURRENT_MAX_DEPTH = INITIAL_DEPTH

    best_move = (-1, -1)
    best_value = -inf

    accumulated_time = 0.0

    alpha = -inf
    beta = inf

    while True:
        if accumulated_time > 3:
            break

        initial_time = time()

        best_local_value = -inf
        best_local_move = (-1,-1)

        for move in possible_moves:
            move_board = board.from_string(cur_state)
            move_board.process_move(move, AGENT_COLOR)
            move_value = get_min_value(move_board.__str__(), alpha, beta, 2)
            if move_value > best_local_value:
                best_local_value = move_value
                best_local_move = move

            if best_local_value == inf:
                # we found a winning move
                return best_local_move

        if time() - INITIAL_TIME < MAX_TIME_IN_SECONDS:
            # if the condition if true, we are sure all the search was completed
            best_value = best_local_value
            best_move = best_local_move

        CURRENT_MAX_DEPTH += 1
        accumulated_time += time() - initial_time
    
    if best_value > -inf:
        return best_move
    else:
        return possible_moves[0]

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
