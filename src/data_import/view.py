# -*- coding: utf-8 -*-
import logging

from PySide2.QtWidgets import QWidget, QDialog, QStyledItemDelegate, QComboBox, QStyleOptionViewItem
from PySide2.QtCore import Qt, Signal, Slot, QModelIndex, QAbstractItemModel

from .ui_csv_config_widget import Ui_CSVConfigDialog
from .ui_date_format_dialog import Ui_DateFormatDialog

logger = logging.getLogger("PlottingApp")


class ComboBoxDelegate(QStyledItemDelegate):

    def __init__(self, owner, values):
        super().__init__(owner)
        self.items = values
        self.editor = None

    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex) -> QWidget:
        self.editor = QComboBox(parent)
        self.editor.addItems(self.items)
        # self.editor.activated.connect(self.emit_commit_data)
        return self.editor

    # def paint(self, painter, option, index):
    #     value = index.data(Qt.DisplayRole)
    #     style = QApplication.style()
    #     opt = QStyleOptionComboBox()
    #     opt.text = str(value)
    #     opt.rect = option.rect
    #     style.drawComplexControl(QStyle.CC_ComboBox, opt, painter)
    #     QStyledItemDelegate.paint(self, painter, option, index)

    # def setEditorData(self, editor: QWidget, index: QModelIndex) -> None:
    #     print(f"ComboBoxDelegate.setEditorData({editor}, {index})")
    #     value = index.data(Qt.DisplayRole)
    #     num = self.items.index(value)
    #     editor.setCurrentIndex(num)

    # def setModelData(self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex) -> None:
    #     value = editor.currentText()
    #     print(value, value, value, value)
    #     model.setData(index, value, Qt.DisplayRole)

    # def updateEditorGeometry(self, editor, option, index):
    #     editor.setGeometry(option.rect)

    # def emit_commit_data(self, position: int) -> None:
    #     print(f"ComboBoxDelegate.emit_commit_data({position})")
    #     self.commitData.emit(self.editor)
    #     self.closeEditor.emit(self.editor)


class ReadCSVDialog(QDialog, Ui_CSVConfigDialog):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.options_table.setAlternatingRowColors(True)
        self.columns_table.setAlternatingRowColors(True)
        self.preview_table.setAlternatingRowColors(True)

    def set_types_values(self, values, column_position=1):
        self.columns_table.setItemDelegateForColumn(column_position, ComboBoxDelegate(self, values))

    # def make_combobox_editable_in_single_click(self, column_position=1):
    #     # make combo boxes editable with a single-click:
    #     for row in range(len(self.columns_table.model())):
    #         self.columns_table.openPersistentEditor(self.columns_table.model().index(row, column_position))


class DateFormatDialog(QDialog, Ui_DateFormatDialog):

    selected_date_format = Signal(str)

    def __init__(self, model=None):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Select Date format")
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
