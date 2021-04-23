# -*- coding: utf-8 -*-
import logging

from PySide2.QtCore import Qt, Signal
from PySide2.QtWidgets import QMainWindow, QPushButton, QDialog, QAbstractScrollArea, QAction
from PySide2.QtGui import QResizeEvent

from .ui_main_window import Ui_MainWindow
from .ui_log_dialog import Ui_LogDialog

logger = logging.getLogger("PlottingApp")


class MainWindow(QMainWindow, Ui_MainWindow):

    axe_button_clicked = Signal(int, name='axe_button_clicked')
    remove_axe_button = Signal(int, name='remove_axe_button')

    def __init__(self, version):
        super(self.__class__, self).__init__()
        self.version = version
        self.splitter_sizes = None
        self.axe_buttons = []
        self.setup_ui()

    def setup_ui(self):
        self.setupUi(self)
        self.setWindowTitle(f"PlottingApp v{self.version}")
        # set default value for actions
        self.actionClose.setEnabled(False)
        self.actionSave.setEnabled(False)
        self.actionExport.setEnabled(False)
        self.actionShow_in_table.setEnabled(False)
        # update widgets
        self.parameters_tree_widget.setHeaderLabels(['Variable Name'])
        self.parameters_tree_widget.setColumnCount(1)
        # add plot toolbar
        self.get_toolbar_layout().addWidget(self.plot_widget.toolbar)
        # set default options
        self.parameters_tree_widget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)

    def show_hide_variables_panel(self):
        self.parameters_tree_widget.setVisible(not self.parameters_tree_widget.isVisible())
        self.search_field.setVisible(not self.search_field.isVisible())
        if self.parameters_btn.text() == 'hide':
            self.parameters_btn.setText('show')
            # save defaults splitter sizes before modification
            self.splitter_sizes = self.splitter.sizes()
            self.splitter.setSizes([0, sum([int(x) for x in self.splitter_sizes])])
        else:
            self.parameters_btn.setText('hide')
            # save defaults splitter sizes before modification
            self.splitter.setSizes(self.splitter_sizes)

    def get_filter_extension(self):
        # TODO to be modified for contextual menu feature
        return ''

    def clear_all_plots(self):
        for i in range(len(self.axe_buttons)):
            self.remove_axe(0)
        self.plot_widget.clear()

    def update_plots(self, config_dict):
        self.plot_widget.update_all_plots(config_dict)

    def clear(self):
        self.parameters_tree_widget.clear()
        self.clear_all_plots()

    def get_toolbar_layout(self):
        return self.plots_button_layout

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.parameters_tree_widget.clearSelection()

    def add_axe(self, axe_nb):
        _btn = QPushButton(text=str(axe_nb + 1), parent=self.buttons_frame)
        _btn.clicked.connect(lambda x: self.axe_button_clicked.emit(axe_nb + 1))
        _btn.setContextMenuPolicy(Qt.ActionsContextMenu)
        _act_rmv = QAction(f"Remove Axe #{axe_nb+1}", self)
        _act_rmv.triggered.connect(lambda: self.remove_axe_button.emit(axe_nb))
        _btn.addAction(_act_rmv)
        self.buttons_frame.layout().insertWidget(len(self.axe_buttons) + 2, _btn)
        self.axe_buttons.append(_btn)

    def remove_axe(self, axe_nb):
        logger.info(f"Remove axe: {axe_nb}")
        # +2 on index because the layout contains two other buttons 'hide/show' and '>>>'
        lyt_itm = self.buttons_frame.layout().takeAt(axe_nb+2)
        self.axe_buttons.pop(axe_nb)
        lyt_itm.widget().deleteLater()

    def get_selected_parameters_and_clear(self):
        d = {}
        for si in self.parameters_tree_widget.selectedItems():
            if si.parent():
                if si.parent().data(0, Qt.DisplayRole) in d:
                    d[si.parent().data(0, Qt.DisplayRole)] += [si.data(0, Qt.DisplayRole)]
                else:
                    d[si.parent().data(0, Qt.DisplayRole)] = [si.data(0, Qt.DisplayRole)]
            elif si.childCount() > 0:
                d[si.data(0, Qt.DisplayRole)] = [si.child(i).data(0, Qt.DisplayRole) for i in range(si.childCount())]
            else:
                d[si.data(0, Qt.DisplayRole)] = None
        self.parameters_tree_widget.clearSelection()
        return d

    def resizeEvent(self, event: QResizeEvent):
        super(MainWindow, self).resizeEvent(event)
        for i in range(self.parameters_tree_widget.columnCount()):
            self.parameters_tree_widget.resizeColumnToContents(i)


class LogFileWindow(QDialog, Ui_LogDialog):

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.ok_btn.clicked.connect(self.close_action)

    def close_action(self):
        self.log_text_edit.clear()
        self.close()

    def show_log_content(self, filepath):
        self.log_file_value.setText(filepath)
        self.log_text_edit.clear()
        with open(filepath, mode='r') as log_content:
            self.log_text_edit.appendPlainText(''.join(log_content.readlines()))
        self.show()
