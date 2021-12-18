# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'log_dialog.ui'
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


class Ui_LogDialog(object):
    def setupUi(self, LogDialog):
        if not LogDialog.objectName():
            LogDialog.setObjectName(u"LogDialog")
        LogDialog.resize(714, 392)
        self.verticalLayout = QVBoxLayout(LogDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.log_file_lbl = QLabel(LogDialog)
        self.log_file_lbl.setObjectName(u"log_file_lbl")

        self.horizontalLayout.addWidget(self.log_file_lbl)

        self.log_file_value = QLabel(LogDialog)
        self.log_file_value.setObjectName(u"log_file_value")

        self.horizontalLayout.addWidget(self.log_file_value)

        self.horizontalLayout.setStretch(1, 1)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.log_text_edit = QPlainTextEdit(LogDialog)
        self.log_text_edit.setObjectName(u"log_text_edit")

        self.verticalLayout.addWidget(self.log_text_edit)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.ok_btn = QPushButton(LogDialog)
        self.ok_btn.setObjectName(u"ok_btn")

        self.horizontalLayout_2.addWidget(self.ok_btn)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(LogDialog)

        QMetaObject.connectSlotsByName(LogDialog)
    # setupUi

    def retranslateUi(self, LogDialog):
        LogDialog.setWindowTitle(QCoreApplication.translate("LogDialog", u"Dialog", None))
        self.log_file_lbl.setText(QCoreApplication.translate("LogDialog", u"Log file:", None))
        self.log_file_value.setText("")
        self.ok_btn.setText(QCoreApplication.translate("LogDialog", u"OK", None))
    # retranslateUi

