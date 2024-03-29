# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'csv_config_widget.ui',
# licensing of 'csv_config_widget.ui' applies.
#
# Created: Sun Apr 26 10:39:37 2020
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_CSVConfigDialog(object):
    def setupUi(self, CSVConfigDialog):
        CSVConfigDialog.setObjectName("CSVConfigDialog")
        CSVConfigDialog.resize(728, 600)
        self.verticalLayout = QtWidgets.QVBoxLayout(CSVConfigDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.file_layout = QtWidgets.QHBoxLayout()
        self.file_layout.setObjectName("file_layout")
        self.file_label = QtWidgets.QLabel(CSVConfigDialog)
        self.file_label.setObjectName("file_label")
        self.file_layout.addWidget(self.file_label)
        self.file_line_edit = QtWidgets.QLineEdit(CSVConfigDialog)
        self.file_line_edit.setObjectName("file_line_edit")
        self.file_layout.addWidget(self.file_line_edit)
        self.file_button = QtWidgets.QPushButton(CSVConfigDialog)
        self.file_button.setObjectName("file_button")
        self.file_layout.addWidget(self.file_button)
        self.verticalLayout.addLayout(self.file_layout)
        self.h_line_1 = QtWidgets.QFrame(CSVConfigDialog)
        self.h_line_1.setFrameShape(QtWidgets.QFrame.HLine)
        self.h_line_1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.h_line_1.setObjectName("h_line_1")
        self.verticalLayout.addWidget(self.h_line_1)
        self.infos_preset_layout = QtWidgets.QHBoxLayout()
        self.infos_preset_layout.setObjectName("infos_preset_layout")
        self.infos_button = QtWidgets.QPushButton(CSVConfigDialog)
        self.infos_button.setObjectName("infos_button")
        self.infos_preset_layout.addWidget(self.infos_button)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.infos_preset_layout.addItem(spacerItem)
        self.preset_label = QtWidgets.QLabel(CSVConfigDialog)
        self.preset_label.setObjectName("preset_label")
        self.infos_preset_layout.addWidget(self.preset_label)
        self.preset_cbox = QtWidgets.QComboBox(CSVConfigDialog)
        self.preset_cbox.setObjectName("preset_cbox")
        self.infos_preset_layout.addWidget(self.preset_cbox)
        self.save_cfg_button = QtWidgets.QPushButton(CSVConfigDialog)
        self.save_cfg_button.setObjectName("save_cfg_button")
        self.infos_preset_layout.addWidget(self.save_cfg_button)
        self.verticalLayout.addLayout(self.infos_preset_layout)
        self.options_columns_hlayout = QtWidgets.QHBoxLayout()
        self.options_columns_hlayout.setObjectName("options_columns_hlayout")
        self.options_vlayout = QtWidgets.QVBoxLayout()
        self.options_vlayout.setObjectName("options_vlayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.options_label = QtWidgets.QLabel(CSVConfigDialog)
        self.options_label.setObjectName("options_label")
        self.horizontalLayout.addWidget(self.options_label)
        self.options_vlayout.addLayout(self.horizontalLayout)
        self.options_table = QtWidgets.QTableView(CSVConfigDialog)
        self.options_table.setObjectName("options_table")
        self.options_vlayout.addWidget(self.options_table)
        self.options_columns_hlayout.addLayout(self.options_vlayout)
        self.columns_vlayout = QtWidgets.QVBoxLayout()
        self.columns_vlayout.setObjectName("columns_vlayout")
        self.columns_label = QtWidgets.QLabel(CSVConfigDialog)
        self.columns_label.setObjectName("columns_label")
        self.columns_vlayout.addWidget(self.columns_label)
        self.columns_table = QtWidgets.QTableView(CSVConfigDialog)
        self.columns_table.setObjectName("columns_table")
        self.columns_vlayout.addWidget(self.columns_table)
        self.options_columns_hlayout.addLayout(self.columns_vlayout)
        self.verticalLayout.addLayout(self.options_columns_hlayout)
        self.h_line_2 = QtWidgets.QFrame(CSVConfigDialog)
        self.h_line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.h_line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.h_line_2.setObjectName("h_line_2")
        self.verticalLayout.addWidget(self.h_line_2)
        self.preview_label = QtWidgets.QLabel(CSVConfigDialog)
        self.preview_label.setObjectName("preview_label")
        self.verticalLayout.addWidget(self.preview_label)
        self.preview_table = QtWidgets.QTableView(CSVConfigDialog)
        self.preview_table.setAlternatingRowColors(True)
        self.preview_table.setObjectName("preview_table")
        self.verticalLayout.addWidget(self.preview_table)
        self.buttonBox = QtWidgets.QDialogButtonBox(CSVConfigDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(CSVConfigDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), CSVConfigDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), CSVConfigDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(CSVConfigDialog)

    def retranslateUi(self, CSVConfigDialog):
        CSVConfigDialog.setWindowTitle(QtWidgets.QApplication.translate("CSVConfigDialog", "Import CSV", None, -1))
        self.file_label.setText(QtWidgets.QApplication.translate("CSVConfigDialog", "File:", None, -1))
        self.file_button.setText(QtWidgets.QApplication.translate("CSVConfigDialog", "select", None, -1))
        self.infos_button.setText(QtWidgets.QApplication.translate("CSVConfigDialog", "infos", None, -1))
        self.preset_label.setText(QtWidgets.QApplication.translate("CSVConfigDialog", "Preset:", None, -1))
        self.save_cfg_button.setText(QtWidgets.QApplication.translate("CSVConfigDialog", "Save configuration", None, -1))
        self.options_label.setText(QtWidgets.QApplication.translate("CSVConfigDialog", "Options:", None, -1))
        self.columns_label.setText(QtWidgets.QApplication.translate("CSVConfigDialog", "Columns:", None, -1))
        self.preview_label.setText(QtWidgets.QApplication.translate("CSVConfigDialog", "Preview:", None, -1))

