# -*- coding: utf-8 -*-
import pytest
from io import StringIO


@pytest.fixture(scope="module")
def user_default_config_file():
    f = StringIO(initial_value='', newline='\n')
    return f
