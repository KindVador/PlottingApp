# -*- coding: utf-8 -*-
import os
from pathlib import Path
from configparser import ConfigParser
import shutil
import logging

from plotting_app.models.configuration import ApplicationConfigurationModel
from plotting_app.views.configuration import ApplicationConfigurationView

CONFIG_DIR = os.path.join(str(Path.home()), ".plotting_app")

logger = logging.getLogger("PlottingApp")


class ApplicationConfigurationController(object):
    """
    Class to handle user's preferences for the whole application.

    User's preferences are saved on the disk in the user directory ('~').

    """

    def __init__(self, file_name='PlottingApp.cfg', folder=CONFIG_DIR):
        self.model = ApplicationConfigurationModel()
        self.view = ApplicationConfigurationView()
        self.file_name = file_name
        self.folder = folder

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

    def add_csv_preset(self, new_preset):
        print("ApplicationConfigurationController.add_csv_preset")
        print(new_preset)
