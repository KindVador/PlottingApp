# -*- coding: utf-8 -*-
import pytest
from src.main.python.plotting_app.main import UserConfiguration


class UserConfigurationTest(object):

    def test_init(self):
        ucfg = UserConfiguration()
        assert ucfg is not None
        assert isinstance(ucfg, UserConfiguration)
        print(ucfg)
