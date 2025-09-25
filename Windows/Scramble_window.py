# coding=utf-8

import keyboard

from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QIcon, QFont
from PySide6.QtCore import QTimer

from Windows_design_python.Scramble_window_design import Ui_Scramble_window_design

from Devices.Arduino.arduino_connection import *
from other.Other.scramble import *
from other.Other.validate_scramble import validate_scramble

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
        self.setWindowIcon(QIcon("images/logo/cubing_robot_logo_icon.png"))

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

        # Competitive scramble tab actions
        if hasattr(self, 'validate_scrambles_button'):
            self.validate_scrambles_button.clicked.connect(self.__validate_competitive_scrambles__)
        if hasattr(self, 'start_competitive_scramble_button'):
            self.start_competitive_scramble_button.clicked.connect(self.__start_competitive_scramble__)
        if hasattr(self, 'generate_scrambles_button'):
            self.generate_scrambles_button.clicked.connect(self.__generate_competitive_scrambles__)
        if hasattr(self, 'clear_all_scrambles_button'):
            self.clear_all_scrambles_button.clicked.connect(self.__clear_all_competitive_scrambles__)

    def __change_window_functions__(self):
        self.stackedWidget.setCurrentIndex(self.change_mode_comboBox.currentIndex())

        # ensure default speed values for new tab
        if hasattr(self, 'competitive_speed_spinbox'):
            self.competitive_speed_spinbox.setValue(99)

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
        if arduino.check_connection():
            arduino.set_motors_speed(255 - ((int(self.set_motor_speed_spinbox_2.text())) + 1))
            arduino.send_message(scramble)
        else:
            self.statusbar.setStyleSheet("background: red")
            self.statusbar.showMessage("Робот не подключён!")

    def __scramble_cube_with_speed__(self, scramble, ui_speed_spinbox):
        if arduino.check_connection():
            arduino.set_motors_speed(255 - ((int(ui_speed_spinbox.text())) + 1))
            arduino.send_message(scramble)
        else:
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

    def __get_competitive_scrambles_widgets__(self):
        inputs = []
        radios = []
        for idx in range(1, 6):
            input_widget = getattr(self, f"scramble_input_{idx}", None)
            radio_widget = getattr(self, f"radio_{idx}", None)
            if input_widget is not None and radio_widget is not None:
                inputs.append(input_widget)
                radios.append(radio_widget)
        return inputs, radios

    def __validate_competitive_scrambles__(self):
        inputs, _ = self.__get_competitive_scrambles_widgets__()
        any_filled = False
        has_error = False
        self.statusbar.setStyleSheet("")
        self.statusbar.showMessage("")

        for idx, le in enumerate(inputs, start=1):
            text = le.text()
            # reset style before re-validate
            le.setStyleSheet("")
            if text.strip():
                any_filled = True
                valid, error, tokens = validate_scramble(text)
                if not valid:
                    has_error = True
                    le.setStyleSheet("background: rgba(255,0,0,0.3)")
                    self.statusbar.setStyleSheet("background: red")
                    self.statusbar.showMessage(f"Ошибка в скрамбле {idx}: {error}")
                    break

        if not any_filled and not has_error:
            self.statusbar.setStyleSheet("background: red")
            self.statusbar.showMessage("Введите хотя бы один скрамбл для проверки.")
            return
        if not has_error:
            self.statusbar.setStyleSheet("background: #008000")
            self.statusbar.showMessage("Скрамблы корректны.")

    def __start_competitive_scramble__(self):
        inputs, radios = self.__get_competitive_scrambles_widgets__()
        selected_index = None
        for i, rb in enumerate(radios):
            if rb.isChecked():
                selected_index = i
                break
        if selected_index is None:
            self.statusbar.setStyleSheet("background: red")
            self.statusbar.showMessage("Выберите скрамбл для выполнения.")
            return

        le = inputs[selected_index]
        text = le.text()
        valid, error, tokens = validate_scramble(text)
        # clear previous highlight
        le.setStyleSheet("")
        if not valid:
            le.setStyleSheet("background: rgba(255,0,0,0.3)")
            self.statusbar.setStyleSheet("background: red")
            self.statusbar.showMessage(f"Ошибка: {error}")
            return

        # run scramble
        if hasattr(self, 'competitive_speed_spinbox'):
            self.__scramble_cube_with_speed__(tokens, self.competitive_speed_spinbox)
        else:
            # fallback to second tab speed control if not present
            self.scramble_cube(tokens)

    def __generate_competitive_scrambles__(self):
        inputs, _ = self.__get_competitive_scrambles_widgets__()
        self.statusbar.setStyleSheet("")
        self.statusbar.showMessage("")
        for le in inputs:
            le.setStyleSheet("")
            le.setText(" ".join(make_scramble()))

    def __clear_all_competitive_scrambles__(self):
        inputs, _ = self.__get_competitive_scrambles_widgets__()
        self.statusbar.setStyleSheet("")
        self.statusbar.showMessage("")
        for le in inputs:
            le.setStyleSheet("")
            le.setText("")

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
