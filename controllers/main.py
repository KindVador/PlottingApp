# -*- coding: utf-8 -*-
import sys
import logging
import pyqtgraph as pg
from PySide2.QtWidgets import QApplication, QMessageBox

from views.main import MainWindow

__version__ = '2019.1.0a'

logger = logging.getLogger("PlottingApp")


class QtMainController(object):
    """
    Main application controller.

    Args:
        app (QApplication):
        db (SqlDataBaseController):
        import_controller (ImportDialogController):
        compute_controller (ComputeController):
        model (TransactionModel):
        view (MainWindow):

    """

    def __init__(self, argv):
        super(self.__class__, self).__init__()
        logger.info("creation of the main controller")
        self.app = QApplication(argv)
        self.app.setStyle('fusion')
        self.model = None
        self.view = MainWindow(__version__)

    def __call__(self, *args, **kwargs):
        logger.info("execution of the main controller")
        self._init_view()
        self.view.show()
        sys.exit(self.app.exec_())

    def _init_view(self):
        logger.info("initialization of the main view")
        self._make_view_connections()

    def _make_view_connections(self):
        logger.info("creation of connections between the main controller and the main view")
        self.view.actionQuit.triggered.connect(self.quit)
        self.view.actionOpen.triggered.connect(self._open)

    def quit(self):
        logger.info("QUIT ACTION")

    def _open(self):
        logger.info("OPEN ACTION")
