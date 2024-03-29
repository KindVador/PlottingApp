# -*- coding: utf-8 -*-
from PySide2.QtCore import Qt, Signal
from PySide2.QtWidgets import QMainWindow, QPushButton

from plotting_app.views.ui.ui_main_window import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):

    axe_button_clicked = Signal(int, name='axe_button_clicked')

    def __init__(self, version):
        super(self.__class__, self).__init__()
        self.version = version
        self.axe_buttons = []
        self.setup_ui()

    def setup_ui(self):
        self.setupUi(self)
        self.setWindowTitle(f"PlottingApp v{self.version}")
        # update widgets
        self.parameters_tree_widget.setHeaderLabels(['Variable Name'])
        self.parameters_tree_widget.setColumnCount(1)
        self.marker_cbx.addItems([f"'{m}'" for m in ['.', ',', 'o', 'x', 'X', '+', 'v', '^', '<', '>', 'p', 'P', '*',
                                                     'h', 'H', 'D', 'd', 'None']])
        self.line_style_cbx.addItems([f"'{ls}'" for ls in ['-', '--', '-.', ':', 'None']])
        self.draw_style_cbx.addItems(['default', 'steps', 'steps-pre', 'steps-mid', 'steps-post'])
        # add plot toolbar
        self.get_toolbar_layout().addWidget(self.plot_widget.toolbar)
        # set default options
        self.marker_cbx.setCurrentText("'.'")
        self.line_style_cbx.setCurrentText("'-'")
        self.draw_style_cbx.setCurrentText('steps-post')
        # make connections
        self.btn_raw_value.clicked.connect(self._btn_raw_value_clicked)
        self.btn_label.clicked.connect(self._btn_label_clicked)
        self.btn_sdi.clicked.connect(self._btn_sdi_clicked)
        self.btn_ssm.clicked.connect(self._btn_ssm_clicked)
        self.btn_parity.clicked.connect(self._btn_parity_clicked)
        self.btn_bit.clicked.connect(self._btn_bit_clicked)
        self.bit_spinbox.valueChanged.connect(self._btn_bit_clicked)

    def show_hide_variables_panel(self):
        self.btn_raw_value.setVisible(not self.btn_raw_value.isVisible())
        self.btn_label.setVisible(not self.btn_label.isVisible())
        self.btn_sdi.setVisible(not self.btn_sdi.isVisible())
        self.btn_ssm.setVisible(not self.btn_ssm.isVisible())
        self.btn_parity.setVisible(not self.btn_parity.isVisible())
        self.btn_bit.setVisible(not self.btn_bit.isVisible())
        self.bit_spinbox.setVisible(not self.bit_spinbox.isVisible())
        self.parameters_tree_widget.setVisible(not self.parameters_tree_widget.isVisible())

    def enable_arinc_buttons(self, state):
        self.btn_raw_value.setChecked(True)
        self.btn_raw_value.setEnabled(state)
        self.btn_label.setChecked(False)
        self.btn_label.setEnabled(state)
        self.btn_sdi.setChecked(False)
        self.btn_sdi.setEnabled(state)
        self.btn_ssm.setChecked(False)
        self.btn_ssm.setEnabled(state)
        self.btn_parity.setChecked(False)
        self.btn_parity.setEnabled(state)
        self.btn_bit.setEnabled(state)
        self.btn_bit.setChecked(False)
        self.bit_spinbox.setEnabled(state)

    def _btn_bit_clicked(self):
        self.btn_raw_value.setChecked(False)
        self.btn_label.setChecked(False)
        self.btn_parity.setChecked(False)
        self.btn_ssm.setChecked(False)
        self.btn_sdi.setChecked(False)
        self.btn_bit.setChecked(True)

    def _btn_raw_value_clicked(self):
        self.btn_label.setChecked(False)
        self.btn_parity.setChecked(False)
        self.btn_ssm.setChecked(False)
        self.btn_sdi.setChecked(False)
        self.btn_bit.setChecked(False)

    def _btn_label_clicked(self):
        self.btn_raw_value.setChecked(False)
        self.btn_parity.setChecked(False)
        self.btn_ssm.setChecked(False)
        self.btn_sdi.setChecked(False)
        self.btn_bit.setChecked(False)

    def _btn_parity_clicked(self):
        self.btn_raw_value.setChecked(False)
        self.btn_label.setChecked(False)
        self.btn_ssm.setChecked(False)
        self.btn_sdi.setChecked(False)
        self.btn_bit.setChecked(False)

    def _btn_ssm_clicked(self):
        self.btn_raw_value.setChecked(False)
        self.btn_parity.setChecked(False)
        self.btn_label.setChecked(False)
        self.btn_sdi.setChecked(False)
        self.btn_bit.setChecked(False)

    def _btn_sdi_clicked(self):
        self.btn_raw_value.setChecked(False)
        self.btn_parity.setChecked(False)
        self.btn_label.setChecked(False)
        self.btn_ssm.setChecked(False)
        self.btn_bit.setChecked(False)

    def get_filter_extension(self):
        if self.btn_raw_value.isEnabled():
            if self.btn_raw_value.isChecked():
                return ''
            elif self.btn_ssm.isChecked():
                return ';SSM'
            elif self.btn_sdi.isChecked():
                return ';SDI'
            elif self.btn_parity.isChecked():
                return ';P'
            elif self.btn_label.isChecked():
                return ';LBL'
            elif self.btn_bit.isChecked():
                return f';BIT{self.bit_spinbox.value():02d}'
            else:
                return ''
        else:
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
        # _btn.setContextMenuPolicy(Qt.ActionsContextMenu)
        # _act = QAction("Remove", self)
        # _act.triggered.connect(lambda x: self.remove_axe_button.emit(axe_nb))
        # _btn.addAction(_act)
        self.buttons_frame.layout().insertWidget(len(self.axe_buttons) + 2, _btn)
        self.axe_buttons.append(_btn)
        self.remove_cbx.addItem(str(len(self.axe_buttons)))

    def remove_axe(self, axe_nb):
        self.remove_cbx.removeItem(axe_nb)
        # self.axe_buttons[axe_nb].removeAction(self.axe_buttons[axe_nb].actions()[0])
        self.axe_buttons.pop(axe_nb).setParent(None)        # remove button from layout

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

    def get_marker(self):
        return self.marker_cbx.currentText().replace("'", "")

    def get_line_style(self):
        return self.line_style_cbx.currentText().replace("'", "")

    def get_drawstyle(self):
        return self.draw_style_cbx.currentText()
