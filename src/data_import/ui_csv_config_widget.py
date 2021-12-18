# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'csv_config_widget.ui'
##
## Created by: Qt User Interface Compiler version 5.15.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide6.QtWidgets import *


class Ui_CSVConfigDialog(object):
    def setupUi(self, CSVConfigDialog):
        if not CSVConfigDialog.objectName():
            CSVConfigDialog.setObjectName(u"CSVConfigDialog")
        CSVConfigDialog.resize(728, 600)
        self.verticalLayout = QVBoxLayout(CSVConfigDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.file_layout = QHBoxLayout()
        self.file_layout.setObjectName(u"file_layout")
        self.file_label = QLabel(CSVConfigDialog)
        self.file_label.setObjectName(u"file_label")

        self.file_layout.addWidget(self.file_label)

        self.file_line_edit = QLineEdit(CSVConfigDialog)
        self.file_line_edit.setObjectName(u"file_line_edit")

        self.file_layout.addWidget(self.file_line_edit)

        self.file_button = QPushButton(CSVConfigDialog)
        self.file_button.setObjectName(u"file_button")

        self.file_layout.addWidget(self.file_button)


        self.verticalLayout.addLayout(self.file_layout)

        self.h_line_1 = QFrame(CSVConfigDialog)
        self.h_line_1.setObjectName(u"h_line_1")
        self.h_line_1.setFrameShape(QFrame.HLine)
        self.h_line_1.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.h_line_1)

        self.infos_preset_layout = QHBoxLayout()
        self.infos_preset_layout.setObjectName(u"infos_preset_layout")
        self.preset_label = QLabel(CSVConfigDialog)
        self.preset_label.setObjectName(u"preset_label")

        self.infos_preset_layout.addWidget(self.preset_label)

        self.preset_cbox = QComboBox(CSVConfigDialog)
        self.preset_cbox.setObjectName(u"preset_cbox")

        self.infos_preset_layout.addWidget(self.preset_cbox)

        self.save_cfg_button = QPushButton(CSVConfigDialog)
        self.save_cfg_button.setObjectName(u"save_cfg_button")

        self.infos_preset_layout.addWidget(self.save_cfg_button)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.infos_preset_layout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.infos_preset_layout)

        self.options_columns_hlayout = QHBoxLayout()
        self.options_columns_hlayout.setObjectName(u"options_columns_hlayout")
        self.options_vlayout = QVBoxLayout()
        self.options_vlayout.setObjectName(u"options_vlayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.options_label = QLabel(CSVConfigDialog)
        self.options_label.setObjectName(u"options_label")

        self.horizontalLayout.addWidget(self.options_label)


        self.options_vlayout.addLayout(self.horizontalLayout)

        self.options_table = QTableView(CSVConfigDialog)
        self.options_table.setObjectName(u"options_table")

        self.options_vlayout.addWidget(self.options_table)


        self.options_columns_hlayout.addLayout(self.options_vlayout)

        self.columns_vlayout = QVBoxLayout()
        self.columns_vlayout.setObjectName(u"columns_vlayout")
        self.columns_label = QLabel(CSVConfigDialog)
        self.columns_label.setObjectName(u"columns_label")

        self.columns_vlayout.addWidget(self.columns_label)

        self.columns_table = QTableView(CSVConfigDialog)
        self.columns_table.setObjectName(u"columns_table")

        self.columns_vlayout.addWidget(self.columns_table)


        self.options_columns_hlayout.addLayout(self.columns_vlayout)


        self.verticalLayout.addLayout(self.options_columns_hlayout)

        self.h_line_2 = QFrame(CSVConfigDialog)
        self.h_line_2.setObjectName(u"h_line_2")
        self.h_line_2.setFrameShape(QFrame.HLine)
        self.h_line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.h_line_2)

        self.preview_label = QLabel(CSVConfigDialog)
        self.preview_label.setObjectName(u"preview_label")

        self.verticalLayout.addWidget(self.preview_label)

        self.preview_table = QTableView(CSVConfigDialog)
        self.preview_table.setObjectName(u"preview_table")
        self.preview_table.setAlternatingRowColors(True)

        self.verticalLayout.addWidget(self.preview_table)

        self.buttonBox = QDialogButtonBox(CSVConfigDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(CSVConfigDialog)
        self.buttonBox.accepted.connect(CSVConfigDialog.accept)
        self.buttonBox.rejected.connect(CSVConfigDialog.reject)

        QMetaObject.connectSlotsByName(CSVConfigDialog)
    # setupUi

    def retranslateUi(self, CSVConfigDialog):
        CSVConfigDialog.setWindowTitle(QCoreApplication.translate("CSVConfigDialog", u"Import CSV", None))
        self.file_label.setText(QCoreApplication.translate("CSVConfigDialog", u"File:", None))
        self.file_button.setText(QCoreApplication.translate("CSVConfigDialog", u"select", None))
        self.preset_label.setText(QCoreApplication.translate("CSVConfigDialog", u"Preset:", None))
        self.save_cfg_button.setText(QCoreApplication.translate("CSVConfigDialog", u"Save configuration", None))
        self.options_label.setText(QCoreApplication.translate("CSVConfigDialog", u"Options:", None))
        self.columns_label.setText(QCoreApplication.translate("CSVConfigDialog", u"Columns:", None))
        self.preview_label.setText(QCoreApplication.translate("CSVConfigDialog", u"Preview:", None))
    # retranslateUi

