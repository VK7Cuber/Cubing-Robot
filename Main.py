import sys
import sqlite3
import keyboard

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QButtonGroup
from PyQt6.QtGui import QPixmap, QIcon, QFont
from PyQt6.QtCore import Qt, QTimer

from Main_window_design_ import Ui_Main_Window_design
from Solving_window_design import Ui_solving_window_design
from Pattern_window_design import Ui_Pattern_window_design
from Scramble_window_design import Ui_Scramble_window_design

from rubik_solver import utils
import qdarktheme
from arduino_connection import *
from scramble import *
from make_link import *

# Доделать:
# 1. Сделать одну функцию для открытия каждого окна, принимающую имя окна

class Main_Window(QMainWindow, Ui_Main_Window_design):
    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.connected_picture = QPixmap("images/logo/cubing_robot_connected.png")
        self.disconnected_picture = QPixmap("images/logo/cubing_robot_disconnected.png")
        self.themes = {0: ["light", "светлая", QPixmap("images/logo/cubing_robot_logo_black.png")],
                       1: ["dark", "тёмная", QPixmap("images/logo/cubing_robot_logo_white.png")]}
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
        self.solving_window = Solving_window(self)
        self.solving_window.hide()

        self.scramble_window = Scramble_window(self)
        self.scramble_window.hide()

        self.pattern_window = Pattern_window(self)
        self.pattern_window.hide()

        self.learning_window = Learning_window(self)
        self.learning_window.hide()

        self.reference_window = Reference_window(self)
        self.reference_window.hide()

        self.windows = [self.solving_window, self.scramble_window, self.pattern_window,
                        self.learning_window, self.reference_window]

    def __connect__(self):
        self.solving_button.clicked.connect(self.__open_solving_window__)
        self.scramble_button_2.clicked.connect(self.__open_scramble_window__)
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
            self.scramble_window.is_connected_label.setPixmap(self.connected_picture)
            self.pattern_window.is_connected_label.setPixmap(self.connected_picture)
        else:
            self.solving_window.is_connected_label.setPixmap(self.disconnected_picture)
            self.scramble_window.is_connected_label.setPixmap(self.disconnected_picture)
            self.pattern_window.is_connected_label.setPixmap(self.disconnected_picture)
        #self.timer.start(100)

    def __change_theme__(self):
        self.current_theme = 1 - self.current_theme
        qdarktheme.setup_theme(self.themes[self.current_theme][0])
        self.theme_button.setText(f"Тема: {self.themes[self.current_theme][1]}")
        self.logo_label.setPixmap(self.themes[self.current_theme][2])


class Solving_window(QMainWindow, Ui_solving_window_design):
    def __init__(self, par):
        super().__init__()
        self.parent = par
        self.error_message = ""
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
        self.button_colors_names = {0: 'w', 1: 'g', 2: 'o', 3: 'b', 4: 'r', 5: 'y'}


    def __set_parent_position__(self):
        main_window_position = self.parent.pos()
        self.move(main_window_position.x(), main_window_position.y())


    def __connect__(self):
        self.main_button.clicked.connect(self.__open_main_window__)

        self.solve_button_2.clicked.connect(self.__make_assambling_algorithm__)

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
        self.rubiks_cube = self.rubiks_cube[:configuration_index] + self.button_colors_names[index] + self.rubiks_cube[configuration_index+1:]
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
        try:
            self.statusbar.showMessage("")
            self.statusbar.setStyleSheet("")
            send_massage(list(map(str, algorithm)))
        except:
            self.statusbar.showMessage(self.error_message)
            self.statusbar.setStyleSheet("background: #ff0000")


class Pattern_window(QMainWindow, Ui_Pattern_window_design):
    def __init__(self, par):
        super().__init__()
        self.parent = par
        self.current_algorithm = "R L' F B' U D' R L'".split()
        self.initUI()
    def initUI(self):
        self.setupUi(self)

        self.__setup_window__()
        self.__connect__()

    def __setup_window__(self):
        self.setWindowTitle("Cubing Robot")
        self.setWindowIcon(QIcon("images/logo/cubing_robot_logo_ico.png"))

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

    def __open_main_window__(self):
        self.hide()
        self.parent.show()
        self.parent.__set_other_position__(self.pos())

    def __change_pattern__(self):
        with sqlite3.connect("cube_patterns_data.sqlite") as connection:
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
        if find_arduino() is None:
            self.statusbar.setStyleSheet("background: red")
            self.statusbar.showMessage("Робот не подключён!")
        elif self.current_algorithm[0] == 'В':
            self.statusbar.setStyleSheet("background: red")
            self.statusbar.showMessage("Данный узор находится в разработке!")
        else:
            self.statusbar.setStyleSheet("")
            self.statusbar.showMessage("")
            send_massage(self.current_algorithm)

class Scramble_window(QMainWindow, Ui_Scramble_window_design):
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
        self.initUI()
    def initUI(self):
        self.setupUi(self)
        self.__setup_window__()
        self.__connect__()
    def __setup_window__(self):
        self.setWindowTitle("Cubing Robot")
        self.setWindowIcon(QIcon("images/logo/cubing_robot_logo_ico.png"))
        self.set_motor_speed_spinbox.setValue(99)
        self.timer_label.setFont(QFont('Arial', 48))

    def __connect__(self):
        self.scramble_button.clicked.connect(self.__make_scrambling_algrorithm__)
        self.cut_down_button.clicked.connect(self.__cut_down__)

        self.main_button.clicked.connect(self.__open_main_window__)
        self.reference_button.clicked.connect(self.__open_refer__)

        self.main_timer.timeout.connect(self.__check_keyboard__)
        self.main_timer.start()
        self.pressed_timer.timeout.connect(self.__set_time__)
        self.pressed_timer.start(10)

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
        try:
            send_massage(scramble)
        except:
            self.statusbar.setStyleSheet("background: red")
            self.statusbar.showMessage("Робот не подключён!")


    def __set_parent_position__(self):
        main_window_position = self.parent.pos()
        self.move(main_window_position.x(), main_window_position.y())

    def __check_keyboard__(self):
        if self.is_showing:
            if keyboard.is_pressed("ctrl"):
                if not self.is_solving:
                    self.timer_label.setStyleSheet("background: red")
                else:
                    self.is_solving = False
                    self.solving_time = 0
                self.space_pressed = True
                if self.solving_time > 0.5:
                    self.space_pressed = False
                    self.delay = True
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
                self.timer_label.setText(f"{int(time // 60)} : {round(time  % 60, 2)}")



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