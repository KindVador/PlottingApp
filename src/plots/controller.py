# -*- coding: utf-8 -*-

from .model import PlotModel
from .view import MatplotlibWidget


class PlotController(object):
    def __init__(self, plt_view):
        self.model = PlotModel()
        self.view = plt_view
