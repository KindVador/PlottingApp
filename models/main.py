# -*- coding: utf-8 -*-
import logging
import typing

import pandas as pd
import PySide2
from PySide2.QtCore import Qt
from PySide2.QtGui import QStandardItem, QStandardItemModel
from PySide2.QtWidgets import QTreeWidgetItem


logger = logging.getLogger("PlottingApp")


class PlotModel(object):

    def __init__(self):
        self._df = None
        self.parameters_items = []
        self.plots = []

    @property
    def dataframe(self):
        return self._df

    @dataframe.setter
    def dataframe(self, df):
        self._df = df
        self.parameters_items = [QTreeWidgetItem([v]) for v in self._df.columns]
        print(self.parameters_items)

    def __getitem__(self, item):
        return self.dataframe[item]

    def add_plot(self, d, ext, axe=None, marker=None, linestyle=None, drawstyle=None):
        plots_dict = {}
        for root, childs in d.items():
            if childs is not None:
                for c in childs:
                    rec_var = f'{root} ({c}){ext}'
                    plots_dict[rec_var] = {'label': f'{root}({c})',
                                           'x_data': self[rec_var].index,
                                           'y_data': self[rec_var],
                                           'y_label': root,
                                           'title': f'{root}{ext}',
                                           'short_label': f'{c}',
                                           'marker': marker,
                                           'linestyle': linestyle,
                                           'drawstyle': drawstyle}
            else:
                rec_var = f'{root}{ext}'
                plots_dict[rec_var] = {'label': root,
                                       'x_data': self[rec_var].index,
                                       'y_data': self[rec_var],
                                       'y_label': root,
                                       'title': f'{root}{ext}',
                                       'short_label': root,
                                       'marker': marker,
                                       'linestyle': linestyle,
                                       'drawstyle': drawstyle}
        if axe is None:
            self.plots.append(plots_dict)
        else:
            # TODO check if variables are already in axe
            self.plots[axe].update(plots_dict)
        logger.info(f"Add plots for: {[v['label'] for k, v in plots_dict.items()]}")

    def clear(self):
        self._df = None
        self.parameters_items = []
        self.plots = []

    def clear_plots_only(self):
        self.plots = []

    def remove_plot(self, index):
        self.plots.pop(index)


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

