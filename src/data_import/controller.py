# -*- coding: utf-8 -*-
import os
import logging

from PySide2.QtWidgets import QFileDialog, QInputDialog, QLineEdit
from PySide2.QtCore import Slot, QDir, Signal, QObject

from .model import ReadCSVModel
from .view import ReadCSVDialog, DateFormatDialog

logger = logging.getLogger("PlottingApp")


class ReadCSVController(QObject):

    config_updated = Signal()
    # preview_refreshed = Signal()

    def __init__(self, preset_model):
        super(self.__class__, self).__init__()
        self.preset_model = preset_model
        self.model = ReadCSVModel(parent=self, preset_model=preset_model)
        self.view = ReadCSVDialog()
        self._init_view()

    def _init_view(self):
        logger.info("initialization of the main view")
        self._make_view_connections()
        # init ComboBox values for type columns
        self.view.configure(self.model.columns_model.allowed_types, 1)
        # connect widgets to models
        self.view.preset_cbox.setModel(self.model.preset_model)

    def _make_view_connections(self):
        logger.info("creation of connections between the main controller and the main view")
        self.view.file_button.clicked.connect(self._select_file)
        self.view.save_cfg_button.clicked.connect(self._save_cfg)
        self.view.columns_table.setModel(self.model.columns_model)
        self.view.options_table.setModel(self.model.options_model)
        self.view.preview_table.setModel(self.model.preview_model)
        self.model.date_format_required.connect(self._ask_date_format)
        self.view.preset_cbox.currentTextChanged.connect(self.load_preset)

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

    def load_preset(self, text):
        logger.info(f"Loading preset: {text}")
        self.model.options_model.clear()
        # populate OptionTableModel with preset values
        for k, v in self.preset_model[text].items():
            self.model.options_model.set_option(k, v)

    def _save_cfg(self):
        logger.info("SAVE CURRENT CONFIGURATION")
        # ask user the name of the configuration
        cfg_name, res = QInputDialog.getText(self.view, "Please fill the name", "Configuration's name", QLineEdit.Normal, QDir.home().dirName())
        if res and len(cfg_name) > 0:
            # save current configuration to the user configuration object
            cfg_dict = {'name': cfg_name, 'options': self.model.options_model.to_dict()}
            self.model.preset_model.beginResetModel()
            self.preset_model.add(cfg_dict['name'], cfg_dict['options'])
            self.model.preset_model.endResetModel()
            # select this new preset in the combobox widget in the view
            self.view.preset_cbox.setCurrentText(cfg_name)
            self.config_updated.emit()

    def get_data_with_dialog(self):
        if self.view.exec_():
            return self.model.get_dataframe(), self.model.csv_path
        else:
            return None, None

    def set_date_format(self, date_format):
        logger.debug(f"ReadCSVController.set_date_format({date_format})")
        self.model._date_format = date_format

    @Slot(name="ask_date_format")
    def _ask_date_format(self):
        logger.info("Ask user to select a date format")
        dlg = DateFormatDialog(self.model.date_format_model)
        dlg.selected_date_format.connect(self.set_date_format)
        dlg.exec_()
