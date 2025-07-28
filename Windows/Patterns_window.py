# coding=utf-8

import sqlite3

from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QIcon, QPixmap

from Windows_design_python.Pattern_window_design import Ui_Pattern_window_design
from Devices.Arduino.arduino_connection import *
from other.Other.scramble import *


class PatternsWindow(QMainWindow, Ui_Pattern_window_design):
    def __init__(self, par):
        super().__init__()
        self.parent = par
        self.current_algorithm = "R L' F B' U D' R L'".split()
        self.solved_pattern = None
        self.initUI()

    def initUI(self):
        self.setupUi(self)

        self.__setup_window__()
        self.__connect__()

    def __setup_window__(self):
        self.setWindowTitle("Cubing Robot")
        self.setWindowIcon(QIcon("images/logo/cubing_robot_logo_icon.png"))

        self.patter_label.setPixmap(QPixmap("images/patterns/uz0.png"))
        self.pattern_formula_label.setText("R L' F B' U D' R L'")
        self.motor_speed_spin_box.setValue(99)

    def __set_parent_position__(self):
        main_window_position = self.parent.pos()
        self.move(main_window_position.x(), main_window_position.y())

    def __connect__(self):
        self.main_button.clicked.connect(self.__open_main_window__)
        self.patter_list_combo_box.currentIndexChanged.connect(self.__change_pattern__)

        self.solve_button.clicked.connect(self.__send_algorithm__)
        self.return_to_solved_state_btn.clicked.connect(self.__return_to_solved_state__)

    def __open_main_window__(self):
        self.hide()
        self.parent.show()
        self.parent.__set_other_position__(self.pos())

    def __change_pattern__(self):
        with sqlite3.connect("databases/cube_patterns_data.sqlite") as connection:
            cursor = connection.cursor()

            query = f"""SELECT * FROM patterns WHERE name = '{self.patter_list_combo_box.currentText()}'"""
            result = cursor.execute(query)
            pattern = ()
            for i in result:
                pattern = i
            self.patter_label.setPixmap(QPixmap(pattern[1]))
            self.pattern_formula_label.setText(i[2])
            self.current_algorithm = i[2].split()

    def __send_algorithm__(self):
        if not arduino.check_connection():
            self.statusbar.setStyleSheet("background: red")
            self.statusbar.showMessage("Робот не подключён!")
        elif self.current_algorithm[0] == 'В':
            self.statusbar.setStyleSheet("background: red")
            self.statusbar.showMessage("Данный узор находится в разработке!")
        else:
            self.statusbar.setStyleSheet("")
            self.statusbar.showMessage("")
            arduino.set_motors_speed(255 - int(self.motor_speed_spin_box.text()))
            arduino.send_message(list(map(str, self.current_algorithm)))
            self.solved_pattern = list(map(str, self.current_algorithm))

    def __return_to_solved_state__(self):
        if not arduino.check_connection():
            self.statusbar.setStyleSheet("background: red")
            self.statusbar.showMessage("Робот не подключён!")
        elif self.solved_pattern is None:
            self.statusbar.setStyleSheet("background: red")
            self.statusbar.showMessage("Никакой узор не собран!")
        else:
            self.statusbar.setStyleSheet("")
            self.statusbar.showMessage("")
            arduino.set_motors_speed(255 - int(self.motor_speed_spin_box.text()))
            arduino.send_message(reverse_algorithm(self.solved_pattern))