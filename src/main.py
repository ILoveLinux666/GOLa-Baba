import sys
from Board import Board
from PySide6.QtWidgets import QApplication

from window import DraggableWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    board: Board = Board()
    board.initialize_board()
    board.next_generation()
    for l in board.get_board():
        for cell in l:
            print(cell.state.value, end=" ")
        print()
    window = DraggableWindow(main_app=app)
    window.show()
    sys.exit(app.exec())
