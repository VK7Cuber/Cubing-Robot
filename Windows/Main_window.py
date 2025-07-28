# coding=utf-8

from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt, QTimer, QSize

from Windows_design_python.Main_window_design import Ui_Main_Window_design

from Windows.Solving_window import SolvingWindow
from Windows.Scramble_window import ScrambleWindow
from Windows.Manual_turns_window import ManualTurnsWindow
from Windows.Patterns_window import PatternsWindow
from Windows.Learning_window import LearningWindow
from Windows.Reference_window import ReferenceWindow

from Devices.Arduino.arduino_connection import *

import qdarktheme


class MainWindow(QMainWindow, Ui_Main_Window_design):
    def __init__(self):
        super().__init__()
        self.timer = QTimer()

        self.is_connected_pictures = {True: QPixmap("images/logo/cubing_robot_connected.png"),
                                      False: QPixmap("images/logo/cubing_robot_disconnected.png")}

        self.themes = [["light", "Светлая", QPixmap("images/logo/cubing_robot_logo_black.png")],
                       ["dark", "Тёмная", QPixmap("images/logo/cubing_robot_logo_white.png")]]
        self.current_theme = 0
        self.initUI()

    def initUI(self):
        self.setupUi(self)

        self.__setup_window__()
        self.__make_windows__()
        self.__connect__()
        self.put_logo()

    def __setup_window__(self):
        self.setWindowTitle("Cubing Robot")
        self.setGeometry(550, 200, 400, 400)
        self.setWindowIcon(QIcon("images/logo/cubing_robot_logo_icon.png"))
        qdarktheme.setup_theme("light")

    def put_logo(self):
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo_label.setPixmap(self.themes[0][2])

    def __make_windows__(self):
        self.solving_window = SolvingWindow(self)
        self.solving_window.hide()

        self.scramble_window = ScrambleWindow(self)
        self.scramble_window.hide()

        self.manual_turns_window = ManualTurnsWindow(self)
        self.manual_turns_window.hide()

        self.pattern_window = PatternsWindow(self)
        self.pattern_window.hide()

        self.learning_window = LearningWindow(self)
        self.learning_window.hide()

        self.reference_window = ReferenceWindow(self)
        self.reference_window.hide()

        self.windows = [self.solving_window, self.scramble_window, self.manual_turns_window,
                        self.pattern_window, self.learning_window, self.reference_window]

        self.__resize_windows__()

    def __resize_windows__(self):
        self.solving_window.resize(QSize(650, 600))
        for index in range(1, 5):
            self.windows[index].resize(self.windows[index].minimumSize())

    def __connect__(self):
        self.solving_button.clicked.connect(self.__open_solving_window__)
        self.scramble_button.clicked.connect(self.__open_scramble_window__)
        self.manual_turns_button.clicked.connect(self.__open_manual_turns_window__)
        self.pattern_button.clicked.connect(self.__open_patter_window__)
        self.learning_button.clicked.connect(self.__open_learning_window__)
        self.reference_button.clicked.connect(self.__open_reference_window__)
        self.theme_button.clicked.connect(self.__change_theme__)

        self.timer.timeout.connect(self.__check_connection__)
        self.timer.start()

    def __open_solving_window__(self):
        self.solving_window.show()
        self.solving_window.__set_parent_position__()
        self.hide()

    def __open_scramble_window__(self):
        self.scramble_window.show()
        self.scramble_window.__set_parent_position__()
        self.scramble_window.is_showing = True
        self.hide()

    def __open_manual_turns_window__(self):
        self.manual_turns_window.show()
        self.manual_turns_window.__set_parent_position__()
        self.hide()

    def __open_patter_window__(self):
        self.pattern_window.show()
        self.pattern_window.__set_parent_position__()
        self.hide()

    def __open_learning_window__(self):
        self.learning_window.show()
        self.hide()

    def __open_reference_window__(self):
        self.reference_window.show()
        self.hide()

    def __set_other_position__(self, position):
        self.move(position.x(), position.y())

    def __check_connection__(self):
        arduino_port = find_arduino()
        if arduino_port is not None:
            self.__change_connected_picture__(True)
            if not arduino.check_connection():
                try:
                    arduino.connect_arduino(arduino_port)
                except:
                    pass
        else:
            self.__change_connected_picture__(False)
            if arduino.check_connection():
                arduino.disconnect()

    def __change_connected_picture__(self, is_connected):
        # Сделать через цикл for, когда допишу окна:
        self.solving_window.is_connected_label.setPixmap(self.is_connected_pictures[is_connected])
        self.manual_turns_window.is_connected_label.setPixmap(self.is_connected_pictures[is_connected])
        self.scramble_window.is_connected_label.setPixmap(self.is_connected_pictures[is_connected])
        self.pattern_window.is_connected_label.setPixmap(self.is_connected_pictures[is_connected])

    def __change_theme__(self):
        self.current_theme = 1 - self.current_theme
        qdarktheme.setup_theme(self.themes[self.current_theme][0])
        self.theme_button.setText(f"{self.themes[self.current_theme][1]}")
        self.logo_label.setPixmap(self.themes[self.current_theme][2])
