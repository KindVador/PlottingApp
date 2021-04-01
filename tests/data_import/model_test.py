# -*- coding: utf-8 -*-
import os
import pytest

from src.data_import.model import ReadCSVModel, default_options


class TestPresetBoxModel(object):

    def test_init(self):
        pass


class TestReadCSVModel(object):

    def test_init(self):
        mdl = ReadCSVModel()
        assert mdl is not None
        assert isinstance(mdl, ReadCSVModel)

    def test_get_dataframe(self, csv_folder):
        mdl = ReadCSVModel()
        mdl.csv_path = os.path.join(csv_folder, 'tda_gmt_format1.csv')
        assert mdl is not None
        assert mdl.csv_path is not None
        # load defaults options in the model
        for k, v in default_options.items():
            mdl.options_model.set_option(k, v[0])
        # set the date_format and some options to have DateTimeIndex
        mdl.date_format = 'q-hh:mm:ss-us'
        mdl.options_model.set_option('index_col', 'GMT')
        mdl.options_model.set_option('parse_dates', True)
        df = mdl.get_dataframe()
        print(df.index)
        print(df.head())
