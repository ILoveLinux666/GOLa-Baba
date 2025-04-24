from Cell import Cell
from State import State


class Board:

    def __init__(self):
        self.board: list[list[Cell]] = []

    def initialize_board(self) -> list[list[Cell]]:
        self.board = [[Cell() for _ in range(0, 20)] for _ in range(0, 20)]
        return self.board

    def get_board(self) -> list[list[Cell]]:
        """Zwraca dwuwymiarową tablicę komórek"""
        return self.board

    def next_generation(self):
        """Tworzy nową tablicę sprawdza warunki i przypisuje do starej tablicy"""
        next_board: list[list[Cell]] = [
            [Cell() for _ in range(0, len(self.board))]
            for _ in range(0, len(self.board))
        ]
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                # Tymczasowe ustawienie granicy
                if i == 0 or i == len(row) - 1 or j == 0 or j == len(self.board) - 1:
                    next_board[i][j] = Cell(State.ALIVE)
                else:
                    sum = (
                        self.board[i - 1][j - 1].state.value
                        + self.board[i - 1][j].state.value
                        + self.board[i - 1][j + 1].state.value
                        + self.board[i][j - 1].state.value
                        + self.board[i][j + 1].state.value
                        + self.board[i + 1][j - 1].state.value
                        + self.board[i + 1][j].state.value
                        + self.board[i + 1][j + 1].state.value
                    )
                    if cell.state == State.DEAD and sum == 3:
                        next_board[i][j] = Cell(State.ALIVE)
                    if cell.state == State.ALIVE and not (sum == 2 or sum == 3):
                        next_board[i][j] = Cell(State.DEAD)
        self.board.clear()
        self.board = next_board
