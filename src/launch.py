# -*- coding: utf-8 -*
import os
from pathlib import Path
import sys
import argparse
import logging
from logging.handlers import RotatingFileHandler

from PySide2.QtWidgets import QApplication

from main.controller import QtMainController

CONFIG_DIR = os.path.join(str(Path.home()), ".plotting_app")
__version__ = '2020.1.0a1'


class AppContext(object):

    def __init__(self, arguments):
        super().__init__()
        self.args = arguments
        self.version = __version__
        self.app = QApplication([])
        self.app.setStyle('fusion')
        self._logger = None
        self.mc = QtMainController(self, self.version)

    def run(self):
        self.start_log(debug=args.debug)
        self.mc()
        return self.app.exec_()

    @property
    def config_dir(self):
        return CONFIG_DIR

    @property
    def resource_dir(self):
        """

        Returns:

        """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS, and places our data files in a folder
            # relative to that temp folder named as specified in the datas tuple in the spec file
            base_path = Path(sys._MEIPASS)
        except Exception:
            # sys._MEIPASS is not defined, so use the original path
            base_path = Path(__file__).parents[1]
        return base_path.joinpath('resources')

    def start_log(self, debug=False):
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(module)s/%(funcName)s - %(message)s')
        self._logger = logging.getLogger("PlottingApp")
        if debug:
            self._logger.setLevel(logging.DEBUG)
        else:
            self._logger.setLevel(logging.INFO)
        if not os.path.exists(CONFIG_DIR):
            os.makedirs(CONFIG_DIR)
        log_file = os.path.join(CONFIG_DIR, "PlottingApp.log")
        log_handler = RotatingFileHandler(log_file, maxBytes=5000, backupCount=2)
        log_handler.setFormatter(formatter)
        self._logger.addHandler(log_handler)
        self._logger.info(f"logging level: {self._logger.level}")

    @property
    def app_logger(self):
        if self._logger is None:
            self.start_log(False)
        return self._logger


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', help="run application in DEBUG mode", action='store_const', const=True,
                        default=False, required=False)
    args = parser.parse_args()
    appctxt = AppContext(args)
    sys.exit(appctxt.run())
