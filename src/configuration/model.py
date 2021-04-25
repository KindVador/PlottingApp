# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
import json
import logging

from matplotlib import rcParams
logger = logging.getLogger("PlottingApp")


class JsonSerializable(metaclass=ABCMeta):
    """
    Class to define method required to serialized object in JSON format.
    """

    json_name = None

    @abstractmethod
    def to_json(self) -> str:
        pass


class PlottingConfigModel(JsonSerializable):
    """
    Model to handle all parameters related to plotting library
    """

    json_name = 'plotting_config'

    def __init__(self):
        self._config = {}

    def add(self, name: str, dct: dict):
        if name not in self._config:
            self._config[name] = dct
        else:
            logger.error(f"Parameter's name '{name}' already exists in the model")

    def apply(self):
        for k, v in self._config.items():
            rcParams[k] = v

    def to_json(self) -> str:
        return json.dumps(self._config, sort_keys=True, indent=4)

    def to_dict(self) -> dict:
        return self._config

    @classmethod
    def from_dict(cls, dct: dict):
        pm = PlottingConfigModel()
        for k, v in dct.items():
            pm.add(k, v)
        return pm


class PresetModel(JsonSerializable):

    json_name = 'csv_presets'

    def __init__(self):
        super(self.__class__, self).__init__()
        self._presets = {}

    @property
    def names(self) -> list:
        return list(self._presets.keys())

    def __len__(self) -> int:
        return len(self._presets)

    def __getitem__(self, item):
        return self._presets[item]

    def __setitem__(self, key, value):
        self.add(name=key, dct=value)

    def add(self, name: str, dct: dict):
        if name not in self._presets:
            self._presets[name] = dct
        else:
            logger.error(f"Preset's name '{name}' already exists in the model")

    def to_json(self):
        return json.dumps(self._presets, sort_keys=True, indent=4)

    def to_dict(self) -> dict:
        return self._presets

    @classmethod
    def from_dict(cls, dct: dict):
        pm = PresetModel()
        for k, v in dct.items():
            pm.add(k, v)
        return pm


class ApplicationConfigurationModel(JsonSerializable):

    def __init__(self):
        super(self.__class__, self).__init__()
        self._models = {PresetModel.json_name: PresetModel(),
                        PlottingConfigModel.json_name: PlottingConfigModel()}
        self.is_dirty = False

    @property
    def models(self) -> dict:
        return self._models

    def __getitem__(self, item):
        logger.debug(f"ApplicationConfigurationModel.__getitem__({item})")
        return self._models[item]

    def __setitem__(self, key, value):
        logger.debug(f"ApplicationConfigurationModel.__setitem__({key}, {value})")
        self._models[key] = value

    def reset(self):
        self._models = {}

    def apply(self):
        if self.get_model(PlottingConfigModel.json_name):
            self.get_model(PlottingConfigModel.json_name).apply()

    def add_model(self, name: str, model: JsonSerializable):
        logger.debug(f"ApplicationConfigurationModel.add_model({name}, {model})")
        if name in self._models.keys():
            logger.error(f"Model's name '{name}' already exists in the ApplicationConfigurationModel")
        elif not isinstance(model, JsonSerializable):
            logger.error("model should be an instance of AbstractConfigurationModel")
        else:
            self._models[name] = model
            self.is_dirty = True

    def get_model(self, model_name):
        if model_name in self.models.keys():
            return self.models.get(model_name)
        else:
            return None

    @classmethod
    def from_json(cls, dct: dict):
        logger.debug(f"ApplicationConfigurationModel.from_json({dct})")
        apm = ApplicationConfigurationModel()
        apm.reset()
        for m in [PresetModel, PlottingConfigModel]:
            if m.json_name in dct.keys():
                apm.add_model(m.json_name, m.from_dict(dct[m.json_name]))
            else:
                apm.add_model(m.json_name, m())
        return apm

    def to_json(self):
        logger.debug("ApplicationConfigurationModel.to_json()")
        return json.dumps({k: v.to_dict() for k, v in self._models.items()}, sort_keys=True, indent=4)
