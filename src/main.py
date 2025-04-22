import sys

from PySide6.QtWidgets import QApplication

from window import DraggableWindow

if __name__ == "__main__":
    # Uruchomienie aplikacji
    app = QApplication(sys.argv)

    window = DraggableWindow(main_app=app)
    window.show()
    sys.exit(app.exec())
