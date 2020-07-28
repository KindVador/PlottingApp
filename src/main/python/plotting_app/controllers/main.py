# -*- coding: utf-8 -*-
import logging

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication

from plotting_app.views.main import MainWindow
from plotting_app.models.main import PlotModel
from plotting_app.controllers.data_import import ReadCSVController
from plotting_app.controllers.configuration import ApplicationConfigurationController

logger = logging.getLogger("PlottingApp")


class QtMainController(object):
    """
    Main application controller.

    Args:
        app (QApplication):
        import_controller (ImportDialogController):
        model (PlotModel):
        view (MainWindow):

    """

    def __init__(self, ctx, version):
        super(self.__class__, self).__init__()
        logger.info("creation of the main controller")
        self.app = ctx.app
        self.app.setStyle('fusion')
        self.cfg = ApplicationConfigurationController()
        self.model = PlotModel()
        self.view = MainWindow(version)

    def __call__(self, *args, **kwargs):
        logger.info("execution of the main controller")
        self._init_view()
        self.view.show()

    def _init_view(self):
        logger.info("initialization of the main view")
        self._make_view_connections()

    def _make_view_connections(self):
        logger.info("creation of connections between the main controller and the main view")
        self.view.actionQuit.triggered.connect(self.quit)
        self.view.actionOpen.triggered.connect(self._open)
        self.view.parameters_btn.clicked.connect(self.view.show_hide_variables_panel)
        self.view.add_btn.clicked.connect(self._add_clicked)
        self.view.parameters_tree_widget.itemDoubleClicked.connect(self._double_clicked)
        self.view.btn_clear_plots.clicked.connect(self._clear_all_plots)
        self.view.remove_cbx.activated.connect(self.remove_subplot)
        self.view.axe_button_clicked.connect(self.add_to_existing_subplot)

    def quit(self):
        logger.info("QUIT ACTION")
        self.app.closeAllWindows()
        self.app.exit(0)

    def _open(self):
        logger.info("OPEN ACTION")
        dic = ReadCSVController()
        # connect signal
        dic.new_csv_preset.connect(self.cfg.add_csv_preset)
        self.model.dataframe = dic.get_data_with_dialog()
        # updates tree items
        self.view.parameters_tree_widget.insertTopLevelItems(0, self.model.parameters_items)
        self.view.parameters_tree_widget.resizeColumnToContents(0)

    def _add_clicked(self):
        d = {}
        for si in self.view.parameters_tree_widget.selectedItems():
            print(si)
            if si.parent():
                if si.parent().data(0, Qt.DisplayRole) in d:
                    d[si.parent().data(0, Qt.DisplayRole)] += [si.data(0, Qt.DisplayRole)]
                else:
                    d[si.parent().data(0, Qt.DisplayRole)] = [si.data(0, Qt.DisplayRole)]
            elif si.childCount() > 0:
                d[si.data(0, Qt.DisplayRole)] = [si.child(i).data(0, Qt.DisplayRole) for i in range(si.childCount())]
            else:
                d[si.data(0, Qt.DisplayRole)] = None
        self.view.parameters_tree_widget.clearSelection()
        print(d)
        self.add_subplot(d)

    def _double_clicked(self, item, column):
        if item is None:
            return
        d = {}
        if item.parent():
            d[item.parent().data(0, Qt.DisplayRole)] = [item.data(0, Qt.DisplayRole)]
        elif item.childCount() > 0:
            d[item.data(0, Qt.DisplayRole)] = [item.child(i).data(0, Qt.DisplayRole) for i in range(item.childCount())]
        else:
            d[item.data(0, Qt.DisplayRole)] = None
        self.view.parameters_tree_widget.clearSelection()
        self.add_subplot(d)

    def add_subplot(self, d):
        if len(d) == 0:
            return
        self.model.add_plot(d, self.view.get_filter_extension(), None, self.view.get_marker(),
                            self.view.get_line_style(), self.view.get_drawstyle())
        self.view.add_axe(len(self.model.plots) - 1)
        self.view.update_plots(self.model.plots)

    def add_to_existing_subplot(self, axe_nb):
        d = self.view.get_selected_parameters_and_clear()
        self.model.add_plot(d, self.view.get_filter_extension(), axe_nb - 1, self.view.get_marker(),
                            self.view.get_line_style(), self.view.get_drawstyle())
        self.view.update_plots(self.model.plots)

    def _clear_all_plots(self):
        self.model.clear_plots_only()
        self.view.clear_all_plots()

    def remove_subplot(self, index):
        if index == -1:
            return
        elif index == 0 and len(self.model.plots) == 1:
            self._clear_all_plots()
        else:
            self.model.remove_plot(index)
            self.view.remove_axe(len(self.model.plots))
            self.view.update_plots(self.model.plots)
