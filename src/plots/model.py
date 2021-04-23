# -*- coding: utf-8 -*-
import logging
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

    def __getitem__(self, item):
        return self.dataframe[item].dropna()

    def add_plot(self, d, ext, axe=None, marker=None, linestyle=None, drawstyle=None):
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
