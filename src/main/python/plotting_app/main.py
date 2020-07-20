# -*- coding: utf-8 -*
import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from configparser import ConfigParser
import shutil

from fbs_runtime.application_context.PySide2 import ApplicationContext, cached_property

from plotting_app.controllers.main import QtMainController
from plotting_app.models.configuration import UserConfigurationModel

__version__ = '2020.1.0a1'


CONFIG_DIR = os.path.join(str(Path.home()), ".plotting_app")


class UserConfiguration(object):
    """
    Class to handle user's preferences for the whole application.

    User's preferences are saved on the disk in the user directory ('~').

    """

    def __init__(self, file_name='PlottingApp.cfg', folder=CONFIG_DIR, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_name = file_name
        self.folder = folder
        self.model = UserConfiguration()

        # check if folder config exists
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
        # check if the file exists
        if not os.path.exists(self.filepath):
            self._create_defaults_user_config()

    @property
    def filepath(self):
        return os.path.join(self.folder, self.file_name)

    @classmethod
    def from_ini_file(cls, file_path):
        parser = ConfigParser()
        # TODO read complete configuration
        parser.read(file_path)

    def _create_defaults_user_config(self):
        main_path = Path(__file__).parent.absolute().parents[1]
        dflt_cfg = main_path.joinpath('data', 'base', 'default.cfg')
        shutil.copyfile(dflt_cfg, self.filepath)


class AppContext(ApplicationContext):

    def __init__(self):
        super().__init__()
        self.cfg = UserConfiguration()
        self.mc = QtMainController(self, __version__)

    def run(self):
        self.mc()
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
