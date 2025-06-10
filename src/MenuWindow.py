import json
import os
import random

from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QFont, QFontDatabase, QPainter, QColor
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QComboBox,
    QSlider,
)

from Board import Board
from Game import GameOfLifeWindow


# TODO do upiększenia
def load_custom_font(size=14):
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
            row = [1 if random.random() < 0.05 else 0 for _ in range(width)]
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


class OptionsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Opcje")
        self.setGeometry(400, 400, 300, 220)
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: #121212; color: white;")

        font = load_custom_font(14)

        layout = QVBoxLayout()
        speed_label = QLabel("Speed:")
        speed_label.setFont(font)
        layout.addWidget(speed_label)

        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setRange(25, 1000)
        self.speed_slider.setValue(50)
        self.speed_slider.setStyleSheet(
            """
            QSlider::groove:horizontal {
                height: 6px;
                background: #333;
            }
            QSlider::handle:horizontal {
                background: #2196f3;
                border: 1px solid #1e88e5;
                width: 14px;
                margin: -5px 0;
                border-radius: 7px;
            }
            """
        )
        layout.addWidget(self.speed_slider)

        size_label = QLabel("Plansza:")
        size_label.setFont(font)
        layout.addWidget(size_label)

        self.size_combo = QComboBox()
        self.size_combo.setFont(font)
        self.size_combo.setStyleSheet(
            "background-color: #333; color: white; padding: 5px;"
        )
        self.size_combo.addItems(["100x200", "300x500", "400x600"])
        layout.addWidget(self.size_combo)

        pixel_label = QLabel("Pixel: ")
        pixel_label.setFont(font)
        layout.addWidget(pixel_label)

        self.pixel_combo = QComboBox()
        self.pixel_combo.setFont(font)
        self.pixel_combo.setStyleSheet(
            "background-color: #333; color: white; padding: 5px;"
        )
        self.pixel_combo.addItems(["10", "20", "30"])
        layout.addWidget(self.pixel_combo)

        save_button = QPushButton("Zapisz")
        save_button.setFont(font)
        save_button.setStyleSheet(
            """
            QPushButton {
                background-color: #2196f3;
                color: white;
                padding: 8px 20px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #42a5f5;
            }
        """
        )
        save_button.clicked.connect(self.save_config)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def save_config(self):
        size_text = self.size_combo.currentText().strip()
        pixel_text = self.pixel_combo.currentText().strip()
        speed_value = self.speed_slider.value()
        try:
            if "x" in size_text:
                width, height = map(int, size_text.split("x"))
            else:
                width, height = 100, 100

            cell_size = int(pixel_text)
            config = {
                "size": [width, height],
                "cell_size": cell_size,
                "speed": speed_value,
            }

            with open("config.json", "w", encoding="utf-8") as f:
                json.dump(config, f, indent=4)

        except Exception as e:
            print("Błąd podczas zapisu konfiguracji:", e)

        self.close()


class DraggableWindow(QWidget):
    def __init__(self, main_app: QApplication):
        super().__init__()
        self.setWindowTitle("Options")
        self.setGeometry(300, 300, 400, 400)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: transparent;")

        self.pixel_font = load_custom_font(14)
        self.title_font = load_custom_font(30)
        self.setFont(self.pixel_font)

        title_label = QLabel("Game of Life")
        title_label.setFont(self.title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: white; padding: 10px 0;")

        self.start_button = QPushButton("Start")
        self.start_button.setFont(self.pixel_font)
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
        menu_button.setFont(self.pixel_font)
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
        menu_button.clicked.connect(self.show_options)

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

        button_layout = QVBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)
        button_layout.addWidget(self.start_button)
        button_layout.addSpacing(20)
        button_layout.addWidget(menu_button)
        button_layout.addSpacing(20)
        button_layout.addWidget(close_button)
        button_layout.addSpacing(40)

        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.offset = QPoint()
        self.pixel_background = PixelBackground(parent=self)
        self.pixel_background.lower()

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
        width, height = 100, 100
        cell_size = 10
        speed = 50
        try:
            with open("config.json", "r", encoding="utf-8") as f:
                config = json.load(f)
                print("Wczytany config:", config)
                if "size" in config and len(config["size"]) == 2:
                    width, height = config["size"]
                if "cell_size" in config and type(config["cell_size"]) == int:
                    cell_size = config["cell_size"]
                    if "speed" in config and isinstance(config["speed"], int):
                        speed = config["speed"]
        except Exception as e:
            print("Błąd podczas w wczytaniu oplika", e)
        print(f"jest plansza: {width}x{height}")
        board = Board()
        board.initialize_board()
        self.game_window = GameOfLifeWindow(
            board=board, cell_size=cell_size, size_x=width, size_y=height
        )
        self.game_window.show()
        self.game_window.start_simulation()


    def show_options(self):
        self.options_window = OptionsWindow()
        self.options_window.show()
