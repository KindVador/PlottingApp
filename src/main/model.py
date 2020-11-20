# -*- coding: utf-8 -*-
import logging
import typing

import pandas as pd
from PySide2.QtCore import Qt, QAbstractItemModel, QModelIndex
from PySide2.QtWidgets import QTreeWidgetItem


logger = logging.getLogger("PlottingApp")


class TreeItem(object):

    def __init__(self, data, parent=None):
        self.children = []
        self.item_data = data
        self.parent_item = parent

    def add_child(self, child) -> None:
        self.children.append(child)

    def child(self, row: int):
        if row < 0 or row >= self.child_count():
            return None
        else:
            return self.children[row]

    def child_count(self) -> int:
        return len(self.children)

    def column_count(self) -> int:
        return len(self.item_data)

    def data(self, column: int) -> object:
        if column < 0 or column >= self.column_count():
            return None
        else:
            return self.item_data[column]

    def row(self) -> int:
        if self.parent_item:
            return self.parent_item.children.index(self)
        else:
            return 0


class VariableItem(TreeItem):

    def __init__(self, data, key, parent=None):
        super(VariableItem, self).__init__(data, parent)
        self.key = key


class DataSourceItem(TreeItem):

    def __init__(self, data, parent=None):
        super(DataSourceItem, self).__init__(data, parent)


class RootItem(TreeItem):

    def __init__(self, data, parent=None):
        super(RootItem, self).__init__(data, parent)


class DataSource(object):

    def __init__(self, name, data):
        self.name = name
        self.data = data

    @property
    def variables(self):
        if isinstance(self.data, pd.DataFrame):
            return [str(c) for c in self.data.columns]
        else:
            return list()

    @classmethod
    def from_dataframe(cls, name, df):
        return cls(name, df)


class DataSourceModel(QAbstractItemModel):

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        logger.info("Creation of variable tree model")
        self.root_item = RootItem(['Available Variables'])
        self._data_sources = {}

    def __len__(self) -> int:
        return len(self._data_sources)

    def add_source(self, data: DataSource) -> None:
        print('DataSourceModel.add_source', data.name)
        if data.name not in self._data_sources.keys():
            self.beginResetModel()
            self._data_sources[data.name] = data.variables
            dsi = DataSourceItem([data.name], parent=self.root_item)
            for v in data.variables:
                dsi.add_child(VariableItem([v], f"{len(self._data_sources)}@{v}", parent=dsi))
            self.root_item.add_child(dsi)
            self.endResetModel()
        else:
            logger.error(f'A DataSource with the name {data.name} is already opened, please close it before adding the new one')

    def index(self, row: int, column: int, parent: QModelIndex = ...) -> QModelIndex:
        """
        Given a model index for a parent item, this function allows views and delegates to access children of that item.
        If no valid child item - corresponding to the specified row, column, and parent model index, can be found, the
        function must return QModelIndex(), which is an invalid model index.

        Args:
            row (int):
            column (int):
            parent (QModelIndex):

        Returns:
            QModelIndex
        """
        if not self.hasIndex(row, column, parent):
            return QModelIndex()
        parent_item = self.root_item if not parent.isValid() else parent.internalPointer()
        child_item = parent_item.child(row)
        if child_item:
            return self.createIndex(row, column, child_item)
        return QModelIndex()

    def parent(self, child: QModelIndex) -> QModelIndex:
        """
        Provides a model index corresponding to the parent of any given child item. If the model index specified
        corresponds to a top-level item in the model, or if there is no valid parent item in the model, the function
        must return an invalid model index, created with the empty QModelIndex() constructor.

        Args:
            child (QModelIndex):
        Returns:

        """
        if not child.isValid():
            return QModelIndex()

        child_item = child.internalPointer()
        parent_item = child_item.parent_item

        if parent_item is self.root_item:
            return QModelIndex()

        return self.createIndex(parent_item.row(), 0, parent_item)

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        """
        Used by other components to obtain information about each item provided by the model. In many models, the
        combination of flags should include Qt::ItemIsEnabled and Qt::ItemIsSelectable.

        Args:
            index:

        Returns:

        """
        if not index.isValid():
            return Qt.NoItemFlags
        if not self.parent(index).isValid():
            # Case of DataSource item level
            return Qt.NoItemFlags | Qt.ItemIsEnabled
        # other cases
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        """
        Used to supply item data to views and delegates. Generally, models only need to supply data for Qt::DisplayRole
        and any application-specific user roles, but it is also good practice to provide data for Qt::ToolTipRole,
        Qt::AccessibleTextRole, and Qt::AccessibleDescriptionRole. See the Qt::ItemDataRole enum documentation for
        information about the types associated with each role.

        Args:
            index:
            role:

        Returns:

        """
        # logger.info("VariableTreeModel.data", index.row(), index.column(), role)
        if not index.isValid():
            return None

        if role != Qt.DisplayRole:
            return None

        item = index.internalPointer()
        return item.data(index.column())

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> typing.Any:
        """
        Provides views with information to show in their headers. The information is only retrieved by views that can
        display header information.

        Args:
            section:
            orientation:
            role:

        Returns:

        """
        logger.info("VariableTreeModel.headerData")
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.root_item.data(section)
        else:
            return None

    def rowCount(self, parent: QModelIndex = ...) -> int:
        """
        Provides the number of rows of data exposed by the model.

        Args:
            parent:

        Returns:

        """
        if parent.column() > 0:
            return 0

        parent_item = self.root_item if not parent.isValid() else parent.internalPointer()
        return parent_item.child_count()

    def columnCount(self, parent: QModelIndex = ...) -> int:
        """
        Provides the number of columns of data exposed by the model. List models do not provide this function because
        it is already implemented in QAbstractListModel.

        Args:
            parent:

        Returns:

        """
        if parent.isValid():
            return parent.internalPointer().column_count()
        return self.root_item.child_count()


class PlotModel(object):

    def __init__(self):
        self._df = None
        self.parameters_items = []
        self.plots = []
        self.sources = DataSourceModel()

    @property
    def dataframe(self):
        return self._df

    @dataframe.setter
    def dataframe(self, df):
        self._df = df
        self.parameters_items = [QTreeWidgetItem([v]) for v in self._df.columns]

    def add_data_source(self, data: DataSource):
        self.sources.add_source(data)

    def __getitem__(self, item):
        return self.dataframe[item].dropna()

    def data(self, idx, role):
        return self.sources.data(index=idx, role=role)

    def add_plot(self, d, ext, axe=None, marker=None, linestyle=None, drawstyle=None):
        print(d, ext)
        plots_dict = {}
        for var in d.keys():
            rec_var = f'{var}{ext}'
            plots_dict[rec_var] = {'label': var,
                                   'x_data': self[rec_var].index,
                                   'y_data': self[rec_var],
                                   'y_label': var,
                                   'title': f'{var}{ext}',
                                   'short_label': var,
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
