from math import inf
from ..othello import board


def make_move(board: board.Board, color) -> tuple[int, int]:
    """
    Returns an Othello move
    :param the_board: a board.Board object with the current game state
    :param color: a character indicating the color to make the move ('B' or 'W')
    :return: (int, int) tuple with x, y indexes of the move (remember: 0 is the first row/column)
    """

    MAX_DEPTH = 5
    print(len(board.legal_moves(color)))
    return get_best_move(board, MAX_DEPTH, color)

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


def get_best_move(game_board: board.Board, max_depth, agent_color) -> tuple[int,int]:
    cur_state = game_board.__str__()
    possible_moves = game_board.legal_moves(agent_color)
    best_move = (-1,-1)
    best_value = -inf

    alpha = -inf
    beta = inf
    for move in possible_moves:
        move_board = board.from_string(cur_state)
        move_board.process_move(move, agent_color)
        move_value = get_min_value(move_board.__str__(), alpha, beta, max_depth, 1, move_board.opponent(agent_color))
        if move_value > best_value:
            best_value = move_value
            best_move = move

        alpha = max(alpha, best_value)
        if alpha >= beta:
            break

    return best_move

def get_max_value(cur_state: str, alpha, beta, max_depth, cur_depth, agent_color) -> int:
    cur_board = board.from_string(cur_state)

    if cur_depth == max_depth: 
        return heuristic(cur_board, agent_color)

    v = -inf
    for move in cur_board.legal_moves(agent_color):
        move_board = board.from_string(cur_state)
        move_board.process_move(move, agent_color)
        v = min(v, get_min_value(move_board.__str__(), alpha, beta, max_depth, cur_depth + 1, move_board.opponent(agent_color)))
        alpha = max(alpha, v)
        if alpha >= beta:
            break

    return v


def get_min_value(state: str, alpha, beta, max_depth, cur_depth, agent_color) -> int:
    cur_board = board.from_string(state)

    if cur_depth == max_depth: 
        return heuristic(cur_board, agent_color)

    v = inf
    for move in cur_board.legal_moves(agent_color):
        move_board = board.from_string(state)
        move_board.process_move(move, agent_color)
        v = max(v, get_max_value(move_board.__str__(), alpha, beta, max_depth, cur_depth + 1, move_board.opponent(agent_color)))

        beta = min(beta, v)
        if beta <= alpha: 
            break

    return v