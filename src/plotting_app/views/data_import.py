# -*- coding: utf-8 -*-
import logging

from PySide2.QtWidgets import QDialog
from PySide2.QtCore import Qt, Signal

from plotting_app.views.ui.ui_csv_config_widget import Ui_CSVConfigDialog
from plotting_app.views.ui.ui_date_format_dialog import Ui_DateFormatDialog

logger = logging.getLogger("PlottingApp")


class ReadCSVDialog(QDialog, Ui_CSVConfigDialog):

    def __init__(self):
        super().__init__()
        self.setupUi(self)


class DateFormatDialog(QDialog, Ui_DateFormatDialog):

    selected_date_format = Signal(str)

    def __init__(self, model=None):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Select Date format")
        # self.table_view.setSelectionMode(QAbstractItemView.SingleSelection) -> set in ui file.
        if model:
            self.table_view.setModel(model)
        self.accepted.connect(self._submit_and_close)
        self.add_date_fmt_btn.clicked.connect(lambda: self.table_view.model().add_item(("TBD", "TBD")))
        self.remove_date_fmt_btn.clicked.connect(self._remove_selected_item)

    def _get_selected_item(self):
        indexes = self.table_view.selectedIndexes()
        if len(indexes) == 1:
            return self.table_view.model().data(indexes[0].siblingAtColumn(1), Qt.DisplayRole)
        else:
            # TODO log an error or throw an exception
            pass

    def _remove_selected_item(self):
        pass

    def _submit_and_close(self):
        self.selected_date_format.emit(self._get_selected_item())
