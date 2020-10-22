# -*- coding: utf-8 -*-
import logging

import matplotlib
matplotlib.use("Qt5Agg")
from PySide2.QtWidgets import QWidget, QSizePolicy, QVBoxLayout
from PySide2.QtCore import QSize
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib import rcParams
import mplcursors
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Tahoma']
rcParams['figure.subplot.top'] = 0.977
rcParams['figure.subplot.bottom'] = 0.073
rcParams['figure.subplot.left'] = 0.036
rcParams['figure.subplot.right'] = 0.99
rcParams['figure.subplot.hspace'] = 0.2
rcParams['figure.subplot.wspace'] = 0.2

plt.style.use('ggplot')


logger = logging.getLogger("AFS_TOOLBOX")


class MatplotlibCanvas(Canvas):

    def __init__(self, parent=None, title='', xlabel='', ylabel='', xlim=None, ylim=None, xscale='linear',
                 yscale='linear', width=4, height=3, dpi=100):
        self.figure = Figure(figsize=(width, height), dpi=dpi, tight_layout=True)
        Canvas.__init__(self, self.figure)
        self.setParent(parent)
        Canvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        Canvas.updateGeometry(self)

    def sizeHint(self):
        w, h = self.get_width_height()
        return QSize(w, h)

    def minimumSizeHint(self):
        return QSize(10, 10)

    def update_all_plots(self, configs):
        self.figure.clear()
        self.ax = self.figure.subplots(nrows=len(configs), ncols=1, sharex=True, sharey=False)
        axes = self.figure.get_axes()
        for ax_nb, d in enumerate(configs):
            ax = axes[ax_nb]
            root_variables = set([elt['title'] for k, elt in d.items()])
            if len(root_variables) == 1:
                ax.set_title(root_variables.pop())
                short_label = True
            else:
                ax.set_title(None)
                short_label = False
            for k, v in configs[ax_nb].items():
                lbl = v['short_label'] if short_label else v['label']
                ax.plot(v['x_data'].to_numpy(), v['y_data'].to_numpy(), label=lbl, drawstyle=v['drawstyle'], marker=v['marker'], linestyle=v['linestyle'])
            ax.legend(loc='best', ncol=2, fontsize='small')
            mplcursors.cursor(ax.lines)
        axes[-1].set_xlabel('Time')
        self.draw()

    def clear(self):
        self.figure.clear()
        self.draw()


class MatplotlibWidget(QWidget):

    def __init__(self, parent=None, title='', xlabel='', ylabel='', xlim=None, ylim=None, xscale='linear',
                 yscale='linear', width=11.69, height=8.27, dpi=75):
        super(self.__class__, self).__init__(parent)
        self.setLayout(QVBoxLayout())
        self.canvas = MatplotlibCanvas(self, title, xlabel, ylabel, xlim, ylim, xscale, yscale, width, height, dpi)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.layout().addWidget(self.canvas)

    def set_title(self, title):
        self.canvas.set_title(title)

    def clear(self):
        for ax in self.canvas.figure.get_axes():
            ax.cla()
        self.canvas.clear()

    def update_all_plots(self, configs):
        self.canvas.update_all_plots(configs)


# def plot(df, config, figsize=(25, 20), name="plot"):
#     fig, ax = plt.subplots(nrows=len(config), ncols=1, sharex=True, sharey=False, figsize=figsize)
#     for i, p in enumerate(config):
#         ax[i].plot(df[p], label=p, drawstyle='steps-post')
#         ax[i].set_ylabel(p)
#         #         ax[i].set_ylim([-0.1, 1.1])
#         ax[i].legend()
#         ax[i].grid(which='major', linestyle='-')
#         ax[i].grid(which='minor', linestyle='--')
#     ax[-1].set_xlabel('UTC')
#     # format the ticks for GMT axis
#     ax[-1].xaxis.set_major_locator(gmt_minute_locator)
#     ax[-1].xaxis.set_major_formatter(gmt_axis_fmt)
#     ax[-1].xaxis.set_minor_locator(gmt_second_locator)
#     # format the coords message box
#     #     ax[-1].format_xdata = mdates.DateFormatter('%Y-%m-%d')
#     fig.autofmt_xdate()
#     plt.savefig(f"{name}.png")
#     plt.show()
