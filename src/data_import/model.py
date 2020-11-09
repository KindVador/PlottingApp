# -*- coding: utf-8 -*-
import io
import logging
import typing
from collections import OrderedDict

import pandas as pd
from PySide2.QtCore import Qt, QAbstractTableModel, QModelIndex, Signal, QObject, QAbstractItemModel

logger = logging.getLogger("PlottingApp")

default_options = {'sep': (';', str), 'skiprows': (None, int), 'decimal': ('.', str), 'header': ('infer', str),
                   'index_col': (None, int), 'na_values': ("?", str), 'nrows': (None, int),
                   'parse_dates': (False, bool), 'keep_date_col': (False, bool), 'comment': ("#", str),
                   'encoding': (None, str)}


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
        self.options = None
        self.indexes = None
        self.types = None
        self.__init_attributes()

    def __init_attributes(self):
        self.options = OrderedDict(sorted({k: v[0] for k, v in default_options.items()}.items()))
        self.indexes = list(self.options.keys())
        self.types = {k: v[1] for k, v in default_options.items()}

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
            if index.column() == 0:
                return self.indexes[index.row()]
            else:
                return self.options[self.indexes[index.row()]]
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
            self.set_option(self.indexes[index.row()], value)
            self.dataChanged.emit(index, index)
            self.option_modified.emit()
            # When 'parse_dates' option is set to True, we need to emit a signal to ask a GMT format to user
            if self.indexes[index.row()] == 'parse_dates' and self.options['parse_dates'] is True:
                self.date_format_required.emit()

        return True

    def clear(self):
        self.beginResetModel()
        self.__init_attributes()
        self.endResetModel()

    def to_dict(self, keep_none_value=True):
        # return {o[0]: o[2](o[1]) for o in self.options if o[1] is not None}
        if keep_none_value:
            return {k: v for k, v in self.options.items()}
        else:
            return {k: v for k, v in self.options.items() if v is not None}

    def set_option(self, name, value):
        # test if option is already defined and add it to indexes if this a new option
        if name not in self.options.keys():
            self.indexes.append(name)
        # update model with new option value
        self.beginResetModel()
        if value is None or value == '':
            self.options[name] = None
        elif self.types[name] is bool:
            if str(value).lower() in {'true', 't', '1'}:
                self.options[name] = True
            else:
                self.options[name] = False
        else:
            self.options[name] = self.types[name](value)
        self.endResetModel()
        # we need to emit a signal to reload with new option value
        self.option_modified.emit()

    def add_option(self, name, value):
        self.set_option(name, value)


class ColumnTableModel(QAbstractTableModel):
    column_modified = Signal()

    def __init__(self):
        super(self.__class__, self).__init__(parent=None)
        self.header = {0: "CSV COLUMN", 1: "TYPE", 2: "NEW NAME"}
        self.columns = []
        self.allowed_types = ['float64', 'float32', 'int64', 'int32', 'bool', 'object', 'str']

    @property
    def renaming_dict(self):
        return {c[0]: c[2] for c in self.columns if c[2] is not None}

    @property
    def types_dict(self):
        return {c[0]: self.__adapt_type(c[1]) for c in self.columns if c[1] is not None}

    @staticmethod
    def __adapt_type(value: str) -> str:
        if value.lower() in ['str', 'string']:
            return 'object'
        elif value.lower() in ['bool', 'boolean', 'bit']:
            return 'Int8'
        elif value.lower() == 'int64':
            return 'Int64'
        elif value.lower() == 'int32':
            return 'Int32'
        else:
            return value

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

    def flags(self, index):
        flags = super(self.__class__, self).flags(index)
        if index.column() > 0:
            flags |= Qt.ItemIsEditable
        return flags

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

    def to_dict(self) -> dict:
        """
        Returns a dict containing only columns to be renamed.

        Returns:
            dict
        """
        return {c[0]: (c[2], c[1]) for c in self.columns if c[2] is not None}

    def setData(self, index: QModelIndex, value: typing.Any, role: int = ...):
        logger.debug(f"ColumnTableModel.setData({index}, {value}, {role})")
        if not index.isValid():
            logger.error("Invalid index sent to ColumnTableModel.setData method")
            return False
        # case of an empty column name
        if index.column() == 2 and len(str(value).strip()) == 0:
            logger.error("Empty column name sent to ColumnTableModel.setData method")
            return False
        # case of a new value
        if role in [Qt.EditRole, Qt.CheckStateRole]:
            self.columns[index.row()][index.column()] = value
            self.dataChanged.emit(index, index)
            self.column_modified.emit()
        return True


class DataFrameTableModel(QAbstractTableModel):
    """
    Model for the preview of a DataFrame in a table.

    Attributes:
        dataframe (pd.DataFrame): pandas DataFrame to be visualized.

    """

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
        logger.debug(f"DateFormatModel.add_item({item_tuple})")
        if isinstance(item_tuple, tuple):
            self.beginInsertRows(QModelIndex(), len(self._items), len(self._items))
            self._items.append(item_tuple)
            self.endInsertRows()
            self.is_dirty = True
        else:
            # TODO log an error or throw an exception
            return

    def remove_item(self, index):
        logger.debug("DateFormatModel.remove_item(", index, ")")
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
        self.columns_model.column_modified.connect(self.update_preview)

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

    @staticmethod
    def _create_dataframe(data, options_dict, renaming_dict=None):
        logger.debug('\n'.join([f'\t\t{k} : {v}' for k, v in options_dict.items()]))

        # drop dtypes from options_dict
        if 'dtype' in options_dict.keys():
            dtype_dict = options_dict.pop('dtype')
        else:
            dtype_dict = None

        # read file using pandas function
        df = pd.read_csv(data, **options_dict)

        if dtype_dict:
            # TODO adapt columns type using dtype_dict
            pass

        # sometimes the last column is empty due to a leading sep at the end of each line.
        if 'Unnamed' in df.columns[-1]:
            df.drop(df.columns[-1], axis=1, inplace=True)

        # df.set_index('GMT', inplace=True, drop=True, append=False)
        # df.index = pd.to_datetime(df.index, format=gmt_format)
        if renaming_dict and len(renaming_dict) > 0:
            df.rename(columns=renaming_dict, inplace=True)
        return df

    def update_preview(self):
        opts = self.options_model.to_dict(keep_none_value=False)
        if self._preview_raw_data:
            rn = self.columns_model.renaming_dict
            # add dtype option in opts dict
            opts['dtype'] = self.columns_model.types_dict
            self.preview_model.dataframe = self._create_dataframe(io.StringIO(self._preview_raw_data), opts, rn)
            # update of columns
            # TODO to be improve as column modifications should be kept when an option is modified
            if len(rn) == 0:
                self.columns_model.clear()
                for c in self.preview_model.dataframe.columns:
                    self.columns_model.add_column(c, str(self.preview_model.dataframe.dtypes[c]), None)

    def get_dataframe(self):
        logger.info('requiring DataFrame object to model')
        opts = self.options_model.to_dict()
        # add dtype option in opts dict
        opts['dtype'] = self.columns_model.types_dict
        return self._create_dataframe(self.csv_path, opts, self.columns_model.renaming_dict)
