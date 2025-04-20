import sys

from PySide6.QtWidgets import QApplication

from Windows.Main_window import MainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    cubing_robot = MainWindow()
    cubing_robot.show()
    sys.exit(app.exec())
