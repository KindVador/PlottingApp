# -*- coding: utf-8 -*-


class UserConfigurationModel(object):

    def __int__(self):
        self._csv_presets = {}

    @property
    def csv_presets(self) -> dict:
        return self._csv_presets

    @csv_presets.setter
    def csv_presets(self, presets: dict):
        self._csv_presets = presets

    def add_csv_preset(self, name: str, preset: dict):
        self._csv_presets[name] = preset
