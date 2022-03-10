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
    global INITIAL_TIME
    INITIAL_TIME = time()

    possible_moves: list[tuple[int, int]] = get_ordered_possible_moves(
        board, agent_color
    )

    best_move = get_best_move(board.__str__(), possible_moves, agent_color)

    history_file = open("depths.txt", 'a')
    history_file.write('MOVES: {} - DEPTH: {} - TIME: {}\n'.format(len(possible_moves), CURRENT_MAX_DEPTH, time() - INITIAL_TIME))
    history_file.close()
    return best_move


def get_ordered_possible_moves(board: board.Board,
                               color: str) -> list[tuple[int, int]]:

    ordered_moves = board.legal_moves(color)

    # trying to put best moves first:
    def sort_funciton(move):
        return position_values[move[1], move[0]]

    ordered_moves.sort(key=sort_funciton)

    return ordered_moves


def heuristic(board: board.Board, agent_color: str) -> int:
    points = get_points(board, agent_color)

    if board.is_terminal_state():
        if points[0] > points[1]:
            return inf  # win
        elif points[0] < points[1]:
            return -inf  # loss

    total_points = points[0] + points[1]

    return 30 * get_corner(board, agent_color) + 5 * get_mobility(board, agent_color) + 25 * get_coin_difference(board, agent_color) + 25 * get_coin_parity(board)


def get_best_move(cur_state: str, possible_moves: list[tuple[int, int]],
                  agent_color: str) -> tuple[int, int]:

    global CURRENT_MAX_DEPTH
    CURRENT_MAX_DEPTH = INITIAL_DEPTH
    
    # killer move: always grab the corner:
    for move in possible_moves:
        if move == (0, 0) or move == (0,7) or move == (7,0) or move == (7,7):
            #print("KILLER MOVE!!!!!!")
            return move

    best_move = (-1, -1)
    best_value = -inf

    accumulated_time = 0.0
    while True:
        if accumulated_time > 2.5:
            break

        initial_time = time()
        alpha = -inf
        beta = inf

        for move in possible_moves:
            move_board = board.from_string(cur_state)
            move_board.process_move(move, agent_color)
            move_value = get_min_value(move_board.__str__(), alpha, beta,
                                    move_board.opponent(agent_color), 2)
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


def get_max_value(cur_state: str, alpha: float, beta: float, agent_color: str,
                  cur_depth: int) -> int:
    cur_board = board.from_string(cur_state)

    if cur_depth > CURRENT_MAX_DEPTH:
        return heuristic(cur_board, agent_color)

    if time() - INITIAL_TIME > MAX_TIME_IN_SECONDS:
        # we don't have enought time to finish the processing of this iteration
        # so we shouldn't consider this iteration
        return -inf

    v = -inf
    legal_moves = get_ordered_possible_moves(cur_board, agent_color)

    opponent = cur_board.opponent(agent_color)

    if len(legal_moves) == 0:
        if cur_board.is_terminal_state():
            # print('estado terminal max', heuristic(cur_board, agent_color))
            return heuristic(cur_board, agent_color)
        else:
            return get_min_value(cur_state, alpha, beta, opponent, cur_depth)

    for move in legal_moves:
        move_board = board.from_string(cur_state)
        move_board.process_move(move, agent_color)
        v = max(
            v,
            get_min_value(move_board.__str__(), alpha, beta, opponent,
                          cur_depth + 1))
        alpha = max(alpha, v)
        if alpha >= beta:
            break

    return v


def get_min_value(cur_state: str, alpha: float, beta: float,
                  opponent_color: str, cur_depth: int) -> int:
    cur_board = board.from_string(cur_state)

    agent_color = cur_board.opponent(opponent_color)

    if cur_depth > CURRENT_MAX_DEPTH:
        return heuristic(cur_board, agent_color)

    if time() - INITIAL_TIME > MAX_TIME_IN_SECONDS:
        # we don't have enought time to finish the processing of this iteration
        # so we shouldn't consider this iteration
        return -inf

    legal_moves = get_ordered_possible_moves(cur_board, opponent_color)

    if len(legal_moves) == 0:
        if cur_board.is_terminal_state():
            # print('estado terminal min', heuristic(cur_board, agent_color))
            return heuristic(cur_board, agent_color)
        else:
            return get_max_value(cur_state, alpha, beta, agent_color,
                                 cur_depth)

    v = inf
    for move in legal_moves:
        move_board = board.from_string(cur_state)
        move_board.process_move(move, opponent_color)
        v = min(
            v,
            get_max_value(move_board.__str__(), alpha, beta, agent_color,
                          cur_depth + 1))

        beta = min(beta, v)
        if beta <= alpha:
            break

    return v
