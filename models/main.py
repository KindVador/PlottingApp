# -*- coding: utf-8 -*-
import logging
import typing

import PySide2
from PySide2.QtCore import Qt
from PySide2.QtGui import QStandardItem, QStandardItemModel


logger = logging.getLogger("PlottingApp")


class VariableTreeModel(QStandardItemModel):
    def __init__(self, parent=None, variables=None):
        super(self.__class__, self).__init__(parent)
        logger.info("Creation of variable tree model")
        self.root = self.invisibleRootItem()
        if variables:
            for v in variables:
                item = QStandardItem(v)
                self.root.appendRow(item)

    def headerData(self, section:int, orientation:PySide2.QtCore.Qt.Orientation, role:int=...) -> typing.Any:
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return "Variable Name"
        else:
            return None

    # def data(self, index:PySide2.QtCore.QModelIndex, role:int=...) -> typing.Any:
    #     logger.info("VariableTreeModel.data", index.row(), index.column(), role)
    #     print(index)
    #     if role == Qt.DisplayRole:
    #         return self.variables[index.row()]
    #     else:
    #         return None
    #
    # def headerData(self, section:int, orientation:PySide2.QtCore.Qt.Orientation, role:int=...) -> typing.Any:
    #     logger.info("VariableTreeModel.headerData")
    #     if role == Qt.DisplayRole and orientation == Qt.Horizontal:
    #         return "Variable Name"
    #     else:
    #         return None
    #
    # def hasChildren(self, parent:PySide2.QtCore.QModelIndex=...) -> bool:
    #     logger.info("VariableTreeModel.hasChildren")
    #     if parent:
    #         print(parent, parent.row(), parent.column(), parent.isValid(), parent.model())
    #         return False
    #     else:
    #         print("parent is None")
    #         return False
    #
    # def rowCount(self, parent:PySide2.QtCore.QModelIndex=...) -> int:
    #     logger.info("VariableTreeModel.rowCount")
    #     if parent:
    #         print(parent, parent.row(), parent.column(), parent.isValid(), parent.model())
    #         return len(self.variables)
    #     else:
    #         print("parent is None")
    #         return None
    #
    # def columnCount(self, parent:PySide2.QtCore.QModelIndex=...) -> int:
    #     logger.info("VariableTreeModel.columnCount")
    #     if parent:
    #         print(parent, parent.row(), parent.column(), parent.isValid(), parent.model())
    #         return 1
    #     else:
    #         print("parent is None")
    #         return None

