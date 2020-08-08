# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
import json
import logging

logger = logging.getLogger("PlottingApp")


class JsonSerializable(metaclass=ABCMeta):
    """
    Class to define method required to serialized object in JSON format.
    """

    @abstractmethod
    def to_json(self) -> str:
        pass


class PresetModel(JsonSerializable):

    def __init__(self):
        super(self.__class__, self).__init__()
        self._presets = {}

    @property
    def names(self) -> list:
        return list(self._presets.keys())

    def __len__(self) -> int:
        return len(self._presets)

    def add(self, name: str, options: dict):
        if name not in self._presets:
            self._presets[name] = {'options': options}
        else:
            logger.error(f"Preset's name '{name}' already exists in the model")

    def to_json(self):
        return json.dumps(self._presets, sort_keys=True, indent=4)

    def to_dict(self):
        return self._presets


class ApplicationConfigurationModel(JsonSerializable):

    def __init__(self):
        super(self.__class__, self).__init__()
        self._models = {'csv_presets': PresetModel()}
        self.is_dirty = False

    @property
    def models(self) -> dict:
        return self._models

    def __getitem__(self, item):
        return self._models[item]

    def __setitem__(self, key, value):
        self._models[key] = value

    def add_model(self, name: str, model: JsonSerializable):
        if name in self._models.keys():
            logger.error(f"Model's name '{name}' already exists in the ApplicationConfigurationModel")
        elif not isinstance(model, JsonSerializable):
            logger.error("model should be an instance of AbstractConfigurationModel")
        else:
            self._models[name] = model
            self.is_dirty = True

    @classmethod
    def from_json(cls):
        # TODO
        return cls()

    def to_json(self):
        return json.dumps({k: v.to_dict() for k, v in self._models.items()}, sort_keys=True, indent=4)
