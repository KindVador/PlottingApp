# -*- coding: utf-8 -*-
import os
import json

import pytest
import pandas as pd

from src.data_import.model import ReadCSVModel, default_options


def csv_manifest():
    filepath = os.path.join(os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-3]),
                            os.path.sep.join(['tests_data', 'csv', 'manifest.json']))
    with open(filepath, mode='r') as fs:
        return json.load(fs)


def extract(keys):
    tmp = []
    for f in csv_manifest():
        tmp.append([f[k.strip()] for k in keys.split(',')])
    return tmp


class TestPresetBoxModel(object):

    def test_init(self):
        pass


class TestReadCSVModel(object):

    def test_init(self):
        mdl = ReadCSVModel()
        assert mdl is not None
        assert isinstance(mdl, ReadCSVModel)

    @pytest.mark.parametrize("fn, sep, gmt_fmt, comment, ncol, encoding", extract("filename, sep, gmt_format, comment, ncol, encoding"))
    def test_dataframe_datetime_index(self, csv_folder, fn, sep, gmt_fmt, comment, ncol, encoding):
        mdl = ReadCSVModel()
        mdl.csv_path = os.path.join(csv_folder, fn)
        assert mdl is not None
        assert mdl.csv_path is not None
        # load defaults options in the model
        for k, v in default_options.items():
            mdl.options_model.set_option(k, v[0])
        # set the date_format and some options to have DateTimeIndex
        mdl.date_format = gmt_fmt
        mdl.options_model.set_option('sep', sep)
        mdl.options_model.set_option('index_col', 'GMT')
        mdl.options_model.set_option('parse_dates', True)
        mdl.options_model.set_option('keep_date_col', False)
        mdl.options_model.set_option('comment', comment)
        mdl.options_model.set_option('encoding', encoding)
        df = mdl.get_dataframe()
        assert df is not None
        if mdl.date_format and mdl.options_model.get_option('parse_dates'):
            assert isinstance(df.index, pd.DatetimeIndex)
        else:
            assert isinstance(df.index, pd.RangeIndex)

        if mdl.options_model.get_option('keep_date_col'):
            assert len(df.columns) == ncol
        else:
            assert len(df.columns) == ncol - 1

    @pytest.mark.parametrize("fn, ncol, sep, encoding", extract("filename, ncol, sep, encoding"))
    def test_dataframe_sep(self, csv_folder, fn, ncol, sep, encoding):
        mdl = ReadCSVModel()
        mdl.csv_path = os.path.join(csv_folder, fn)
        assert mdl is not None
        assert mdl.csv_path is not None
        # load defaults options in the model
        for k, v in default_options.items():
            mdl.options_model.set_option(k, v[0])
        mdl.options_model.set_option('sep', sep)
        mdl.options_model.set_option('encoding', encoding)
        df = mdl.get_dataframe()
        assert df is not None
        assert isinstance(df.index, pd.RangeIndex)
        assert len(df.columns) == ncol

    @pytest.mark.parametrize("fn, sep, ncol, skiprows, encoding", extract("filename, sep, ncol, skiprows, encoding"))
    def test_dataframe_skiprows(self, csv_folder, fn, sep, ncol, skiprows, encoding):
        mdl = ReadCSVModel()
        mdl.csv_path = os.path.join(csv_folder, fn)
        assert mdl is not None
        assert mdl.csv_path is not None
        # load defaults options in the model
        for k, v in default_options.items():
            mdl.options_model.set_option(k, v[0])
        mdl.options_model.set_option('sep', sep)
        mdl.options_model.set_option('skiprows', skiprows)
        mdl.options_model.set_option('encoding', encoding)
        df = mdl.get_dataframe()
        assert df is not None
        assert isinstance(df.index, pd.RangeIndex)
        assert len(df.columns) == ncol

    @pytest.mark.parametrize("fn, sep, ncol, decimal, encoding", extract("filename, sep, ncol, decimal, encoding"))
    def test_dataframe_decimal(self, csv_folder, fn, sep, ncol, decimal, encoding):
        mdl = ReadCSVModel()
        mdl.csv_path = os.path.join(csv_folder, fn)
        assert mdl is not None
        assert mdl.csv_path is not None
        # load defaults options in the model
        for k, v in default_options.items():
            mdl.options_model.set_option(k, v[0])
        mdl.options_model.set_option('sep', sep)
        mdl.options_model.set_option('decimal', decimal)
        mdl.options_model.set_option('encoding', encoding)
        df = mdl.get_dataframe()
        assert df is not None
        assert isinstance(df.index, pd.RangeIndex)
        assert len(df.columns) == ncol

    @pytest.mark.parametrize("fn, sep, ncol, header, encoding", extract("filename, sep, ncol, header, encoding"))
    def test_dataframe_header(self, csv_folder, fn, sep, ncol, header, encoding):
        mdl = ReadCSVModel()
        mdl.csv_path = os.path.join(csv_folder, fn)
        assert mdl is not None
        assert mdl.csv_path is not None
        # load defaults options in the model
        for k, v in default_options.items():
            mdl.options_model.set_option(k, v[0])
        mdl.options_model.set_option('sep', sep)
        mdl.options_model.set_option('header', header)
        mdl.options_model.set_option('encoding', encoding)
        df = mdl.get_dataframe()
        assert df is not None
        assert isinstance(df.index, pd.RangeIndex)
        assert len(df.columns) == ncol

    @pytest.mark.parametrize("fn, sep, ncol, index_col, encoding", extract("filename, sep, ncol, index_col, encoding"))
    def test_dataframe_index_col(self, csv_folder, fn, sep, ncol, index_col, encoding):
        mdl = ReadCSVModel()
        mdl.csv_path = os.path.join(csv_folder, fn)
        assert mdl is not None
        assert mdl.csv_path is not None
        # load defaults options in the model
        for k, v in default_options.items():
            mdl.options_model.set_option(k, v[0])
        mdl.options_model.set_option('sep', sep)
        mdl.options_model.set_option('index_col', index_col)
        mdl.options_model.set_option('encoding', encoding)
        df = mdl.get_dataframe()
        assert df is not None
        print(type(df.index))
        if isinstance(index_col, str) and index_col == 'GMT':
            assert isinstance(df.index, pd.Index)
        else:
            assert isinstance(df.index, pd.RangeIndex)

    @pytest.mark.parametrize("fn, sep, ncol, na_values, encoding", extract("filename, sep, ncol, na_values, encoding"))
    def test_dataframe_na_values(self, csv_folder, fn, sep, ncol, na_values, encoding):
        mdl = ReadCSVModel()
        mdl.csv_path = os.path.join(csv_folder, fn)
        assert mdl is not None
        assert mdl.csv_path is not None
        # load defaults options in the model
        for k, v in default_options.items():
            mdl.options_model.set_option(k, v[0])
        mdl.options_model.set_option('sep', sep)
        mdl.options_model.set_option('na_values', na_values)
        mdl.options_model.set_option('encoding', encoding)
        df = mdl.get_dataframe()
        assert df is not None
        assert isinstance(df.index, pd.RangeIndex)
        assert len(df.columns) == ncol

    @pytest.mark.parametrize("fn, sep, ncol, nrows, nblines, comment, encoding", extract("filename, sep, ncol, nrows, nblines, comment, encoding"))
    def test_dataframe_nrows(self, csv_folder, fn, sep, ncol, nrows, nblines, comment, encoding):
        mdl = ReadCSVModel()
        mdl.csv_path = os.path.join(csv_folder, fn)
        assert mdl is not None
        assert mdl.csv_path is not None
        # load defaults options in the model
        for k, v in default_options.items():
            mdl.options_model.set_option(k, v[0])
        mdl.options_model.set_option('nrows', nrows)
        mdl.options_model.set_option('sep', sep)
        mdl.options_model.set_option('comment', comment)
        mdl.options_model.set_option('encoding', encoding)
        df = mdl.get_dataframe()
        assert df is not None
        if isinstance(nrows, int):
            assert len(df) == nrows
        else:
            assert len(df) == nblines
        assert len(df.columns) == ncol

    @pytest.mark.parametrize("fn, sep, ncol, comment, nblines, encoding", extract("filename, sep, ncol, comment, nblines, encoding"))
    def test_dataframe_comment(self, csv_folder, fn, sep, ncol, comment, nblines, encoding):
        mdl = ReadCSVModel()
        mdl.csv_path = os.path.join(csv_folder, fn)
        assert mdl is not None
        assert mdl.csv_path is not None
        # load defaults options in the model
        for k, v in default_options.items():
            mdl.options_model.set_option(k, v[0])
        mdl.options_model.set_option('sep', sep)
        mdl.options_model.set_option('comment', comment)
        mdl.options_model.set_option('encoding', encoding)
        df = mdl.get_dataframe()
        assert df is not None
        assert isinstance(df.index, pd.RangeIndex)
        assert len(df.columns) == ncol
        assert len(df) == nblines

    @pytest.mark.parametrize("fn, sep, ncol, encoding", extract("filename, sep, ncol, encoding"))
    def test_dataframe_encoding(self, csv_folder, fn, sep, ncol, encoding):
        mdl = ReadCSVModel()
        mdl.csv_path = os.path.join(csv_folder, fn)
        assert mdl is not None
        assert mdl.csv_path is not None
        # load defaults options in the model
        for k, v in default_options.items():
            mdl.options_model.set_option(k, v[0])
        mdl.options_model.set_option('encoding', encoding)
        mdl.options_model.set_option('sep', sep)
        df = mdl.get_dataframe()
        assert df is not None
        assert isinstance(df.index, pd.RangeIndex)
        assert len(df.columns) == ncol
