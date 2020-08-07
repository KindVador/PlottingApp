# -*- coding: utf-8 -*-
import os
from pathlib import Path
import shutil
import logging
import json

from plotting_app.models.configuration import ApplicationConfigurationModel, JsonSerializable
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
        if os.path.exists(self.filepath):
            self.load_from_disk()
        else:
            self._create_defaults_user_config()

    @property
    def filepath(self):
        return os.path.join(self.folder, self.file_name)

    def _create_defaults_user_config(self):
        main_path = Path(__file__).parent.absolute().parents[1]
        dflt_cfg = main_path.joinpath('data', 'base', 'default.cfg')
        shutil.copyfile(dflt_cfg, self.filepath)

    def add_model_user_configuration(self, name: str, model: JsonSerializable):
        self.model.add_model(name, model)

    def load_from_disk(self):
        with open(os.path.join(self.folder, self.file_name), mode='r') as f:
            pass

    def save_to_disk(self):
        with open(self.filepath, mode='w') as f:
            f.write(self.model.to_json())
        # reset flag
        self.model.is_dirty = False
