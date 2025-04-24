from Cell import Cell
from State import State


class Board:

    def __init__(self):
        self.board: dict[tuple[int, int], Cell] = {}

    def initialize_board(self) -> dict[tuple[int, int], Cell]:
        """Tworzy glider do testów"""
        self.board[(8, 7)] = Cell(State.ALIVE)
        self.board[(9, 8)] = Cell(State.ALIVE)
        self.board[(10, 8)] = Cell(State.ALIVE)
        self.board[(10, 7)] = Cell(State.ALIVE)
        self.board[(10, 6)] = Cell(State.ALIVE)

        return self.board

    def get_board(self) -> dict[tuple[int, int], Cell]:
        """Zwraca mapę żywych komórek"""
        return self.board

    def check_neighbours(
        self,
        target_cell: Cell,
        cell_pos: tuple[int, int],
        depth: int,
        new_gen_cells: dict[tuple[int, int], Cell],
    ):
        if depth < 2:
            n_of_alive = 0
            for y in (-1, 0, 1):
                for x in (-1, 0, 1):
                    if y == 0 and x == 0:
                        continue
                    if neighbour := self.board.get(
                        (cell_pos[0] + x, cell_pos[1] + y), Cell()
                    ):
                        # print(f"({cell_pos[0] + x},{cell_pos[1] + y}) - {neighbour}")
                        self.check_neighbours(
                            neighbour,
                            (cell_pos[0] + x, cell_pos[1] + y),
                            depth + 1,
                            new_gen_cells,
                        )
                        if neighbour.state == State.ALIVE:
                            n_of_alive += 1
            if target_cell.state == State.DEAD and n_of_alive == 3:
                new_gen_cells[cell_pos] = Cell(State.ALIVE)
            if target_cell.state == State.ALIVE and (
                n_of_alive == 2 or n_of_alive == 3
            ):
                new_gen_cells[cell_pos] = Cell(State.ALIVE)

    def next_generation(self):
        """Tworzy nową mapę sprawdza warunki i wpisuje żywe komórki do nowej tablicy"""
        new_gen_cells: dict[tuple[int, int], Cell] = {}
        for pos, cell in self.board.items():
            self.check_neighbours(
                target_cell=cell, cell_pos=pos, depth=0, new_gen_cells=new_gen_cells
            )

        self.board = new_gen_cells
