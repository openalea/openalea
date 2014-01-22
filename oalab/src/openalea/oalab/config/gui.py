
__all__ = ['MainWindowConfig']

import sys

from IPython.config.configurable import Configurable
from IPython.config.application import Application
from IPython.utils.traitlets import List, Bool, Unicode

class MainWindowConfig(Configurable):
    shell = Bool(True, config=True, help="Display graphical Python interpreter")
    shell_priority = List(['oalab:IPythonShell', 'oalab:BuiltinShell'], config=True, help="List of graphical Python interpreters, sorted by preference")

    project = Bool(True, config=True, help="Display project tree view")

class MainConfig(Application):
    classes = List([MainWindowConfig])
    config_file = Unicode(u'', config=True,
                  help="Load this config file")

    def initialize(self):
        self.mainwindow_config = MainWindowConfig(config=self.config)
