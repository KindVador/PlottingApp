# -*- coding: utf-8 -*-
from PySide2.QtWidgets import QMainWindow

from .ui.ui_main_window import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, version):
        super(self.__class__, self).__init__()
        self.version = version
        self.setupUi(self)
