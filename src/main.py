import sys

from PySide6.QtWidgets import QApplication

from Board import Board
from MenuWindow import DraggableWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    board: Board = Board()
    board.initialize_board()
    window = DraggableWindow(main_app=app)
    window.show()
    sys.exit(app.exec())
