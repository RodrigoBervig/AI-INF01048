import random
from readline import write_history_file
from ..othello import board


from pyparsing import col

openings = [
    "C4e3F6e6F5g6E7c5",
    "C4e3F6e6F5g6",
    "C4e3F6e6F5c5F4g6F7g5",
    "C4e3F6e6F5c5F4g6F7d3",
    "C4e3F6e6F5c5F4g6F7",
    "C4e3F6e6F5c5F4g5G4f3C6d3D6b3C3b4E2b6",
    "C4e3F6e6F5c5F4g5G4f3C6d3D6",
    "C4e3F6e6F5c5D6",
    "C4e3F6e6F5c5D3",
    "C4e3F6e6F5c5C3g5",
    "C4e3F6e6F5c5C3c6D6",
    "C4e3F6e6F5c5C3c6D3d2E2b3C1c2B4a3A5b5A6a4A2",
    "C4e3F6e6F5c5C3c6",
    "C4e3F6e6F5c5C3b4D6c6B5a6B6c7",
    "C4e3F6e6F5c5C3b4",
    "C4e3F6e6F5c5C3",
    "C4e3F6e6F5",
    "C4e3F6b4",
    "C4e3F5e6F4c5D6c6F7g5G6",
    "C4e3F5e6F4c5D6c6F7f3",
    "C4e3F5e6F4",
    "C4e3F5e6D3",
    "C4e3F5b4F3f4E2e6G5f6D6c6",
    "C4e3F5b4F3",
    "C4e3F5b4",
    "C4e3F4c5E6",
    "C4e3F4c5D6f3E6c6",
    "C4e3F4c5D6f3E6c3D3e2D2",
    "C4e3F4c5D6f3E6c3D3e2B6f5G5f6",
    "C4e3F4c5D6f3E6c3D3e2B6f5G5",
    "C4e3F4c5D6f3E6c3D3e2B6f5B4f6G5d7",
    "C4e3F4c5D6f3E6c3D3e2B6f5",
    "C4e3F4c5D6f3E6c3D3e2B5f5B4f6C2e7D2c7",
    "C4e3F4c5D6f3E6c3D3e2B5f5B3",
    "C4e3F4c5D6f3E6c3D3e2B5f5",
    "C4e3F4c5D6f3E6c3D3e2B5",
    "C4e3F4c5D6f3E6c3D3e2",
    "C4e3F4c5D6f3E2",
    "C4e3F4c5D6f3D3c3",
    "C4e3F4c5D6f3D3",
    "C4e3F4c5D6f3C6",
    "C4e3F4c5D6e6",
    "C4e3",
    "C4c5",
    "C4c3F5c5",
    "C4c3E6c5",
    "C4c3D3c5F6f5",
    "C4c3D3c5F6e3C6f5F4g5",
    "C4c3D3c5F6e2C6",
    "C4c3D3c5F6",
    "C4c3D3c5D6f4F5e6F6",
    "C4c3D3c5D6f4F5e6C6d7",
    "C4c3D3c5D6f4F5d2G4d7",
    "C4c3D3c5D6f4F5d2B5",
    "C4c3D3c5D6f4F5d2",
    "C4c3D3c5D6f4F5",
    "C4c3D3c5D6f4B4e3B3",
    "C4c3D3c5D6f4B4c6B5b3B6e3C2a4A5a6D2",
    "C4c3D3c5D6f4B4b6B5c6F5",
    "C4c3D3c5D6f4B4b6B5c6B3",
    "C4c3D3c5D6f4B4",
    "C4c3D3c5D6e3",
    "C4c3D3c5D6",
    "C4c3D3c5B6e3",
    "C4c3D3c5B6c6B5",
    "C4c3D3c5B6",
    "C4c3D3c5B5",
    "C4c3D3c5B4e3",
    "C4c3D3c5B4d2E2",
    "C4c3D3c5B4d2D6",
    "C4c3D3c5B4d2C2f4D6c6F5e6F7",
    "C4c3D3c5B4",
    "C4c3D3c5B3f4B5b4C6d6F5",
    "C4c3D3c5B3f3",
    "C4c3D3c5B3",
    "C4c3D3c5B2",
    "C4c3"
]

