# -*- coding: utf-8 -*-
import json
import logging

logger = logging.getLogger("PlottingApp")


class ApplicationConfigurationModel(object):

    def __init__(self):
        self.is_dirty = False
        self._csv_presets = {}

    @property
    def csv_presets(self) -> dict:
        return self._csv_presets

    @csv_presets.setter
    def csv_presets(self, value: dict):
        self.is_dirty = True
        self._csv_presets = value

    def add_csv_preset(self, preset: dict):
        if preset['name'] in self.csv_presets:
            logger.error(f"A preset with the {preset['name']} is already registered")
        else:
            self._csv_presets[preset['name']] = preset['options']
            self.is_dirty = True

    def to_dict(self) -> dict:
        return {'csv_presets': self.csv_presets}
