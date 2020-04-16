# -*- coding: utf-8 -*-
import os
import logging

import pandas as pd
from PySide2.QtWidgets import QFileDialog

from plotting_app.models.data_import import ReadCSVModel
from plotting_app.views.data_import import ReadCSVDialog

logger = logging.getLogger("PlottingApp")


class ReadCSVController(object):

    def __init__(self,):
        self.model = ReadCSVModel()
        self.view = ReadCSVDialog()
        self._init_view()

    def _init_view(self):
        logger.info("initialization of the main view")
        self._make_view_connections()

    def _make_view_connections(self):
        logger.info("creation of connections between the main controller and the main view")
        self.view.file_button.clicked.connect(self._select_file)
        self.view.columns_table.setModel(self.model.columns_model)
        self.view.options_table.setModel(self.model.options_model)
        self.view.preview_table.setModel(self.model.preview_model)

    def _select_file(self):
        logger.info("SELECT FILE ACTION")
        opts = QFileDialog.Options()
        user_path = ''
        file_dlg = QFileDialog(parent=self.view)
        file_url = file_dlg.getOpenFileName(self.view, "Select CSV file", user_path, "CSV files (*.csv)", "", opts)
        if file_url and os.path.isfile(file_url[0]):
            self.view.file_line_edit.setText(file_url[0])
            self.model.csv_path = file_url[0]
        else:
            logger.info("User has canceled file selection")

    def get_data_with_dialog(self):
        if self.view.exec_():
            return pd.read_csv(self.model.csv_path, **self.model.options_model.to_dict())
        else:
            return None
