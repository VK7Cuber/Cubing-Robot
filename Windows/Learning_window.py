# coding=utf-8

import sqlite3

from PySide6.QtWidgets import QMainWindow

from Windows_design_python.Learning_window_TRY_1 import Learning
from Devices.Arduino.arduino_connection import *


class LearningWindow(QMainWindow, Learning):
    def __init__(self, par):
        super().__init__()
        self.parent = par
        self.initUI()

    def initUI(self):
        self.setupUi(self)

        self.main_button.clicked.connect(self.__open_main_window__)

        self.base_algorithm_showing_button.clicked.connect(self.send_base)

        self.comboBox_2.currentIndexChanged.connect(self.__change_type_of_scanning__)
        # self.CFOP_algorithm_showing_butto.clicked.connect(self.send)
        self.stackedWidget_2.setCurrentIndex(0)

    def __change_type_of_scanning__(self):
        self.stackedWidget_2.setCurrentIndex(self.comboBox_2.currentIndex())

    def send_base(self):
        self.statusbar.showMessage("")
        self.statusbar.setStyleSheet("")
        try:
            with sqlite3.connect("databases/Base_method_algorithms_data.sqlite") as connection:
                cursor = connection.cursor()

                query = f"""SELECT * FROM Algorithms WHERE id = {self.base_algorithm_showing_box.currentIndex()}"""
                result = cursor.execute(query)
                pattern = ()
                for i in result:
                    pattern = i
                arduino.set_motors_speed(205)
                arduino.send_message(list(map(str, pattern[1].split())))
        except:
            self.statusbar.showMessage("Робот не подключен!")
            self.statusbar.setStyleSheet("background: red")

    def __open_main_window__(self):
        self.hide()
        self.parent.show()
        self.parent.__set_other_position__(self.pos())