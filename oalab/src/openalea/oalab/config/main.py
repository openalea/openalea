# -*- coding: utf-8 -*-

__all__ = ['MainConfig']

from IPython.config.application import Application
from IPython.utils.traitlets import List, Unicode
from openalea.oalab.config.gui import MainWindowConfig

class MainConfig(Application):   
    classes = List([MainWindowConfig])
    config_file = Unicode(u'', config=True,
                  help="Load this config file")

    def initialize(self):
        self.mainwindow_config = MainWindowConfig(config=self.config)
