# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'new_date_format_dialog.ui',
# licensing of 'new_date_format_dialog.ui' applies.
#
# Created: Wed Apr 29 23:49:22 2020
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_NewDateFormatDialog(object):
    def setupUi(self, NewDateFormatDialog):
        NewDateFormatDialog.setObjectName("NewDateFormatDialog")
        NewDateFormatDialog.resize(388, 87)
        self.formLayout = QtWidgets.QFormLayout(NewDateFormatDialog)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.date_format_label = QtWidgets.QLabel(NewDateFormatDialog)
        self.date_format_label.setObjectName("date_format_label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.date_format_label)
        self.date_format_lineedit = QtWidgets.QLineEdit(NewDateFormatDialog)
        self.date_format_lineedit.setObjectName("date_format_lineedit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.date_format_lineedit)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.cancel_button = QtWidgets.QPushButton(NewDateFormatDialog)
        self.cancel_button.setObjectName("cancel_button")
        self.horizontalLayout.addWidget(self.cancel_button)
        self.add_button = QtWidgets.QPushButton(NewDateFormatDialog)
        self.add_button.setObjectName("add_button")
        self.horizontalLayout.addWidget(self.add_button)
        self.formLayout.setLayout(1, QtWidgets.QFormLayout.SpanningRole, self.horizontalLayout)

        self.retranslateUi(NewDateFormatDialog)
        QtCore.QMetaObject.connectSlotsByName(NewDateFormatDialog)

    def retranslateUi(self, NewDateFormatDialog):
        NewDateFormatDialog.setWindowTitle(QtWidgets.QApplication.translate("NewDateFormatDialog", "Dialog", None, -1))
        self.date_format_label.setText(QtWidgets.QApplication.translate("NewDateFormatDialog", "Date format:", None, -1))
        self.cancel_button.setText(QtWidgets.QApplication.translate("NewDateFormatDialog", "Cancel", None, -1))
        self.add_button.setText(QtWidgets.QApplication.translate("NewDateFormatDialog", "Add", None, -1))

