# -*- coding: utf-8 -*-
import io
import logging
import typing

import pandas as pd
from PySide2.QtCore import Qt, QAbstractTableModel, QModelIndex, Signal, QObject

logger = logging.getLogger("PlottingApp")

default_options = [['sep', ',', str], ['skiprows', None, int], ['decimal', '.', str], ['header', 'infer', str],
                   ['index_col', None, int], ['na_values', None, str], ['nrows', None, int],
                   ['parse_dates', False, bool], ['keep_date_col', False, bool], ['comment', None, str],
                   ['encoding', None, str]]


class OptionTableModel(QAbstractTableModel):
    option_modified = Signal()
    date_format_required = Signal()

    def __init__(self):
        super(self.__class__, self).__init__(parent=None)
        self.header = {0: "OPTION", 1: "VALUE"}
        self.options = default_options

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

    def flags(self, index):
        flags = super(self.__class__, self).flags(index)
        if index.column() == 1:
            flags |= Qt.ItemIsEditable
        # elif index.column() in (5, 6):
        #     flags |= Qt.ItemIsUserCheckable
        return flags

    def data(self, index: QModelIndex, role: int = ...):
        if role == Qt.DisplayRole:
            return self.options[index.row()][index.column()]
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

    def setData(self, index: QModelIndex, value: typing.Any, role: int = ...):
        if not index.isValid():
            return False

        if role == Qt.EditRole or role == Qt.CheckStateRole:
            if value == '':
                return False
            self.options[index.row()][1] = value
        self.dataChanged.emit(index, index)
        self.option_modified.emit()
        if self.options[index.row()][0] == 'parse_dates':
            self.date_format_required.emit()
        return True

    def clear(self):
        self.beginResetModel()
        self.options = default_options
        self.endResetModel()

    def to_dict(self):
        return {o[0]: o[2](o[1]) for o in self.options if o[1] is not None}


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
            return str(self.dataframe.iloc[index.row()][index.column()])
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


class ReadCSVModel(QObject):

    date_format_required = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._csv_path = None
        self.options_model = OptionTableModel()
        self.columns_model = ColumnTableModel()
        self.preview_model = DataFrameTableModel()
        self.date_format = ''
        self._preview_raw_data = None
        # connect
        self.options_model.option_modified.connect(self.update_preview)
        self.options_model.date_format_required.connect(self.date_format_dialog)

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
        self.update_preview()

    def update_preview(self):
        opts = self.options_model.to_dict()
        print(opts)
        self.preview_model.dataframe = pd.read_csv(io.StringIO(self._preview_raw_data), **opts)
        # update of columns
        self.columns_model.clear()
        for c in self.preview_model.dataframe.columns:
            self.columns_model.add_column(c, '', c)

    def date_format_dialog(self):
        print('date_format_dialog')
        self.date_format_required.emit()
