# coding=utf-8

import time

from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QIcon, QPixmap

from Windows_design_python.Manual_turns_window_design import Ui_Manual_turns_window
from Devices.Arduino.arduino_connection import *
from other.Other.scramble import get_random_turn

CONSTANT_ROTATION = False


class ManualTurnsWindow(QMainWindow, Ui_Manual_turns_window):
    def __init__(self, par):
        super().__init__()
        self.parent = par
        self.initUI()

    def initUI(self):
        self.setupUi(self)

        self.__setup_window__()
        self.__connect__()

    def __setup_window__(self):
        self.setWindowTitle("Cubing Robot")
        self.setWindowIcon(QIcon("images/logo/cubing_robot_logo_ico.png"))

        self.set_motor_speed_spinbox.setValue(99)

    def __set_parent_position__(self):
        main_window_position = self.parent.pos()
        self.move(main_window_position.x(), main_window_position.y())

    def __connect__(self):
        self.main_button.clicked.connect(self.__open_main_window__)
        self.reference_button.clicked.connect(self.__open_reference_window__)

        self.buttonGroup.buttonClicked.connect(self.__turn_side__)

        self.constant_rotation_button.clicked.connect(self.__start_constant_rotation__)
        self.stop_constant_rotation_button.clicked.connect(self.__stop_constant_rotation__)

    def __open_main_window__(self):
        self.hide()
        self.parent.show()
        self.parent.__set_other_position__(self.pos())

    def __open_reference_window__(self):
        pass

    def __turn_side__(self, button):
        button_name = button.objectName()
        turn = button_name[0]
        if "back" in button_name:
            turn += "'"
        try:
            self.statusbar.setStyleSheet("")
            self.statusbar.showMessage("")
            send_massage(255 - int(self.set_motor_speed_spinbox.text()), [turn])
        except:
            self.statusbar.setStyleSheet("background: red;")
            self.statusbar.showMessage("Робот не подключен!")

    def __start_constant_rotation__(self):
        pass
        # global CONSTANT_ROTATION
        # CONSTANT_ROTATION = True
        # while CONSTANT_ROTATION:
        #     turn = get_random_turn()
        #     try:
        #         self.statusbar.setStyleSheet("")
        #         self.statusbar.showMessage("")
        #         send_massage(255 - int(self.set_motor_speed_spinbox.text()), [turn])
        #     except:
        #         self.statusbar.setStyleSheet("background: red;")
        #         self.statusbar.showMessage("Робот не подключен!")
        #         break

    def __stop_constant_rotation__(self):
        pass
        # global CONSTANT_ROTATION
        # CONSTANT_ROTATION = False
