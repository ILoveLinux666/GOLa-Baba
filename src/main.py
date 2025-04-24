import sys
from Board import Board
from PySide6.QtWidgets import QApplication

from window import DraggableWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    board: Board = Board()
    board.initialize_board()
    for pos, cell in board.get_board().items():
        print(f"{pos} - {cell}")
    print("="*40)
    board.next_generation()
    for pos, cell in board.get_board().items():
        print(f"{pos} - {cell}")
    window = DraggableWindow(main_app=app)
    window.show()
    sys.exit(app.exec())
