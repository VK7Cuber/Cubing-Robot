
from PySide6.QtWidgets import QMainWindow

from Windows_design_python.Solving_window_design import Ui_Solving_window_design


class ReferenceWindow(QMainWindow, Ui_Solving_window_design):
    def __init__(self, par):
        super().__init__()
        self.parent = par
        self.initUI()

    def initUI(self):
        self.setupUi(self)