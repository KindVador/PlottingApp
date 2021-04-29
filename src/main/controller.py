# -*- coding: utf-8 -*-
import logging
from pathlib import Path

from PySide2.QtCore import Qt, QSize
from PySide2.QtWidgets import QApplication
from PySide2.QtGui import QIcon
import pandas as pd

from .model import VariableTreeModel
from .view import MainWindow, LogFileWindow
from plots.controller import PlotController
from plots.model import PlotModel
from data_import.controller import ReadCSVController
from configuration.controller import ApplicationConfigurationController

logger = logging.getLogger("PlottingApp")


class QtMainController(object):
    """
    Main application controller.

    Args:
        app (QApplication):
        import_controller (ImportDialogController):
        plot_model (PlotModel):
        view (MainWindow):

    """

    def __init__(self, ctx, version):
        super(self.__class__, self).__init__()
        logger.debug(f"QtMainController.__init__({ctx}, {version})")
        self.ctx = ctx
        self.app = ctx.app
        self.app.setStyle('fusion')
        self.cfg = None
        self.model = VariableTreeModel()
        self.view = MainWindow(version)
        self.plot_model = PlotModel()
        self.plot_controller = PlotController(plt_view=self.view.plot_widget)
        self.log_view = None

    def __call__(self, *args, **kwargs):
        logger.debug(f"QtMainController.__call__({args}, {kwargs})")
        self.load_user_preferences()
        self._init_view()
        self.view.show()

    def load_user_preferences(self, filepath=None):
        logger.debug(f'QtMainController.load_user_preferences(filepath={filepath})')
        if self.cfg is None:
            if filepath:
                p = Path(filepath)
                logger.debug(p.name, p.parent)
                self.cfg = ApplicationConfigurationController(folder=p.parent, file_name=p.name)
            else:
                self.cfg = ApplicationConfigurationController(folder=self.ctx.config_dir)

    def save_user_preferences(self, filepath=None):
        logger.debug(f"QtMainController.save_user_preferences(filepath={filepath})")
        if self.cfg:
            self.cfg.save_to_disk(filepath)

    def _init_view(self):
        logger.info("initialization of the main view")
        # set Application icon
        app_icon = QIcon()
        resources_path = self.ctx.resource_dir
        for size in [16, 24, 32, 64, 128, 256, 512]:
            logger.info(str(resources_path.joinpath(f'icons/base/{str(size)}.png')))
            if not resources_path.joinpath(f'icons/base/{str(size)}.png').exists():
                logger.error(f"ICON FILE NOT FOUND : {str(resources_path.joinpath(f'icons/base/{str(size)}.png'))}")
            app_icon.addFile(str(resources_path.joinpath(f'icons/base/{str(size)}.png')), QSize(size, size))
        self.view.setWindowIcon(app_icon)
        self.view.parameters_tree_widget.setModel(self.model)
        self._make_view_connections()

    def _make_view_connections(self):
        logger.info("creation of connections between the main controller and the main view")
        # menu: File
        self.view.actionOpen.triggered.connect(self._open)
        self.view.actionSave.triggered.connect(self._save)
        self.view.actionClose.triggered.connect(self._close)
        self.view.actionQuit.triggered.connect(self.quit)
        # menu: Data
        self.view.actionCSV.triggered.connect(self.import_data)
        self.view.actionExport.triggered.connect(self.export_data)
        self.view.actionShow_in_table.triggered.connect(self.show_data_table)
        # menu: Help
        self.view.actionAbout.triggered.connect(self.show_about)
        self.view.actionShow_log.triggered.connect(self.show_log)
        # main window
        self.view.parameters_btn.clicked.connect(self.view.show_hide_variables_panel)
        self.view.add_btn.clicked.connect(self._add_clicked)
        self.view.parameters_tree_widget.doubleClicked.connect(self._double_clicked)
        self.view.actionClearAll.triggered.connect(self._clear_all_plots)
        self.view.axe_button_clicked.connect(self.add_to_existing_subplot)
        self.view.remove_axe_button.connect(self.remove_subplot)

    def _open(self):
        logger.info("OPEN ACTION")

    def _save(self):
        logger.info("SAVE ACTION")

    def _close(self):
        logger.info("CLOSE ACTION")

    def quit(self):
        logger.info("QUIT ACTION")
        self.app.closeAllWindows()
        self.app.exit(0)

    def import_data(self):
        logger.info("IMPORT DATA ACTION")
        dic = ReadCSVController(preset_model=self.cfg.model['csv_presets'])
        dic.config_updated.connect(self.cfg.save_to_disk)
        df, file_path = dic.get_data_with_dialog()
        if isinstance(df, pd.DataFrame):
            self.plot_model.dataframe = df
            # updates tree items
            file_name = Path(file_path).name
            self.model.addVariables(file_name, list(df.columns))
            self.view.parameters_tree_widget.resizeColumnToContents(0)

    def export_data(self):
        logger.info("EXPORT DATA ACTION")

    def show_data_table(self):
        logger.info("SHOW DATA TABLE ACTION")

    def show_about(self):
        logger.info("SHOW ABOUT ACTION")

    def show_log(self):
        logger.info("SHOW LOG ACTION")
        if not self.log_view:
            self.log_view = LogFileWindow()
        self.log_view.show_log_content(self.ctx.log_file)

    def _add_clicked(self):
        d = {}
        for si in self.view.parameters_tree_widget.selectedIndexes():
            if si.internalPointer().parentItem() == self.model.rootItem:
                for i in range(si.internalPointer().childCount()):
                    child = si.internalPointer().child(i)
                    d[child.data(0)] = None
            else:
                d[self.model.data(si, Qt.DisplayRole)] = None
        self.view.parameters_tree_widget.clearSelection()
        logger.info(f"add parameter {d}")
        self.add_subplot(d)

    def _double_clicked(self, index):
        if not index.isValid():
            return
        d = {}
        item = index.internalPointer()
        if item.parentItem() == self.model.rootItem:
            for i in range(item.childCount()):
                child = item.child(i)
                d[child.data(0)] = None
        else:
            d[self.model.data(index, Qt.DisplayRole)] = None
        self.view.parameters_tree_widget.clearSelection()
        self.add_subplot(d)

    def add_subplot(self, d):
        if len(d) == 0:
            return
        self.plot_model.add_plot(d, self.view.get_filter_extension(), None)
        self.view.add_axe(len(self.plot_model.plots) - 1)
        self.view.update_plots(self.plot_model.plots)

    def add_to_existing_subplot(self, axe_nb):
        d = self.view.get_selected_parameters_and_clear()
        self.plot_model.add_plot(d, self.view.get_filter_extension(), axe_nb - 1)
        self.view.update_plots(self.plot_model.plots)

    def _clear_all_plots(self):
        logger.info('Clearing all plots')
        self.plot_model.clear_plots_only()
        self.view.clear_all_plots()

    def remove_subplot(self, index):
        logger.info(f"Remove subplot at index: {index}")
        if index == -1:
            return
        elif index == 0 and len(self.plot_model.plots) == 1:
            self._clear_all_plots()
        else:
            self.plot_model.remove_plot(index)
            self.view.remove_axe(len(self.plot_model.plots))
            self.view.update_plots(self.plot_model.plots)
