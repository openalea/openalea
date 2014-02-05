# -*- coding: utf-8 -*-

__all__ = ['MainWindowConfig']

from IPython.config.configurable import Configurable
from IPython.utils.traitlets import List, Bool, Enum

enum_position = Enum(['top', 'bottom']) # TODO: check trait declaration

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
