from Cell import Cell


class Board:

    def __init__(self):
        self.board: list[list[Cell]] = []

    def initialize_board(self) -> list[list[Cell]]:
        self.board = [[Cell for _ in range(0, 99)] for _ in range(0, 99)]
        return board

    def get_board(self):
        return self.board
