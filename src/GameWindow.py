from PySide6.QtWidgets import QWidget, QVBoxLayout


class GameWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Game Window")
        self.setGeometry(300, 300, 250, 150)
        self.setStyleSheet("background-color:  #000; color: white;")
        layout = QVBoxLayout()
        self.setLayout(layout)

    def start_game(self):
        self.game_window = GameWindow()
        self.game_window.show()
        self.close()
