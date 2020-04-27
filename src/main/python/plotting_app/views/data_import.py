# -*- coding: utf-8 -*-
from PySide2.QtWidgets import QDialog

from plotting_app.views.ui.ui_csv_config_widget import Ui_CSVConfigDialog
from plotting_app.views.ui.ui_date_format_dialog import Ui_DateFormatDialog


class ReadCSVDialog(QDialog, Ui_CSVConfigDialog):

    def __init__(self):
        super().__init__()
        self.setupUi(self)


class DateFormatDialog(QDialog, Ui_DateFormatDialog):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
