from PySide6.QtCore import QTimer, Qt, QPoint
from PySide6.QtGui import QPainter, QColor
from PySide6.QtWidgets import QWidget, QSlider, QVBoxLayout

# Assume Board and Cell are defined elsewhere and imported
# Board.get_board() -> dict[(int, int), Cell]
# Board.next_generation() updates board state
from Board import Board  # adjust import path as needed


class GameCanvas(QWidget):
    def __init__(self, board: Board, cell_size: int = 10):
        super().__init__()
        self.board = board
        self.cell_size = cell_size
        self.offset = QPoint(0, 0)
        self.last_mouse_pos = None
        self.setCursor(Qt.OpenHandCursor)
        self.setMinimumSize(100, 100)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.fillRect(self.rect(), QColor("white"))
        painter.translate(self.offset)
        for (x, y), cell in self.board.get_board().items():
            painter.fillRect(
                x * self.cell_size,
                y * self.cell_size,
                self.cell_size,
                self.cell_size,
                QColor("black"),
            )
        painter.end()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_mouse_pos = event.pos()
            self.setCursor(Qt.ClosedHandCursor)

    def mouseMoveEvent(self, event):
        if self.last_mouse_pos is not None:
            self.offset += event.pos() - self.last_mouse_pos
            self.last_mouse_pos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_mouse_pos = None
            self.setCursor(Qt.OpenHandCursor)


class GameOfLifeWindow(QWidget):

    def __init__(self, board: Board, cell_size: int = 10, update_interval: int = 200, size_x: int = 300, size_y: int = 300):
        super().__init__()
        self.board = board
        self.cell_size = cell_size
        self.setWindowTitle("Game of Life — Whiteboard View")

        # Canvas
        self.canvas = GameCanvas(board, cell_size)

        # Timer for stepping generations
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._next_generation)
        self.timer.setInterval(update_interval)

        # Speed slider
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setRange(25, 1000)  # ms per generation
        self.speed_slider.setValue(update_interval)
        self.speed_slider.setToolTip("ms per generation")
        self.speed_slider.valueChanged.connect(self.timer.setInterval)

        # Layout: canvas above, slider below
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvas)
        layout.addWidget(self.speed_slider)
        self.resize(size_x, size_y)

    def start(self):
        """Start the simulation timer."""
        if not self.timer.isActive():
            self.timer.start()

    def _next_generation(self):
        self.board.next_generation()
        self.canvas.update()
