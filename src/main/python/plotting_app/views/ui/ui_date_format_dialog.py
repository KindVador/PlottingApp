# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'date_format_dialog.ui',
# licensing of 'date_format_dialog.ui' applies.
#
# Created: Sun Apr 26 11:16:45 2020
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_DateFormatDialog(object):
    def setupUi(self, DateFormatDialog):
        DateFormatDialog.setObjectName("DateFormatDialog")
        DateFormatDialog.resize(380, 96)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DateFormatDialog.sizePolicy().hasHeightForWidth())
        DateFormatDialog.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(DateFormatDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.date_format_label = QtWidgets.QLabel(DateFormatDialog)
        self.date_format_label.setObjectName("date_format_label")
        self.horizontalLayout.addWidget(self.date_format_label)
        self.date_format_cbx = QtWidgets.QComboBox(DateFormatDialog)
        self.date_format_cbx.setMinimumSize(QtCore.QSize(200, 0))
        self.date_format_cbx.setObjectName("date_format_cbx")
        self.horizontalLayout.addWidget(self.date_format_cbx)
        self.new_date_format_button = QtWidgets.QPushButton(DateFormatDialog)
        self.new_date_format_button.setObjectName("new_date_format_button")
        self.horizontalLayout.addWidget(self.new_date_format_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(DateFormatDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(DateFormatDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), DateFormatDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), DateFormatDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(DateFormatDialog)

    def retranslateUi(self, DateFormatDialog):
        DateFormatDialog.setWindowTitle(QtWidgets.QApplication.translate("DateFormatDialog", "Dialog", None, -1))
        self.date_format_label.setText(QtWidgets.QApplication.translate("DateFormatDialog", "Date format:", None, -1))
        self.new_date_format_button.setText(QtWidgets.QApplication.translate("DateFormatDialog", "New", None, -1))

