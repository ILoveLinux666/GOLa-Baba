import os
import random

from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QFont, QFontDatabase, QPainter, QColor
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton

from Board import Board
from Game import GameOfLifeWindow


# TODO do upiększenia
def load_custom_font():
    font_path = os.path.join("assets", "fonts", "pixel.otf")
    font_id = QFontDatabase.addApplicationFont(font_path)
    if font_id == -1:
        print("Failed to load font.")
        return QFont("Arial", size)
    font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
    return QFont(font_family, size)


class PixelBackground(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pixel_size = 10
        self.setGeometry(parent.rect())
        self.pattern = self.generate_random_pattern()

    def generate_random_pattern(self):
        pattern = []
        width = self.width() // self.pixel_size
        height = self.height() // self.pixel_size

        for y in range(height):
            row = []
            for x in range(width):
                row.append(1 if random.random() < 0.05 else 0)
            pattern.append(row)
        return pattern

    def paintEvent(self, event):
        painter = QPainter(self)
        for y, row in enumerate(self.pattern):
            for x, val in enumerate(row):
                color = QColor("#2196f3") if val == 1 else QColor("#1e1e1e")
                painter.fillRect(
                    x * self.pixel_size,
                    y * self.pixel_size,
                    self.pixel_size,
                    self.pixel_size,
                    color,
                )



class DraggableWindow(QWidget):
    def __init__(self, main_app: QApplication):
        super().__init__()
        # Dodajemy tytuł i przyciski
        self.setWindowTitle("Options")
        self.setGeometry(300, 300, 400, 400)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: #1e1e1e;")

        self.pixel_font = load_custom_font(14)
        self.title_font = load_custom_font(24)
        self.setFont(self.pixel_font)

        # Ustawienie tytułu
        title_label = QLabel("Game of Life")
        title_label.setFont(self.pixel_font)
        # title_label.setFont(QFont("Comic Sans MS", 20, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: white; padding: 20px 0;")
        self.start_button = QPushButton("Start")
        self.start_button.setFont(QFont("Comic Sans MS", 14))
        self.start_button.setStyleSheet(
            """
            QPushButton {
                background-color: #00c853;
                color: white;
                padding: 10px 30px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #00e676;
            }
        """
        )
        self.start_button.clicked.connect(self.start_game)
        # menu
        menu_button = QPushButton("Options")
        menu_button.setFont(QFont("Comic Sans MS", 14))
        menu_button.setStyleSheet(
            """
            QPushButton {
                background-color: #f06292;
                color: white;
                padding: 10px 30px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #f48fb1;
            }
        """
        )

        # close
        close_button = QPushButton("Close")
        close_button.setFont(self.pixel_font)
        close_button.setStyleSheet(
            """
            QPushButton {
                background-color: #e53935;
                color: white;
                padding: 10px 30px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #ef5350;
            }
        """
        )

        close_button.clicked.connect(main_app.quit)

        # Przyciski

        button_layout = QVBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)
        button_layout.addWidget(self.start_button)
        button_layout.addSpacing(20)
        button_layout.addWidget(menu_button)
        button_layout.addSpacing(20)
        button_layout.addWidget(close_button)
        button_layout.addSpacing(40)

        # Główny layout
        layout = QVBoxLayout()
        button_layout.addSpacing(20)
        layout.addWidget(title_label)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        # Do przechowywania pozycji myszy
        self.offset = QPoint()

        # Dodanie tła z losowymi pikselami jako child widget
        self.pixel_background = PixelBackground(parent=self)
        self.pixel_background.lower()  # Umieszcza tło za innymi elementami

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = (
                event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            )
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self.offset)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.offset = QPoint()

    def start_game(self):
        board = Board()
        board.initialize_board()
        self.game_window = GameOfLifeWindow(board)
        self.game_window.show()
        self.game_window.start()
