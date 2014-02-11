# -*- python -*-
#
#       Main Window class
#       VPlantsLab GUI is create here
# 
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2013 INRIA - CIRAD - INRA
#
#       File author(s): Julien Coste <julien.coste@inria.fr>
#
#       File contributor(s):
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################


config_file_default = """
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
c.MainWindowConfig.packages = False

# Display control panel
c.MainWindowConfig.controlpanel = False

# Display Help widget
c.MainWindowConfig.helpwidget = False

# Display 3D Viewer
c.MainWindowConfig.viewer3d = False

# Display menu bar
c.MainWindowConfig.menu = True

# Display project tree view
c.MainWindowConfig.project = False

# Display graphical Python interpreter
c.MainWindowConfig.shell = False

# Display search widget for package manager
c.MainWindowConfig.packagesearch = False

# Display logger (usefull to debug)
c.MainWindowConfig.logger = False

# List of graphical Python interpreters, sorted by preference
c.MainWindowConfig.shell_priority = ['oalab:IPythonShell', 'oalab:BuiltinShell']

# Display alea_install_gui
c.MainWindowConfig.store = False

# Display package manager sorted by categories
c.MainWindowConfig.packagecategories = False"""

config_file_mini = """
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
c.MainWindowConfig.packages = False

# Display control panel
c.MainWindowConfig.controlpanel = False

# Display Help widget
c.MainWindowConfig.helpwidget = True

# Display 3D Viewer
c.MainWindowConfig.viewer3d = False

# Display menu bar
c.MainWindowConfig.menu = True

# Display project tree view
c.MainWindowConfig.project = False

# Display graphical Python interpreter
c.MainWindowConfig.shell = True

# Display search widget for package manager
c.MainWindowConfig.packagesearch = False

# Display logger (usefull to debug)
c.MainWindowConfig.logger = False

# List of graphical Python interpreters, sorted by preference
c.MainWindowConfig.shell_priority = ['oalab:IPythonShell', 'oalab:BuiltinShell']

# Display alea_install_gui
c.MainWindowConfig.store = False

# Display package manager sorted by categories
c.MainWindowConfig.packagecategories = False"""

config_file_3d = """
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
c.MainWindowConfig.packages = False

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
c.MainWindowConfig.packagesearch = False

# Display logger (usefull to debug)
c.MainWindowConfig.logger = False

# List of graphical Python interpreters, sorted by preference
c.MainWindowConfig.shell_priority = ['oalab:IPythonShell', 'oalab:BuiltinShell']

# Display alea_install_gui
c.MainWindowConfig.store = False

# Display package manager sorted by categories
c.MainWindowConfig.packagecategories = False"""

config_file_tissue = """
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
c.MainWindowConfig.viewer3d = False

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
c.MainWindowConfig.packagecategories = True"""

config_file_plant = """
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
c.MainWindowConfig.packagecategories = True"""


