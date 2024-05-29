import sys
from PyQt6.QtWidgets import QApplication
from ui_manager import UIManager

class App(QApplication):
    def __init__(self, argv):
        super().__init__(argv)

        self.ui_manager = UIManager()  # Instantiate the UIManager class
        self.ui_manager.show()  # Show the main window

if __name__ == "__main__":
    app = App(sys.argv)
    sys.exit(app.exec())
