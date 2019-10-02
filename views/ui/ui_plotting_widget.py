# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plotting_widget.ui',
# licensing of 'plotting_widget.ui' applies.
#
# Created: Sun Mar 31 10:01:21 2019
#      by: pyside2-uic  running on PySide2 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_PlottingWidget(object):
    def setupUi(self, PlottingWidget):
        PlottingWidget.setObjectName("PlottingWidget")
        PlottingWidget.resize(950, 566)
        self.horizontalLayout = QtWidgets.QHBoxLayout(PlottingWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.v_layout = QtWidgets.QVBoxLayout()
        self.v_layout.setObjectName("v_layout")
        self.h_layout = QtWidgets.QHBoxLayout()
        self.h_layout.setObjectName("h_layout")
        self.variables_lbl = QtWidgets.QLabel(PlottingWidget)
        self.variables_lbl.setObjectName("variables_lbl")
        self.h_layout.addWidget(self.variables_lbl)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.h_layout.addItem(spacerItem)
        self.add_btn = QtWidgets.QPushButton(PlottingWidget)
        self.add_btn.setObjectName("add_btn")
        self.h_layout.addWidget(self.add_btn)
        self.v_layout.addLayout(self.h_layout)
        self.variables_tree = QtWidgets.QTreeView(PlottingWidget)
        self.variables_tree.setObjectName("variables_tree")
        self.v_layout.addWidget(self.variables_tree)
        self.horizontalLayout.addLayout(self.v_layout)
        self.plot_frame = QtWidgets.QFrame(PlottingWidget)
        self.plot_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.plot_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.plot_frame.setObjectName("plot_frame")
        self.horizontalLayout.addWidget(self.plot_frame)

        self.retranslateUi(PlottingWidget)
        QtCore.QMetaObject.connectSlotsByName(PlottingWidget)

    def retranslateUi(self, PlottingWidget):
        PlottingWidget.setWindowTitle(QtWidgets.QApplication.translate("PlottingWidget", "Form", None, -1))
        self.variables_lbl.setText(QtWidgets.QApplication.translate("PlottingWidget", "Variables:", None, -1))
        self.add_btn.setText(QtWidgets.QApplication.translate("PlottingWidget", "Add to Plot", None, -1))

