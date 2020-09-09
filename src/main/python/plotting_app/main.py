# -*- coding: utf-8 -*
import os
from pathlib import Path
import sys
import argparse
import logging
from logging.handlers import RotatingFileHandler

from fbs_runtime.application_context.PySide2 import ApplicationContext, cached_property

# if sys.platform == 'win32':
sys.path.insert(0, str(Path(__file__).parent.absolute().parents[0]))
from plotting_app.controllers.main import QtMainController

__version__ = '2020.1.0a1'
CONFIG_DIR = os.path.join(str(Path.home()), ".plotting_app")


class AppContext(ApplicationContext):

    def __init__(self):
        super().__init__()
        self.mc = QtMainController(self, __version__)

    def run(self):
        self.mc()
        return self.app.exec_()

    @property
    def config_dir(self):
        return CONFIG_DIR

    # @cached_property
    # def img_checked(self):
    #     return QtGui.QIcon(self.get_resource("images/checked.png"))
    #
    # @cached_property
    # def img_unchecked(self):
    #     return QtGui.QIcon(self.get_resource("images/unchecked.png"))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', help="run application in DEBUG mode", action='store_const', const=True,
                        default=False, required=False)
    args = parser.parse_args()

    # File handler should always be at least INFO level so we need the application root level to be at least at INFO.
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(module)s/%(funcName)s - %(message)s')
    logger = logging.getLogger("PlottingApp")
    if args.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
    log_file = os.path.join(CONFIG_DIR, "PlottingApp.log")
    log_handler = RotatingFileHandler(log_file, maxBytes=5000, backupCount=2)
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)
    logger.info(f"logging level: {logger.level}")

    appctxt = AppContext()
    sys.exit(appctxt.run())
