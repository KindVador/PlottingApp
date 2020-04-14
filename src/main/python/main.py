# -*- coding: utf-8 -*
import sys
import logging
from logging.handlers import RotatingFileHandler

from fbs_runtime.application_context.PySide2 import ApplicationContext
from PySide2.QtWidgets import QMainWindow

from controllers.main import QtMainController

__version__ = '2020.1.0a1'


if __name__ == '__main__':
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext`

    # File handler should always be at least INFO level so we need the application root level to be at least at INFO.
    levels = [logging.CRITICAL, logging.ERROR, logging.WARN, logging.INFO, logging.DEBUG]
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(module)s/%(funcName)s - %(message)s')
    root_level = logging.INFO
    logger = logging.getLogger("PlottingApp")
    logger.setLevel(root_level)
    log_handler = RotatingFileHandler('PlottingApp.log', maxBytes=500000, backupCount=2)
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)
    logger.info(f"logging level: {root_level}")

    mc = QtMainController(sys.argv, __version__)
    mc()

    # window = QMainWindow()
    # window.resize(250, 150)
    # window.show()
    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)
