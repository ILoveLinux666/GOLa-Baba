import sys

from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton


class DraggableWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Dodajemy tytuł i przyciski
        self.setWindowTitle("Menu")
        self.setGeometry(300, 300, 400, 400)
        self.setWindowFlags(Qt.FramelessWindowHint)  # Bez ramki
        self.setStyleSheet("background-color: #1e1e1e;")

        # Ustawienie tytułu
        title_label = QLabel("Game of Life")
        title_label.setFont(QFont("Comic Sans MS", 20, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: white; padding: 20px 0;")

        # nieudaaje mi sie pobrac fontu pikselowego :(
        # start
        start_button = QPushButton("Start")
        start_button.setFont(QFont("Comic Sans MS", 14))
        start_button.setStyleSheet(
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
        # menu
        menu_button = QPushButton("Menu")
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
        close_button.setFont(QFont("Comic Sans MS", 14))
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

        close_button.clicked.connect(app.quit)

        # przyciski
        button_layout = QVBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)
        button_layout.addWidget(start_button)
        button_layout.addSpacing(20)
        button_layout.addWidget(menu_button)
        button_layout.addSpacing(20)
        button_layout.addWidget(close_button)
        button_layout.addSpacing(40)

        # Główny
        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Do przechowywania pozycji myszy
        self.offset = QPoint()

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
