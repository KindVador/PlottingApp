# -*- coding: utf-8 -*
import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from fbs_runtime.application_context.PySide2 import ApplicationContext, cached_property

from plotting_app.controllers.main import QtMainController

__version__ = '2020.1.0a1'


CONFIG_DIR = os.path.join(Path.home(), ".plotting_app")


class UserConfiguration(object):

    def __init__(self):
        pass

    def load(self):
        """
        Loads configuration from disk (Home directory)

        Returns:

        """
        pass


class AppContext(ApplicationContext):

    def run(self):
        mc = QtMainController(self, __version__)
        mc()
        return self.app.exec_()

    # @cached_property
    # def img_checked(self):
    #     return QtGui.QIcon(self.get_resource("images/checked.png"))
    #
    # @cached_property
    # def img_unchecked(self):
    #     return QtGui.QIcon(self.get_resource("images/unchecked.png"))


if __name__ == '__main__':

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

    appctxt = AppContext()
    sys.exit(appctxt.run())
