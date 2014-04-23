
import copy
from openalea.vpltk.plugin import iter_plugins
from openalea.oalab.plugins.minilab import OALabExtensionMini

config_template = """
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
c.MainWindowConfig.controlpanel = False

# Display Help widget
c.MainWindowConfig.helpwidget = True

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
c.MainWindowConfig.store = False

# Display package manager sorted by categories
c.MainWindowConfig.packagecategories = True
"""


class OALabExtensionTissue(OALabExtensionMini):

    data = copy.deepcopy(OALabExtensionMini.data)
    data['extension_name'] = 'tissue'
    data['config_template'] = config_template
