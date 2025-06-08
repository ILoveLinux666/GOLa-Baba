import sys

from PySide6.QtWidgets import QApplication

from MenuWindow import DraggableWindow
from src.Options import Options

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DraggableWindow(main_app=app)
    window.show()
    Options.load()
    print(Options.get_options())
    sys.exit(app.exec())
