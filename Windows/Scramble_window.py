# coding=utf-8

import keyboard

from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QIcon, QFont
from PySide6.QtCore import QTimer

from Windows_design_python.Scramble_window_design import Ui_Scramble_window_design

from Devices.Arduino.arduino_connection import *
from other.Other.scramble import *

from rubik_solver import utils


class ScrambleWindow(QMainWindow, Ui_Scramble_window_design):
    def __init__(self, par):
        super().__init__()

        self.parent = par

        self.main_timer = QTimer()
        self.pressed_timer = QTimer()
        self.is_showing = False
        self.solving_time = 0
        self.space_pressed = False
        self.delay = False
        self.is_solving = False

        self.button_colors = ["#ffffff", "#008000", "#ffa500", "#0000ff", "#ff0000", "#ffff00"]
        self.button_colors_names = ['w', 'g', 'o', 'b', 'r', 'y']
        self.rubiks_cube = 'yyyyyyyyybbbbbbbbbrrrrrrrrrgggggggggooooooooowwwwwwwww'

        self.initUI()

    def initUI(self):
        self.setupUi(self)
        self.__setup_window__()
        self.__connect__()

    def __setup_window__(self):
        self.setWindowTitle("Cubing Robot")
        self.setWindowIcon(QIcon("images/logo/cubing_robot_logo_ico.png"))

        self.set_motor_speed_spinbox_1.setValue(99)
        self.set_motor_speed_spinbox_2.setValue(99)
        self.timer_label.setFont(QFont('Arial', 36))

        self.label_2.hide()
        self.scramble_from_cube_state_label.hide()

        self.stackedWidget.setCurrentIndex(0)

    def __connect__(self):
        self.scramble_button.clicked.connect(self.__make_scrambling_algrorithm__)
        self.cut_down_button.clicked.connect(self.__cut_down__)

        self.main_button.clicked.connect(self.__open_main_window__)
        self.reference_button.clicked.connect(self.__open_refer__)

        self.main_timer.timeout.connect(self.__check_keyboard__)
        self.main_timer.start()
        self.pressed_timer.timeout.connect(self.__set_time__)
        self.pressed_timer.start(10)

        self.get_scramble_button.clicked.connect(self.__get_scramble__)
        self.scramble_cube_to_state_btn.clicked.connect(self.__scamble_cube_by_entered_state__)

        self.change_mode_comboBox.currentIndexChanged.connect(self.__change_window_functions__)
        self.buttonGroup.buttonClicked.connect(self.__change_button_color__)

    def __change_window_functions__(self):
        self.stackedWidget.setCurrentIndex(self.change_mode_comboBox.currentIndex())


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


    def __get_scramble__(self):
        try:
            self.statusbar.setStyleSheet("")
            self.statusbar.showMessage("")
            scramble = reverse_algorithm(list(map(str, utils.solve(self.rubiks_cube, "Kociemba"))))
            self.label_2.show()
            self.scramble_from_cube_state_label.show()
            self.scramble_from_cube_state_label.setText(" ".join(scramble))
        except:
            self.statusbar.setStyleSheet("background: red")
            error_message = "Введена неверная конфигурация кубика! Проверьте правильность расположения цветов!"
            self.statusbar.showMessage(error_message)


    def __scamble_cube_by_entered_state__(self):
        try:
            self.statusbar.setStyleSheet("")
            self.statusbar.showMessage("")
            scramble = reverse_algorithm(list(map(str, utils.solve(self.rubiks_cube, "Kociemba"))))
            self.label_2.show()
            self.scramble_from_cube_state_label.show()
            self.scramble_from_cube_state_label.setText(" ".join(scramble))
            self.scramble_cube(scramble)
        except:
            self.statusbar.setStyleSheet("background: red")
            error_message = "Введена неверная конфигурация кубика! Проверьте правильность расположения цветов!"
            self.statusbar.showMessage(error_message)

    def scramble_cube(self, scramble):
        try:
            send_massage(255 - ((int(self.set_motor_speed_spinbox_2.text())) + 1), scramble)
        except:
            self.statusbar.setStyleSheet("background: red")
            self.statusbar.showMessage("Робот не подключён!")


    def __cut_down__(self):
        self.timer_label.setText("0 : 00")
        self.scramble_label.setText(" - ")
        self.statusbar.showMessage("")
        self.statusbar.setStyleSheet("")

    def __open_main_window__(self):
        self.hide()
        self.is_showing = False
        self.parent.show()
        self.parent.__set_other_position__(self.pos())

    def __open_refer__(self):
        pass

    def __make_scrambling_algrorithm__(self):
        self.statusbar.showMessage("")
        self.statusbar.setStyleSheet("")
        scramble = make_scramble()
        self.scramble_label.setText(" ".join(scramble))
        self.scramble_cube(scramble)

    def __set_parent_position__(self):
        main_window_position = self.parent.pos()
        self.move(main_window_position.x(), main_window_position.y())

    def __check_keyboard__(self):
        if self.is_showing:
            if self.change_mode_comboBox.currentIndex() == 0:
                if keyboard.is_pressed("ctrl"):
                    if not self.is_solving:
                        self.timer_label.setFont(QFont('Arial', 36))
                        self.timer_label.setStyleSheet("background: red")
                    else:
                        self.is_solving = False
                        self.solving_time = 0
                    self.space_pressed = True
                    if self.solving_time > 0.5:
                        self.space_pressed = False
                        self.delay = True
                        self.timer_label.setFont(QFont('Arial', 36))
                        self.timer_label.setStyleSheet("background: green")
                else:
                    self.timer_label.setStyleSheet("")
                    self.space_pressed = False
                    if self.delay:
                        self.delay = False
                        self.is_solving = True
                        self.solving_time = 0

    def __set_time__(self):
        if self.is_showing:
            if self.space_pressed:
                self.solving_time += 0.01
            elif self.is_solving:
                self.solving_time += 0.01
                time = self.solving_time
                self.timer_label.setText(f"{int(time // 60)} : {round(time % 60, 2)}")
                self.timer_label.setFont(QFont('Arial', 36))
