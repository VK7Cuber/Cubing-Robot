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
        self.connected_picture = QPixmap("images/logo/cubing_robot_connected.png")
        self.disconnected_picture = QPixmap("images/logo/cubing_robot_disconnected.png")
        self.themes = {0: ["light", "Светлая", QPixmap("images/logo/cubing_robot_logo_black.png")],
                       1: ["dark", "Тёмная", QPixmap("images/logo/cubing_robot_logo_white.png")]}
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
        self.setWindowIcon(QIcon("images/logo/cubing_robot_logo_ico.png"))
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

    def __resize_windows__(self):
        self.solving_window.resize(QSize(650, 600))
        for window in self.windows[:1]:
            window.resize(window.minimumSize())

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
            self.solving_window.is_connected_label.setPixmap(self.connected_picture)
            self.manual_turns_window.is_connected_label.setPixmap(self.connected_picture)
            self.scramble_window.is_connected_label.setPixmap(self.connected_picture)
            self.pattern_window.is_connected_label.setPixmap(self.connected_picture)
        else:
            self.solving_window.is_connected_label.setPixmap(self.disconnected_picture)
            self.manual_turns_window.is_connected_label.setPixmap(self.disconnected_picture)
            self.scramble_window.is_connected_label.setPixmap(self.disconnected_picture)
            self.pattern_window.is_connected_label.setPixmap(self.disconnected_picture)
        # self.timer.start(100)

    def __change_theme__(self):
        self.current_theme = 1 - self.current_theme
        qdarktheme.setup_theme(self.themes[self.current_theme][0])
        self.theme_button.setText(f"{self.themes[self.current_theme][1]}")
        self.logo_label.setPixmap(self.themes[self.current_theme][2])
