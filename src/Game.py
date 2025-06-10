from State import State
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
        self.drawing_mode = True
        self.is_mouse_down = False
        self.right_mouse_down = False
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
        if self.drawing_mode:
            if event.button() == Qt.LeftButton:
                self.is_mouse_down = True
                self._add_cell_from_mouse(event.pos())
                self.setCursor(Qt.CrossCursor)
            elif event.button() == Qt.RightButton:
                self.right_mouse_down = True
                self._remove_cell_from_mouse(event.pos())
                self.setCursor(Qt.ForbiddenCursor)
        elif not self.drawing_mode and event.button() == Qt.LeftButton:
            self.last_mouse_pos = event.pos()
            self.setCursor(Qt.ClosedHandCursor)

    def mouseMoveEvent(self, event):
        if self.drawing_mode:
            if self.is_mouse_down:
                self._add_cell_from_mouse(event.pos())
            elif self.right_mouse_down:
                self._remove_cell_from_mouse(event.pos())
        elif not self.drawing_mode and self.last_mouse_pos is not None:
            self.offset += event.pos() - self.last_mouse_pos
            self.last_mouse_pos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if self.drawing_mode:
            if event.button() == Qt.LeftButton:
                self.is_mouse_down = False
                self.setCursor(Qt.CrossCursor)
            elif event.button() == Qt.RightButton:
                self.right_mouse_down = False
                self.setCursor(Qt.CrossCursor)
        elif not self.drawing_mode and event.button() == Qt.LeftButton:
            self.last_mouse_pos = None
            self.setCursor(Qt.OpenHandCursor)

    def _add_cell_from_mouse(self, pos):
        x = (pos.x() - self.offset.x()) // self.cell_size
        y = (pos.y() - self.offset.y()) // self.cell_size
        self.board.insert_cell(x, y)
        self.update()

    def _remove_cell_from_mouse(self, pos):
        x = (pos.x() - self.offset.x()) // self.cell_size
        y = (pos.y() - self.offset.y()) // self.cell_size
        self.board.delete_cell(x, y)
        self.update()

    def set_drawing_mode(self, enabled: bool):
        self.drawing_mode = enabled
        if enabled:
            self.setCursor(Qt.CrossCursor)
        else:
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

        # Start button
        self.start_button = QPushButton("Start Simulation")
        self.start_button.clicked.connect(self.start)

        # Layout: canvas, controls (slider + button)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvas)
        layout.addWidget(self.speed_slider)
        self.resize(size_x, size_y)
        controls = QHBoxLayout()
        controls.addWidget(self.speed_slider)
        controls.addWidget(self.start_button)
        layout.addLayout(controls)
        
    def start_simulation(self):
        self.canvas.set_drawing_mode(True)
        self.start_button.setEnabled(True)

    def start(self):
        """Start the simulation timer."""
        self.canvas.set_drawing_mode(False)
        self.start_button.setEnabled(False)
        if not self.timer.isActive():
            self.timer.start()

    def _next_generation(self):
        self.board.next_generation()
        self.canvas.update()
