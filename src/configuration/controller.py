# -*- coding: utf-8 -*-
import os
from pathlib import Path
import shutil
import logging
import json

from .model import ApplicationConfigurationModel, JsonSerializable
from .view import ApplicationConfigurationView

logger = logging.getLogger("PlottingApp")


class ApplicationConfigurationController(object):
    """
    Class to handle user's preferences for the whole application.

    User's preferences are saved on the disk in the user folder ('~').
    """

    def __init__(self, folder, file_name='PlottingApp.cfg'):
        self.model = None
        self.view = ApplicationConfigurationView()
        self.file_name = file_name
        self.folder = folder

        # check if folder config exists
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
        # check if the file exists
        if not os.path.exists(self.filepath):
            self._create_defaults_user_config()
        self.load_from_disk(os.path.join(self.folder, self.file_name))

    @property
    def filepath(self):
        return os.path.join(self.folder, self.file_name)

    def _create_defaults_user_config(self):
        logger.debug("ApplicationConfigurationController._create_defaults_user_config()")
        main_path = Path(__file__).parent.absolute().parents[1]
        dflt_cfg = main_path.joinpath('resources', 'config', 'default.cfg')
        shutil.copyfile(dflt_cfg, os.path.join(self.folder, self.file_name))

    def add_model_user_configuration(self, name: str, model: JsonSerializable):
        logger.debug(f"ApplicationConfigurationController.add_model_user_configuration({name}, {model})")
        self.model.add_model(name, model)

    def load_from_disk(self, filepath):
        logger.debug("ApplicationConfigurationController.load_from_disk()")
        # test if file is empty before reading it
        if os.path.getsize(filepath) > 0:
            try:
                with open(os.path.join(self.folder, self.file_name), mode='r') as f:
                    self.model = ApplicationConfigurationModel.from_json(json.loads(f.read()))
            except json.decoder.JSONDecodeError as error:
                self.model = ApplicationConfigurationModel()
                logger.error("Invalid configuration file.")
                logger.error(error)
        self.model.apply()

    def save_to_disk(self, filepath=None):
        logger.debug(f"ApplicationConfigurationController.save_to_disk({filepath})")
        if filepath:
            # Save as
            with open(filepath, mode='w') as f:
                f.write(self.model.to_json())
        else:
            # Save
            with open(self.filepath, mode='w') as f:
                f.write(self.model.to_json())
        # reset flag
        self.model.is_dirty = False
