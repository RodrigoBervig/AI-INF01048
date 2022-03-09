from math import inf
import random
from ..othello import board
from time import time
from .heuristics import *

INITIAL_TIME = 0.0
MAX_TIME_IN_SECONDS = 4.8
MAX_DEPTH = 8


def make_move(board: board.Board, agent_color: str) -> tuple[int, int]:
    """
    Returns an Othello move
    :param the_board: a board.Board object with the current game state
    :param color: a character indicating the color to make the move ('B' or 'W')
    :return: (int, int) tuple with x, y indexes of the move (remember: 0 is the first row/column)
    """
    global INITIAL_TIME
    INITIAL_TIME = time()

    # print(board.legal_moves(color))
    possible_moves: list[tuple[int, int]] = get_ordered_possible_moves(
        board, agent_color)
    best_move = get_best_move(board.__str__(), possible_moves, agent_color)
    print(time() - INITIAL_TIME)
    return best_move


def get_ordered_possible_moves(board: board.Board,
                               color: str) -> list[tuple[int, int]]:

    ordered_moves = board.legal_moves(color)

    return ordered_moves


def heuristic(board: board.Board, agent_color: str) -> int:
    points = get_points(board, agent_color)

    if board.is_terminal_state():
        if points[0] > points[1]:
            return inf  # win
        elif points[0] < points[1]:
            return -inf  # loss

    total_points = points[0] + points[1]
    if total_points <= 20:
        return 1000 * get_corner(board, agent_color) + 50 * get_mobility(board, agent_color)
    elif total_points <= 55:
        return 1000 * get_corner(board, agent_color) + 20 * get_mobility(board, agent_color) + 10 * get_coin_difference(board, agent_color)
    
    return 1000 * get_corner(board, agent_color) + 100 * get_mobility(board, agent_color) + 500 * get_coin_difference(board, agent_color)


def get_best_move(cur_state: str, possible_moves: list[tuple[int, int]],
                  agent_color: str) -> tuple[int, int]:
    best_move = (-1, -1)
    best_value = -inf

    alpha = -inf
    beta = inf
    for move in possible_moves:
        move_board = board.from_string(cur_state)
        move_board.process_move(move, agent_color)
        move_value = get_min_value(move_board.__str__(), alpha, beta,
                                   move_board.opponent(agent_color), 1)
        if move_value > best_value:
            best_value = move_value
            best_move = move

        alpha = max(alpha, best_value)
        if alpha >= beta:
            break

    if best_value == -inf:
        # if all moves are losing moves (it's impossible to win), choose a random move
        best_move = random.choice(possible_moves)

    return best_move


def get_max_value(cur_state: str, alpha: float, beta: float, agent_color: str,
                  cur_depth: int) -> int:
    cur_board = board.from_string(cur_state)

    if cur_depth >= MAX_DEPTH or time() - INITIAL_TIME > MAX_TIME_IN_SECONDS:
        return heuristic(cur_board, agent_color)

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

    if cur_depth >= MAX_DEPTH or time() - INITIAL_TIME > MAX_TIME_IN_SECONDS:
        # pass oponent color here, since the opponent is trying to minimize our score
        return heuristic(cur_board, cur_board.opponent(agent_color))

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
