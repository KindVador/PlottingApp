# -*- coding: utf-8 -*-
import logging

from PySide2.QtWidgets import (QWidget, QDialog, QStyledItemDelegate, QComboBox, QStyleOptionViewItem, QStyle,
                               QStyleOptionButton, QApplication)
from PySide2.QtCore import Qt, Signal, QModelIndex, QEvent, QRect, QPoint

from .ui_csv_config_widget import Ui_CSVConfigDialog
from .ui_date_format_dialog import Ui_DateFormatDialog

logger = logging.getLogger("PlottingApp")


class CheckBoxDelegate(QStyledItemDelegate):
    """
    A delegate that places a fully functioning QCheckBox in every cell of the column to which it's applied
    """

    def __init__(self, parent):
        QStyledItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index):
        """
        Important, otherwise an editor is created if the user clicks in this cell.
        ** Need to hook up a signal to the model

        Args:
            parent:
            option:
            index:

        Returns:

        """
        return None

    def paint(self, painter, option, index):
        """
        Paint a checkbox without the label.

        Args:
            painter:
            option:
            index:

        Returns:

        """

        checked = bool(index.data())
        check_box_style_option = QStyleOptionButton()

        if (index.flags() & Qt.ItemIsEditable) > 0:
            check_box_style_option.state |= QStyle.State_Enabled
        else:
            check_box_style_option.state |= QStyle.State_ReadOnly

        check_box_style_option.state |= (QStyle.State_On if checked else QStyle.State_Off)

        check_box_style_option.rect = self.getCheckBoxRect(option)

        check_box_style_option.state |= QStyle.State_Enabled

        QApplication.style().drawControl(QStyle.CE_CheckBox, check_box_style_option, painter)

    def editorEvent(self, event, model, option, index):
        """
        Change the data in the model and the state of the checkbox if the user presses the left mousebutton or presses
        Key_Space or Key_Select and this cell is editable. Otherwise do nothing.

        Args:
            event:
            model:
            option:
            index:

        Returns:

        """
        if not (index.flags() & Qt.ItemIsEditable) > 0:
            return False

        # Do not change the checkbox-state
        if event.type() == QEvent.MouseButtonPress:
          return False
        if event.type() in [QEvent.MouseButtonRelease, QEvent.MouseButtonDblClick]:
            if event.button() != Qt.LeftButton or not self.getCheckBoxRect(option).contains(event.pos()):
                return False
            if event.type() == QEvent.MouseButtonDblClick:
                return True
        elif event.type() == QEvent.KeyPress:
            if event.key() not in [Qt.Key_Space, Qt.Key_Select]:
                return False
        else:
            return False

        # Change the checkbox-state
        self.setModelData(None, model, index)
        return True

    def setModelData(self, editor, model, index):
        """
        The user wanted to change the old state in the opposite.

        Args:
            editor:
            model:
            index:

        Returns:

        """
        newValue = not bool(index.data())
        model.setData(index, newValue, Qt.EditRole)

    def getCheckBoxRect(self, option):
        """

        Args:
            option:

        Returns:

        """
        check_box_style_option = QStyleOptionButton()
        check_box_rect = QApplication.style().subElementRect(QStyle.SE_CheckBoxIndicator, check_box_style_option, None)
        check_box_point = QPoint(option.rect.x() +
                                 option.rect.width() / 2 -
                                 check_box_rect.width() / 2,
                                 option.rect.y() +
                                 option.rect.height() / 2 -
                                 check_box_rect.height() / 2)
        return QRect(check_box_point, check_box_rect.size())


class ComboBoxDelegate(QStyledItemDelegate):

    def __init__(self, owner, values):
        super().__init__(owner)
        self.items = values
        self.editor = None

    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex) -> QWidget:
        self.editor = QComboBox(parent)
        self.editor.addItems(self.items)
        return self.editor


class ReadCSVDialog(QDialog, Ui_CSVConfigDialog):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.options_table.setAlternatingRowColors(True)
        self.columns_table.setAlternatingRowColors(True)
        self.preview_table.setAlternatingRowColors(True)

    def configure(self, type_values, type_pos=1, index_pos=2):
        self.columns_table.setItemDelegateForColumn(type_pos, ComboBoxDelegate(self, type_values))
        self.columns_table.setItemDelegateForColumn(index_pos, CheckBoxDelegate(self))


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
