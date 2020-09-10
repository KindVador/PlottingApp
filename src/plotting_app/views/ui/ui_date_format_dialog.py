# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'date_format_dialog.ui',
# licensing of 'date_format_dialog.ui' applies.
#
# Created: Sat Jun 13 17:36:47 2020
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_DateFormatDialog(object):
    def setupUi(self, DateFormatDialog):
        DateFormatDialog.setObjectName("DateFormatDialog")
        DateFormatDialog.resize(317, 288)
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
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.add_date_fmt_btn = QtWidgets.QPushButton(DateFormatDialog)
        self.add_date_fmt_btn.setObjectName("add_date_fmt_btn")
        self.horizontalLayout.addWidget(self.add_date_fmt_btn)
        self.remove_date_fmt_btn = QtWidgets.QPushButton(DateFormatDialog)
        self.remove_date_fmt_btn.setObjectName("remove_date_fmt_btn")
        self.horizontalLayout.addWidget(self.remove_date_fmt_btn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.table_view = QtWidgets.QTableView(DateFormatDialog)
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table_view.setObjectName("table_view")
        self.verticalLayout.addWidget(self.table_view)
        self.button_box = QtWidgets.QDialogButtonBox(DateFormatDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_box.sizePolicy().hasHeightForWidth())
        self.button_box.setSizePolicy(sizePolicy)
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.button_box.setObjectName("button_box")
        self.verticalLayout.addWidget(self.button_box)

        self.retranslateUi(DateFormatDialog)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL("accepted()"), DateFormatDialog.accept)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL("rejected()"), DateFormatDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(DateFormatDialog)

    def retranslateUi(self, DateFormatDialog):
        DateFormatDialog.setWindowTitle(QtWidgets.QApplication.translate("DateFormatDialog", "Dialog", None, -1))
        self.date_format_label.setText(QtWidgets.QApplication.translate("DateFormatDialog", "Date format:", None, -1))
        self.add_date_fmt_btn.setText(QtWidgets.QApplication.translate("DateFormatDialog", "Add", None, -1))
        self.remove_date_fmt_btn.setText(QtWidgets.QApplication.translate("DateFormatDialog", "Remove", None, -1))

