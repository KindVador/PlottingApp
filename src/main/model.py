# -*- coding: utf-8 -*-
import logging
import typing

import PySide2
from PySide2.QtCore import Qt, QAbstractItemModel, QModelIndex


logger = logging.getLogger("PlottingApp")


class VariableTreeItem(object):
    """

    """

    def __init__(self, data, parent=None):
        self.child_items = []
        self.item_data = data
        self.parent = parent

    def appendChild(self, child):
        self.child_items.append(child)

    def child(self, row: int):
        if row < 0 or row >= len(self.child_items):
            return None
        return self.child_items[row]

    def childCount(self) -> int:
        return len(self.child_items)

    def columnCount(self) -> int:
        return len(self.item_data)

    def data(self, column: int):
        if column < 0 or column >= len(self.item_data):
            return None
        return self.item_data[column]

    def row(self) -> int:
        if self.parent:
            return self.parent.child_items.index(self)
        return 0

    def parentItem(self):
        return self.parent


class VariableTreeModel(QAbstractItemModel):
    """

    """
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        logger.info("Creation of variable tree plot_model")
        self.rootItem = VariableTreeItem(["Variables"])
        self._items = []

    def headerData(self, section:int, orientation:PySide2.QtCore.Qt.Orientation, role:int=...) -> typing.Any:
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.rootItem.data(section)
        else:
            return None

    def data(self, index:PySide2.QtCore.QModelIndex, role:int=...) -> typing.Any:
        if (not index.isValid()) or role != Qt.DisplayRole:
            return None
        return index.internalPointer().data(index.column())

    def flags(self, index: PySide2.QtCore.QModelIndex):
        if not index.isValid():
            return Qt.NoItemFlags
        return super(self.__class__, self).flags(index)

    def index(self, row, column, parent=None, *args, **kwargs):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()
        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()
        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        return QModelIndex()

    def parent(self, index:PySide2.QtCore.QModelIndex):
        if not index.isValid():
            return QModelIndex()
        childItem = index.internalPointer()
        parentItem = childItem.parentItem()
        if parentItem == self.rootItem:
            return QModelIndex()
        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent:PySide2.QtCore.QModelIndex=...) -> int:
        if not parent.isValid():
            return self.rootItem.childCount()
        return parent.internalPointer().childCount()

    def columnCount(self, parent:PySide2.QtCore.QModelIndex=...) -> int:
        if not parent.isValid():
            return self.rootItem.columnCount()
        return parent.internalPointer().columnCount()

    def addVariables(self, file_name, variables):
        logger.info("VariableTreeModel.addVariables")
        first_item = VariableTreeItem([file_name], self.rootItem)
        self._items.append(first_item)
        self.rootItem.appendChild(first_item)
        for v in variables:
            new_item = VariableTreeItem([v], first_item)
            first_item.appendChild(new_item)
            self._items.append(new_item)
        self.endResetModel()
