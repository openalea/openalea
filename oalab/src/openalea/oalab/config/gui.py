
__all__ = ['MainWindowConfig']

import sys

from IPython.config.configurable import Configurable
from IPython.config.application import Application
from IPython.utils.traitlets import List, Bool, Unicode

class MainWindowConfig(Configurable):
    project = Bool(True, config=True, help="Display project tree view")
    packages = Bool(True, config=True, help="Display package manager")
    packagecategories = Bool(True, config=True, help="Display package manager sorted by categories")
    packagesearch = Bool(True, config=True, help="Display search widget for package manager")
    controlpanel = Bool(True, config=True, help="Display control panel")
    viewer3d = Bool(True, config=True, help="Display 3D Viewer")
    logger = Bool(True, config=True, help="Display logger (usefull to debug)")
    help = Bool(True, config=True, help="Display Help widget")
    
    shell = Bool(True, config=True, help="Display graphical Python interpreter")
    shell_priority = List(['oalab:IPythonShell', 'oalab:BuiltinShell'], config=True, help="List of graphical Python interpreters, sorted by preference")

    store = Bool(True, config=True, help="Display alea_install_gui")
    
    menu = Bool(True, config=True, help="Display menu bar")

    
class MainConfig(Application):
    classes = List([MainWindowConfig])
    config_file = Unicode(u'', config=True,
                  help="Load this config file")

    def initialize(self):
        self.mainwindow_config = MainWindowConfig(config=self.config)




default_config_file = """
# Configuration file for application.

c = get_config()

#------------------------------------------------------------------------------
# MainConfig configuration
#------------------------------------------------------------------------------

# This is an application.

# MainConfig will inherit config from: Application

# Set the log level by value or name.
# c.MainConfig.log_level = 30

# The Logging format template
# c.MainConfig.log_format = '[%(name)s]%(highlevel)s %(message)s'

# Load this config file
# c.MainConfig.config_file = u''

# The date format used by logging formatters for %(asctime)s
# c.MainConfig.log_datefmt = '%Y-%m-%d %H:%M:%S'

#------------------------------------------------------------------------------
# MainWindowConfig configuration
#------------------------------------------------------------------------------

# Display package manager
c.MainWindowConfig.packages = True

# Display control panel
c.MainWindowConfig.controlpanel = True

# Display Help widget
c.MainWindowConfig.help = True

# Display 3D Viewer
c.MainWindowConfig.viewer3d = True

# Display menu bar
c.MainWindowConfig.menu = True

# Display project tree view
c.MainWindowConfig.project = True

# Display graphical Python interpreter
c.MainWindowConfig.shell = True

# Display search widget for package manager
c.MainWindowConfig.packagesearch = True

# Display logger (usefull to debug)
c.MainWindowConfig.logger = True

# List of graphical Python interpreters, sorted by preference
c.MainWindowConfig.shell_priority = ['oalab:IPythonShell', 'oalab:BuiltinShell']

# Display alea_install_gui
c.MainWindowConfig.store = True

# Display package manager sorted by categories
c.MainWindowConfig.packagecategories = True"""
