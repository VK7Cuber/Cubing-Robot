# coding=utf-8

import sqlite3

from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QIcon

from Windows_design_python.Solving_window_design import Ui_Solving_window_design
from Devices.Arduino.arduino_connection import *
from other.Other.scramble import *

from rubik_solver import utils


class SolvingWindow(QMainWindow, Ui_Solving_window_design):
    def __init__(self, par):
        super().__init__()
        self.parent = par
        self.error_message = ""
        self.count_of_clicks = 0
        self.initUI()

        self.rubiks_cube = 'yyyyyyyyybbbbbbbbbrrrrrrrrrgggggggggooooooooowwwwwwwww'

    def initUI(self):
        self.setupUi(self)

        self.__setup_window__()
        self.__connect__()

    def __setup_window__(self):
        self.setWindowTitle("Cubing Robot")
        self.setWindowIcon(QIcon("images/logo/cubing_robot_logo_ico.png"))

        self.stackedWidget.setCurrentIndex(0)
        self.begginer_method_rb.setChecked(True)
        self.set_motor_speed_spinbox_1.setValue(99)
        self.set_motor_speed_spinbox_2.setValue(99)

        self.button_colors = ["#ffffff", "#008000", "#ffa500", "#0000ff", "#ff0000", "#ffff00"]
        self.button_colors_names = ['w', 'g', 'o', 'b', 'r', 'y']

    def __set_parent_position__(self):
        main_window_position = self.parent.pos()
        self.move(main_window_position.x(), main_window_position.y())

    def __connect__(self):
        self.main_button.clicked.connect(self.__open_main_window__)

        self.solve_button_2.clicked.connect(self.__make_assambling_algorithm__)

        self.save_scramble_button.clicked.connect(self.__save_scramble__)

        self.open_last_scramble_button.clicked.connect(self.__open_last_scramble__)

        self.change_type_of_scanning_combo_box.currentIndexChanged.connect(self.__change_type_of_scanning__)
        self.buttonGroup.buttonClicked.connect(self.__change_button_color__)

    def __open_main_window__(self):
        self.hide()
        self.parent.show()
        self.parent.__set_other_position__(self.pos())

    def __change_type_of_scanning__(self):
        self.stackedWidget.setCurrentIndex(self.change_type_of_scanning_combo_box.currentIndex())

    def __change_button_color__(self, button):
        color = button.palette().window().color().name()
        index = self.button_colors.index(color) + 1
        if index > 5:
            index = 0
        button.setStyleSheet(f"background: {self.button_colors[index]};")

        configuration_index = button.objectName()[-2:]
        if configuration_index[0] == "_":
            configuration_index = configuration_index[1]
        configuration_index = int(configuration_index)
        self.rubiks_cube = self.rubiks_cube[:configuration_index] + self.button_colors_names[index] + self.rubiks_cube[
                                                                                                      configuration_index + 1:]

    def __make_assambling_algorithm__(self):
        self.error_message = "Введена неверная конфигурация кубика! Проверьте правильность расположения цветов!"
        try:
            self.statusbar.showMessage("")
            self.statusbar.setStyleSheet("")
            # assembling_algorithm = str(utils.solve(self.rubiks_cube, "Kociemba"))[1:-1]
            assembling_algorithm = []
            if self.rubiks_cube != 'yyyyyyyyybbbbbbbbbrrrrrrrrrgggggggggooooooooowwwwwwwww':
                assembling_algorithm = utils.solve(self.rubiks_cube, "Kociemba")
            # Ссылку не трогаем --> print(make_link(assembling_algorithm))
            self.count_of_movements_label_2.setText(str(len(assembling_algorithm)))
            assambling_algorithm_string = str(assembling_algorithm)[1: -1]
            self.assembling_algorithm_label_2.setText(assambling_algorithm_string)
            self.send_assembling_algorithm(assembling_algorithm)
        except:
            self.statusbar.showMessage(self.error_message)
            self.statusbar.setStyleSheet("background: #ff0000")

    def send_assembling_algorithm(self, algorithm):
        self.error_message = "Робот не подключён!"
        if arduino.check_connection():
            self.statusbar.showMessage("")
            self.statusbar.setStyleSheet("")
            arduino.set_motors_speed(255 - ((int(self.set_motor_speed_spinbox_2.text())) + 1))
            arduino.send_message(list(map(str, algorithm)))
        else:
            self.statusbar.showMessage(self.error_message)
            self.statusbar.setStyleSheet("background: #ff0000")

    def __save_scramble__(self):
        self.error_message = "Введена неверная конфигурация кубика! Проверьте правильность расположения цветов!"
        self.statusbar.setStyleSheet("")
        self.statusbar.showMessage("")
        index = 0
        with open("other/Other/last_scramble_index", "r") as read_file:
            index = int(read_file.readline().strip())
        try:
            with sqlite3.connect("databases/Scrambles_data.sqlite") as database:
                cursor = database.cursor()
                algorithm = list(map(str, utils.solve(self.rubiks_cube, "Kociemba")))
                reversed_algorithm = " ".join(reverse_algorithm(algorithm))
                algorithm = " ".join(algorithm)
                query = f"""INSERT INTO Scrambles(id, configuration, scramble, reversed_scramble) VALUES("{index + 1}", "{self.rubiks_cube}", "{algorithm}", "{reversed_algorithm}")"""
                cursor.execute(query)
                with open("other/Other/last_scramble_index", "w") as write_file:
                    write_file.write(str(index + 1))
        except:
            self.statusbar.setStyleSheet("background: red")
            self.statusbar.showMessage(self.error_message)

    def __open_last_scramble__(self):
        self.error_message = "Нет сохранённых скрамблов!"
        try:
            self.statusbar.setStyleSheet("")
            self.statusbar.showMessage("")
            index = 0
            with open("other/Other/last_scramble_index") as file:
                index = int(file.readline().strip())
            with sqlite3.connect("databases/Scrambles_data.sqlite") as database:
                cursor = database.cursor()
                query = f"""SELECT configuration, scramble, reversed_scramble FROM Scrambles
                WHERE id = {index - self.count_of_clicks}"""
                result = cursor.execute(query)
                algorithms_set = []
                for i in result:
                    algorithms_set = i
                self.__set_scramble__(algorithms_set)
            self.count_of_clicks += 1
            if index == self.count_of_clicks:
                self.count_of_clicks = 0
        except:
            self.statusbar.setStyleSheet("background: red")
            self.statusbar.showMessage(self.error_message)

    def __set_scramble__(self, algorithms_set):
        self.rubiks_cube = algorithms_set[0]
        index = 0
        centre_indexes = [4, 13, 22, 31, 40, 49]
        for button in self.buttonGroup.buttons():
            if index in centre_indexes:
                index += 1
            button.setStyleSheet(
                f"background: {self.button_colors[self.button_colors_names.index(algorithms_set[0][index])]}")
            index += 1