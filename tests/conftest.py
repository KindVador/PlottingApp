# -*- coding: utf-8 -*-
import os

import pytest


@pytest.fixture(scope="session")
def csv_folder():
    return os.path.join(os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-2]),
                        os.path.sep.join(['tests_data', 'csv']))
