import random
from ..othello import board
from .openingList import openings

from pyparsing import col


class OpeningBook:

    def __init__(self, board: board.Board, agent_color: str):
        self.history = ""
        self.history_file = "r2d2_move_history_file_dont_touch_it_is_art.txt"
        self.opening_is_over = False
        self.internal_board = [['.'] * 8 for i in range(8)]

        self.internal_board[3][3] = self.internal_board[4][3] = self.internal_board[3][4] = self.internal_board[4][4] = 'B'

        p1, p2 = self.get_points_from_board(board, agent_color)

        # create file if it does not exist yet
        file = open(self.history_file, 'a+')
        file.close()

        file = open(self.history_file, 'r+')

        if p1 + p2 == 4 or (p1+p2 == 5 and agent_color == 'W'):  
            # we know the game is starting now, therefore we must erase the file from any previous game
            file.truncate(0)
        else:
            self.history = file.read()

        file.close()

        if len(self.history) or agent_color == 'W':  # then we know that our oponent has to have made a move last time
            # L means that we know we are not in the opening anymore
            if len(self.history) and self.history[-1] == 'L':
                self.opening_is_over = True
                return

            # fills the board untill the last move made by our agent
            for i in range(0, len(self.history), 2):
                column, row = self.notation_to_move(
                    self.history[i], self.history[i+1])
                self.internal_board[row][column] = 'B'

            oponent_last_move = (-1, -1)
            oponent_index = 1 if agent_color == 'B' else 0

            # finds out what was the move made by our oponent last time by checking the difference between boards
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

            # add to our history the oponent move
            self.write_move_to_history(
                oponent_last_move_notation[0], oponent_last_move_notation[1])

            self.history += oponent_last_move_notation[0]
            self.history += oponent_last_move_notation[1]

    def move_to_notation(self, column: int, row: int, index: int) -> str:
        columns = ["a", "b", "c", "d", "e", "f", "g", "h"]

        notation_string = ""
        notation_string += columns[column] + str(row+1)

        return notation_string

    def notation_to_move(self, c: str, r: str) -> tuple[int, int]:
        columns = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}

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

        continuations = []

        for opening in openings:
            if self.is_prefix(self.history, opening):
                continuations.append(opening)

        if len(continuations):
            opening = random.choice(continuations)
            self.write_move_to_history(
                opening[len(self.history)], opening[len(self.history) + 1])
            return self.notation_to_move(opening[len(self.history)], opening[len(self.history) + 1])

        self.write_move_to_history('L', 'L')

    def is_prefix(self, s, w):
        if len(s) >= len(w):
            return False

        for i in range(0, len(s)):
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
