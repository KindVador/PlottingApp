# -*- coding: utf-8 -*-
from PySide2.QtWidgets import QDialog

from plotting_app.views.ui.ui_csv_config_widget import Ui_CSVConfigDialog


class ReadCSVDialog(QDialog, Ui_CSVConfigDialog):

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)