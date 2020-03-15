# -*- coding: utf-8 -*-
import io
import logging

import pandas as pd
from PySide2.QtCore import Qt, QAbstractTableModel, QModelIndex

logger = logging.getLogger("PlottingApp")


class OptionTableModel(QAbstractTableModel):

    def __init__(self):
        super(self.__class__, self).__init__(parent=None)
        self.header = {0: "OPTION", 1: "VALUE"}
        self.options = []

    def rowCount(self, parent: QModelIndex = ..., *args, **kwargs):
        return len(self.options)

    def columnCount(self, parent: QModelIndex = ..., *args, **kwargs):
        return len(self.header)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            if section in self.header.keys():
                return self.header[section]
            else:
                return None
        else:
            return None

    def data(self, index: QModelIndex, role: int = ...):
        if role == Qt.DisplayRole:
            return self.columns[index.row()][index.column()]
        elif role == Qt.FontRole:
            return None
        elif role == Qt.ForegroundRole:
            return None
        elif role == Qt.TextAlignmentRole:
            if index.column() == 0:
                return int(Qt.AlignLeft | Qt.AlignVCenter)
            else:
                return int(Qt.AlignHCenter | Qt.AlignVCenter)
        else:
            return None

    def clear(self):
        self.beginResetModel()
        self.options = []
        self.endResetModel()


class ColumnTableModel(QAbstractTableModel):

    def __init__(self):
        super(self.__class__, self).__init__(parent=None)
        self.header = {0: "CSV COLUMN", 1: "TYPE", 2: "NEW NAME"}
        self.columns = []

    def rowCount(self, parent: QModelIndex = ..., *args, **kwargs):
        return len(self.columns)

    def columnCount(self, parent: QModelIndex = ..., *args, **kwargs):
        return len(self.header)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            if section in self.header.keys():
                return self.header[section]
            else:
                return None
        else:
            return None

    def data(self, index: QModelIndex, role: int = ...):
        if role == Qt.DisplayRole:
            return self.columns[index.row()][index.column()]
        elif role == Qt.FontRole:
            return None
        elif role == Qt.ForegroundRole:
            return None
        elif role == Qt.TextAlignmentRole:
            if index.column() == 0:
                return int(Qt.AlignLeft | Qt.AlignVCenter)
            else:
                return int(Qt.AlignHCenter | Qt.AlignVCenter)
        else:
            return None

    def clear(self):
        self.beginResetModel()
        self.columns = []
        self.endResetModel()

    def add_column(self, csv_name, data_type, new_name):
        # TODO create function to add column to the model
        self.beginInsertRows(self.index(len(self.columns), 1), len(self.columns), len(self.columns))
        self.columns.append([csv_name, data_type, new_name])
        self.endInsertRows()


class DataFrameTableModel(QAbstractTableModel):

    def __init__(self):
        super(self.__class__, self).__init__(parent=None)
        self._df = None

    @property
    def dataframe(self):
        return self._df

    @dataframe.setter
    def dataframe(self, df):
        self.beginResetModel()
        if isinstance(df, pd.DataFrame):
            self._df = df
            self.endResetModel()
        else:
            self.endResetModel()
            raise TypeError()

    def rowCount(self, parent: QModelIndex = ..., *args, **kwargs):
        if isinstance(self.dataframe, pd.DataFrame):
            return len(self.dataframe)
        else:
            return 0

    def columnCount(self, parent: QModelIndex = ..., *args, **kwargs):
        if isinstance(self.dataframe, pd.DataFrame):
            return len(self.dataframe.columns)
        else:
            return 0

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.dataframe.columns[section]
            # if section in self.header.keys():
            #     return self.header[section]
            # else:
            #     return None
        else:
            return None

    def data(self, index: QModelIndex, role: int = ...):
        if role == Qt.DisplayRole:
            return self.dataframe.iloc[index.row()][index.column()]
        elif role == Qt.FontRole:
            return None
        elif role == Qt.ForegroundRole:
            return None
        elif role == Qt.TextAlignmentRole:
            if index.column() == 0:
                return int(Qt.AlignLeft | Qt.AlignVCenter)
            else:
                return int(Qt.AlignHCenter | Qt.AlignVCenter)
        else:
            return None


class ReadCSVModel(object):

    def __init__(self):
        self._csv_path = None
        self.options_model = OptionTableModel()
        self.columns_model = ColumnTableModel()
        self.preview_model = DataFrameTableModel()
        self._preview_raw_data = None

    @property
    def csv_path(self):
        return self._csv_path

    @csv_path.setter
    def csv_path(self, file_path):
        self._csv_path = file_path
        with open(file_path, mode='r') as input_data:
            self._preview_raw_data = input_data.readline()
            for i in range(15):
                self._preview_raw_data += input_data.readline()
        self.preview_model.dataframe = pd.read_csv(io.StringIO(self._preview_raw_data), sep=';')
        for c in self.preview_model.dataframe.columns:
            self.columns_model.add_column(c, '', c)

