import sys

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from Main_window_design import Ui_Main_Window_design
from Solving_window_design import Ui_solving_window_design

#from rubik_solver import utils

class Main_Window(QMainWindow, Ui_Main_Window_design):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.setupUi(self)

        self.__setup_window__()
        self.__make_windows__()
        self.__connect_buttons__()
        self.put_logo()

    def __setup_window__(self):
        self.setWindowTitle("Cubing Robot")
        self.setGeometry(550, 200, 400, 400)
    def put_logo(self):
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo_label.setPixmap(QPixmap("images/cubing_robot_logo.png"))


    def __make_windows__(self):
        self.solving_window = Solving_window(self)
        self.solving_window.hide()

        self.pattern_window = Pattern_window(self)
        self.pattern_window.hide()

        self.learning_window = Learning_window(self)
        self.learning_window.hide()

        self.reference_window = Reference_window(self)
        self.reference_window.hide()
    def __connect_buttons__(self):
        self.solving_button.clicked.connect(self.__open_solving_window__)
        self.pattern_button.clicked.connect(self.__open_patter_window__)
        self.learning_button.clicked.connect(self.__open_learning_window__)
        self.reference_button.clicked.connect(self.__open_reference_window__)

    def __open_solving_window__(self):
        self.solving_window.show()
        self.solving_window.__set_parent_position__()
        self.hide()
    def __open_patter_window__(self):
        self.pattern_window.show()
        self.hide()
    def __open_learning_window__(self):
        self.learning_window.show()
        self.hide()
    def __open_reference_window__(self):
        self.reference_window.show()
        self.hide()

    def __set_other_position__(self, position):
        self.move(position.x(), position.y())


class Solving_window(QMainWindow, Ui_solving_window_design):
    def __init__(self, par):
        super().__init__()
        self.parent = par
        self.initUI()
    def initUI(self):
        self.setupUi(self)

        self.__setup_window__()
        self.__connect_buttons__()

    def __setup_window__(self):
        self.setWindowTitle("Cubing Robot")
        self.begginer_method_rb.setChecked(True)
        self.motor_speed_spinbox.setValue(99)

    def __set_parent_position__(self):
        main_window_position = self.parent.pos()
        self.move(main_window_position.x(), main_window_position.y())


    def __connect_buttons__(self):
        self.main_button.clicked.connect(self.__open_main_window__)

    def __open_main_window__(self):
        self.hide()
        self.parent.show()
        self.parent.__set_other_position__(self.pos())



class Pattern_window(QMainWindow, Ui_solving_window_design):
    def __init__(self, par):
        super().__init__()
        self.parent = par
        self.initUI()
    def initUI(self):
        self.setupUi(self)

class Learning_window(QMainWindow, Ui_solving_window_design):
    def __init__(self, par):
        super().__init__()
        self.parent = par
        self.initUI()
    def initUI(self):
        self.setupUi(self)

class Reference_window(QMainWindow, Ui_solving_window_design):
    def __init__(self, par):
        super().__init__()
        self.parent = par
        self.initUI()
    def initUI(self):
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    cubing_robot = Main_Window()
    cubing_robot.show()
    sys.exit(app.exec())