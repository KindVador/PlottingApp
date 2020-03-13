# -*- coding: utf-8 -*-
from PySide2.QtWidgets import QDialog

from .ui.ui_csv_config_widget import Ui_CSVConfigDialog


class ReadCSVDialog(QDialog, Ui_CSVConfigDialog):

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)

    def get_csv_options(self):
        # TODO add checkbox to activate options
        d = dict()
        # d['sep'] = str(self.sep_edit.text())
        # d['index_col'] = str(self.index_col_edit.text())
        # d['skiprows'] = str(self.skiprows_edit.text())
        # d['na_values'] = str(self.na_values_edit.text())
        # d['prefix'] = str(self.prefix_edit.text())
        # d['decimal'] = str(self.decimal_edit.text())
        return d
