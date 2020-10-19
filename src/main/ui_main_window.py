# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 5.15.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *

from .widgets import MatplotlibWidget


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1066, 600)
        self.actionQuit = QAction(MainWindow)
        self.actionQuit.setObjectName(u"actionQuit")
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionClose = QAction(MainWindow)
        self.actionClose.setObjectName(u"actionClose")
        self.actionExport = QAction(MainWindow)
        self.actionExport.setObjectName(u"actionExport")
        self.actionCSV = QAction(MainWindow)
        self.actionCSV.setObjectName(u"actionCSV")
        self.actionShow_in_table = QAction(MainWindow)
        self.actionShow_in_table.setObjectName(u"actionShow_in_table")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.variables_layout = QVBoxLayout()
        self.variables_layout.setSpacing(5)
        self.variables_layout.setObjectName(u"variables_layout")
        self.variables_layout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.search_field = QLineEdit(self.centralwidget)
        self.search_field.setObjectName(u"search_field")

        self.variables_layout.addWidget(self.search_field)

        self.parameters_tree_widget = QTreeWidget(self.centralwidget)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.parameters_tree_widget.setHeaderItem(__qtreewidgetitem)
        self.parameters_tree_widget.setObjectName(u"parameters_tree_widget")
        self.parameters_tree_widget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.parameters_tree_widget.setSelectionMode(QAbstractItemView.MultiSelection)
        self.parameters_tree_widget.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.parameters_tree_widget.setSortingEnabled(True)
        self.parameters_tree_widget.setAllColumnsShowFocus(True)
        self.parameters_tree_widget.setExpandsOnDoubleClick(False)
        self.parameters_tree_widget.setColumnCount(1)

        self.variables_layout.addWidget(self.parameters_tree_widget)


        self.horizontalLayout.addLayout(self.variables_layout)

        self.buttons_frame = QFrame(self.centralwidget)
        self.buttons_frame.setObjectName(u"buttons_frame")
        self.buttons_frame.setMaximumSize(QSize(45, 16777215))
        self.buttons_frame.setFrameShape(QFrame.Panel)
        self.buttons_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.buttons_frame)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 5, 0, 5)
        self.parameters_btn = QPushButton(self.buttons_frame)
        self.parameters_btn.setObjectName(u"parameters_btn")

        self.verticalLayout.addWidget(self.parameters_btn)

        self.verticalSpacer = QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.add_btn = QPushButton(self.buttons_frame)
        self.add_btn.setObjectName(u"add_btn")

        self.verticalLayout.addWidget(self.add_btn)

        self.verticalSpacer_2 = QSpacerItem(20, 184, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)


        self.horizontalLayout.addWidget(self.buttons_frame)

        self.plots_layout = QVBoxLayout()
        self.plots_layout.setObjectName(u"plots_layout")
        self.plots_button_layout = QHBoxLayout()
        self.plots_button_layout.setObjectName(u"plots_button_layout")
        self.btn_clear_plots = QPushButton(self.centralwidget)
        self.btn_clear_plots.setObjectName(u"btn_clear_plots")
        font = QFont()
        font.setPointSize(12)
        self.btn_clear_plots.setFont(font)

        self.plots_button_layout.addWidget(self.btn_clear_plots)

        self.remove_lbl = QLabel(self.centralwidget)
        self.remove_lbl.setObjectName(u"remove_lbl")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.remove_lbl.sizePolicy().hasHeightForWidth())
        self.remove_lbl.setSizePolicy(sizePolicy)
        self.remove_lbl.setMaximumSize(QSize(45, 16777215))

        self.plots_button_layout.addWidget(self.remove_lbl)

        self.remove_cbx = QComboBox(self.centralwidget)
        self.remove_cbx.setObjectName(u"remove_cbx")
        self.remove_cbx.setFont(font)
        self.remove_cbx.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        self.plots_button_layout.addWidget(self.remove_cbx)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(40, 16777215))

        self.plots_button_layout.addWidget(self.label)

        self.marker_cbx = QComboBox(self.centralwidget)
        self.marker_cbx.setObjectName(u"marker_cbx")
        font1 = QFont()
        font1.setPointSize(12)
        font1.setBold(False)
        font1.setWeight(50)
        self.marker_cbx.setFont(font1)
        self.marker_cbx.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        self.plots_button_layout.addWidget(self.marker_cbx)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMaximumSize(QSize(48, 16777215))

        self.plots_button_layout.addWidget(self.label_2)

        self.line_style_cbx = QComboBox(self.centralwidget)
        self.line_style_cbx.setObjectName(u"line_style_cbx")
        self.line_style_cbx.setFont(font1)
        self.line_style_cbx.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        self.plots_button_layout.addWidget(self.line_style_cbx)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.plots_button_layout.addWidget(self.label_3)

        self.draw_style_cbx = QComboBox(self.centralwidget)
        self.draw_style_cbx.setObjectName(u"draw_style_cbx")
        self.draw_style_cbx.setFont(font)

        self.plots_button_layout.addWidget(self.draw_style_cbx)

        self.horizontalSpacer = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.plots_button_layout.addItem(self.horizontalSpacer)


        self.plots_layout.addLayout(self.plots_button_layout)

        self.plot_widget = MatplotlibWidget(self.centralwidget)
        self.plot_widget.setObjectName(u"plot_widget")

        self.plots_layout.addWidget(self.plot_widget)

        self.plots_layout.setStretch(1, 1)

        self.horizontalLayout.addLayout(self.plots_layout)

        self.horizontalLayout.setStretch(2, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1066, 24))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuData = QMenu(self.menubar)
        self.menuData.setObjectName(u"menuData")
        self.menuImport = QMenu(self.menuData)
        self.menuImport.setObjectName(u"menuImport")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuData.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionClose)
        self.menuFile.addAction(self.actionQuit)
        self.menuHelp.addAction(self.actionAbout)
        self.menuData.addAction(self.menuImport.menuAction())
        self.menuData.addAction(self.actionExport)
        self.menuData.addAction(self.actionShow_in_table)
        self.menuImport.addAction(self.actionCSV)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.actionClose.setText(QCoreApplication.translate("MainWindow", u"Close", None))
        self.actionExport.setText(QCoreApplication.translate("MainWindow", u"Export", None))
        self.actionCSV.setText(QCoreApplication.translate("MainWindow", u"CSV", None))
        self.actionShow_in_table.setText(QCoreApplication.translate("MainWindow", u"Show in table", None))
        self.parameters_btn.setText(QCoreApplication.translate("MainWindow", u"hide", None))
        self.add_btn.setText(QCoreApplication.translate("MainWindow", u">>>", None))
        self.btn_clear_plots.setText(QCoreApplication.translate("MainWindow", u"Clear all", None))
        self.remove_lbl.setText(QCoreApplication.translate("MainWindow", u"Remove:", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Marker:", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Line Style:", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Draw style:", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuData.setTitle(QCoreApplication.translate("MainWindow", u"Data", None))
        self.menuImport.setTitle(QCoreApplication.translate("MainWindow", u"Import", None))
    # retranslateUi