class OpeningBook:

    def __init__(self, board: board.Board, agent_color: str):
        self.history = ""
        self.history_file = "r2d2_move_history_file_dont_touch_it_is_art.txt"
        self.opening_is_over = False
        self.internal_board = [['.'] * 8 for i in range(8)]

        self.internal_board[3][3] = self.internal_board[4][3] = self.internal_board[3][4] = self.internal_board[4][4] = 'B'

        p1, p2 = self.get_points_from_board(board, agent_color)

        file = open(self.history_file, 'a+')
        file.close()

        file = open(self.history_file, 'r+')

        if p1 + p2 == 4:  # we know the game is starting now, therefore we must erase the file from any previous game
            file.truncate(0)
        else:
            self.history = file.read()

        file.close()

        if len(self.history):  # then we know that our oponent has to have made a move last time
            if self.history[-1] == 'L':
                self.opening_is_over = True
                return

            for i in range(0, len(self.history), 2):
                column, row = self.notation_to_move(
                    self.history[i], self.history[i+1])
                self.internal_board[row][column] = 'B'

            oponent_last_move = (-1, -1)
            oponent_index = 1 if agent_color == 'B' else 0

            found = False
            for i in range(0, 8):
                for j in range(0, 8):
                    if board.tiles[i][j] != '.' and self.internal_board[i][j] == '.':
                        oponent_last_move = (j, i)
                        #print("coluna: " + str(j) + " linha: " + str(i))
                        found = True
                        break
                if found:
                    break

            oponent_last_move_notation = self.move_to_notation(
                oponent_last_move[0], oponent_last_move[1], oponent_index)

            self.write_move_to_history(
                oponent_last_move_notation[0], oponent_last_move_notation[1])
            
            file = open(self.history_file, 'r+')
            self.history = file.read()
            file.close()
            

            

    def move_to_notation(self, column: int, row: int, index: int) -> str:
        black_columns = ["A", "B", "C", "D", "E", "F", "G", "H"]
        white_columns = ["a", "b", "c", "d", "e", "f", "g", "h"]

        notation_string = ""
        notation_string += (black_columns[column] if (index %
                            2 == 0) else white_columns[column]) + str(row+1)

        return notation_string

    def notation_to_move(self, c: str, r: str) -> tuple[int, int]:
        columns = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7,
                   "a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}

        return (columns[c], int(r)-1)

    def write_move_to_history(self, column, row):
        file = open(self.history_file, 'a')
        file.write(column)
        file.write(row)
        file.close()

    def get_next_move(self):
        if self.opening_is_over:
            return None

        if len(self.history) == 0:
            move = random.choice(openings)
            self.write_move_to_history(move[0], move[1])
            return self.notation_to_move(move[0], move[1])

        for opening in openings:
            if self.is_prefix(self.history, opening):
                self.write_move_to_history(
                    opening[len(self.history)], opening[len(self.history) + 1])
                return self.notation_to_move(opening[len(self.history)], opening[len(self.history) + 1])

        self.write_move_to_history('L', 'L')

    def is_prefix(self, s, w):
        if len(s) >= len(w):
            return False

        for i in range(0,len(s)):
            if s[i] != w[i]:
                return False

        return True

    def get_points_from_board(self, board: board.Board, agent_color: str) -> tuple[int, int]:
        """
        Returns a tuple (a,b) where a is the agent's points, and b is the opponent's points
        """
        oponent_color = board.opponent(agent_color)
        p1_score = sum([1 for char in str(board) if char == agent_color])
        p2_score = sum([1 for char in str(board) if char == oponent_color])

        return (p1_score, p2_score)
