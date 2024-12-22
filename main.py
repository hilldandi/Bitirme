from PyQt5.QtWidgets import QApplication
from screens.main_app import MainApp
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
