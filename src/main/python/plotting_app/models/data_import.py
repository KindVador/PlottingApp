# -*- coding: utf-8 -*-
import io
import logging
import typing

import pandas as pd
from PySide2.QtCore import Qt, QAbstractTableModel, QModelIndex, Signal, QObject, QAbstractItemModel

logger = logging.getLogger("PlottingApp")

default_options = [['sep', ';', str], ['skiprows', None, int], ['decimal', '.', str], ['header', 'infer', str],
                   ['index_col', None, int], ['na_values', "?", str], ['nrows', None, int],
                   ['parse_dates', False, bool], ['keep_date_col', False, bool], ['comment', "#", str],
                   ['encoding', None, str]]


class PresetBoxModel(QAbstractItemModel):

    def __init__(self, preset_model):
        super(self.__class__, self).__init__(parent=None)
        self.preset_model = preset_model

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.preset_model)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return 1

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if role == Qt.DisplayRole:
            return self.preset_model.names[index.row()]
        else:
            return None

    def index(self, row, column, parent=None, *args, **kwargs):
        return self.createIndex(row, column)

    def parent(self, index):
        return QModelIndex()


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

        if role in [Qt.EditRole, Qt.CheckStateRole]:
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

    def to_dict(self):
        return {c[0]: (c[2], c[1]) for c in self.columns if c[1] is not None}


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


class DateFormatModel(QAbstractItemModel):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._items = []
        self.is_dirty = False

    def add_item(self, item_tuple=("", "")):
        print("DateFormatModel.add_item(", item_tuple, ")")
        if isinstance(item_tuple, tuple):
            self.beginInsertRows(QModelIndex(), len(self._items), len(self._items))
            self._items.append(item_tuple)
            self.endInsertRows()
            self.is_dirty = True
        else:
            # TODO log an error or throw an exception
            return

    def remove_item(self, index):
        print("DateFormatModel.remove_item(", index, ")")
        self.is_dirty = True

    def headerData(self, section, orientation, role=None):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            if section == 0:
                return "NAME"
            else:
                return "FORMAT"
        else:
            return None

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self._items)

    def index(self, row, column, parent=None, *args, **kwargs):
        return self.createIndex(row, column)

    def parent(self, index):
        return QModelIndex()

    def columnCount(self, parent=None, *args, **kwargs):
        return 2

    def flags(self, index):
        flags = super(self.__class__, self).flags(index)
        flags |= Qt.ItemIsEditable
        return flags

    def data(self, index, role=None):
        if role == Qt.DisplayRole:
            return self._items[index.row()][index.column()]
        else:
            return None

    def setData(self, index, value, role=None):
        if role == Qt.EditRole:
            if index.column() == 0:
                self._items[index.row()] = (value, self._items[index.row()][1])
            elif index.column() == 1:
                self._items[index.row()] = (self._items[index.row()][0], value)
            self.dataChanged.emit(index, index)
            return True


class ReadCSVModel(QObject):

    date_format_required = Signal()

    def __init__(self, parent=None, preset_model=None):
        super().__init__(parent)
        self._csv_path = None
        self.options_model = OptionTableModel()
        self.columns_model = ColumnTableModel()
        self.preview_model = DataFrameTableModel()
        self.preset_model = PresetBoxModel(preset_model)
        self.date_format_model = DateFormatModel()
        self._date_format = ''
        self._preview_raw_data = None
        # connect
        self.options_model.option_modified.connect(self.update_preview)
        self.options_model.date_format_required.connect(self.date_format_required.emit)

        # populate model with DateFormat
        # TODO load items from user config file
        self.date_format_model.add_item(('TDA1', 'q-hh-mm-ss'))
        self.date_format_model.add_item(('TDA2', 'q-hh:mm:ss.us'))

    @property
    def csv_path(self):
        return self._csv_path

    @csv_path.setter
    def csv_path(self, file_path):
        self._csv_path = file_path
        with open(file_path, mode='r') as input_data:
            self._preview_raw_data = input_data.readline()
            for _ in range(15):
                self._preview_raw_data += input_data.readline()
        self.update_preview()

    @property
    def date_format(self):
        return self._date_format

    @date_format.setter
    def date_format(self, value):
        if isinstance(value, str):
            self._date_format = value
        else:
            # TODO log an error or throw an exception
            pass

    def update_preview(self):
        opts = self.options_model.to_dict()
        print(opts)
        self.preview_model.dataframe = pd.read_csv(io.StringIO(self._preview_raw_data), **opts)
        # update of columns
        self.columns_model.clear()
        for c in self.preview_model.dataframe.columns:
            self.columns_model.add_column(c, '', c)
