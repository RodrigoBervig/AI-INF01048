from pyparsing import col
from ..othello import board

rmovs = [-1, -1, -1, 0, 1, 1, 1, 0]
cmovs = [-1, 0, 1, 1, 1, 0, -1, -1]


def get_corner(board: board.Board, agent_color: str) -> int:
    oponent_color = board.opponent(agent_color)
    agent_corners = 0
    oponent_corners = 0

    corners = [(0, 0), (7, 7), (7, 0), (0, 7)]

    for c1, c2 in corners:
        agent_corners += board.tiles[c1][c2] == agent_color
        oponent_corners += board.tiles[c1][c2] == oponent_color

    return (0 if oponent_corners + agent_corners == 0 else
            100 * (agent_corners - oponent_corners) /
            (oponent_corners + agent_corners))


def get_mobility(board: board.Board, agent_color: str) -> int:

    oponent_color = board.opponent(agent_color)
    myMoves = len(board.legal_moves(agent_color))
    oppMoves = len(board.legal_moves(oponent_color))

    if myMoves + oppMoves != 0:
        mobility = 100*(myMoves - oppMoves)/(myMoves + oppMoves)
    else:
        mobility = 0

    return mobility


def get_potential_mobility(board: board.Board, agent_color: str) -> int:

    def valid_position(row, column):
        return row >= 0 and row < 8 and column >= 0 and column < 8

    agent_adjacency = set()
    opponent_adjacency = set()

    for i in range(0, 8):
        for j in range(0, 8):
            if board.tiles[i][j] == '.':
                continue
            for k in range(0, 8):
                if valid_position(i + rmovs[k], j + cmovs[k]):
                    if board.tiles[i][j] == agent_color:
                        agent_adjacency.add((i, j))
                    else:
                        opponent_adjacency.add((i, j))

    agent_potential = len(agent_adjacency)
    opponent_potential = len(opponent_adjacency)

    if agent_potential + opponent_potential == 0:
        return 0

    return 100 * (agent_potential - opponent_potential) / (agent_potential + opponent_potential)


def get_points(board: board.Board, agent_color: str) -> tuple[int, int]:
    """
    Returns a tuple (a,b) where a is the agent's points, and b is the opponent's points
    """
    oponent_color = board.opponent(agent_color)
    p1_score = sum([1 for char in str(board) if char == agent_color])
    p2_score = sum([1 for char in str(board) if char == oponent_color])

    return (p1_score, p2_score)


def get_coin_difference(board: board.Board, agent_color: str):
    player_points, opponent_points = get_points(board, agent_color)

    if player_points + opponent_points == 0:
        return 0
    return 100 * (player_points - opponent_points)/(player_points + opponent_points)


def get_coin_parity(board: board.Board):
    p1, p2 = get_points(board, 'W')
    return 1 if (64 - (p1 + p2)) % 2 == -1 else 1
