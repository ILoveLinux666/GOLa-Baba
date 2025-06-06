from PySide6.QtCore import Qt, QPoint
from PySide6.QtWidgets import QWidget, QVBoxLayout


class GameWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Game Window")
        self.setGeometry(300, 300, 400, 400)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet("background-color:  #000; color: white;")
        layout = QVBoxLayout()
        self.setLayout(layout)

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
