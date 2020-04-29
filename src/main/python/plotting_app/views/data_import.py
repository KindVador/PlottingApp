# -*- coding: utf-8 -*-
from PySide2.QtWidgets import QDialog
from PySide2.QtCore import Signal

from plotting_app.views.ui.ui_csv_config_widget import Ui_CSVConfigDialog
from plotting_app.views.ui.ui_date_format_dialog import Ui_DateFormatDialog
from plotting_app.views.ui.ui_new_date_format_dialog import Ui_NewDateFormatDialog


class ReadCSVDialog(QDialog, Ui_CSVConfigDialog):

    def __init__(self):
        super().__init__()
        self.setupUi(self)


class NewDateFormatDialog(QDialog, Ui_NewDateFormatDialog):

    new_date_format = Signal(str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("New Date format")
        self.add_button.clicked.connect(self.submit_and_close)
        self.cancel_button.clicked.connect(self.close)

    def submit_and_close(self):
        self.new_date_format.emit(self.date_format_lineedit.text())
        self.accept()


class DateFormatDialog(QDialog, Ui_DateFormatDialog):

    new_date_format_created = Signal(str)
    selected_date_format = Signal(str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Select Date format")
        self.new_date_fmt_dlg = NewDateFormatDialog()
        self.new_date_fmt_dlg.new_date_format.connect(self._create_new_date_format)
        self.new_date_format_button.clicked.connect(self.new_date_fmt_dlg.exec_)

    def _create_new_date_format(self, date_format):
        self.date_format_cbx.addItem(date_format)
        self.new_date_format_created.emit(date_format)

    def submit_and_close(self):
        self.selected_date_format.emit(self.date_format_cbx.currentText())
        self.accept()
