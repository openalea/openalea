# -*- coding: utf-8 -*-
# -*- python -*-
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
__revision__ = ""

import warnings

from openalea.core.pkgmanager import PackageManager
from openalea.oalab.gui.logger import Logger
from openalea.oalab.control.controlpanel import ControlPanel
from openalea.oalab.gui.help import Help
from openalea.oalab.gui.menu import PanedMenu
from openalea.vpltk.shell.shell import get_interpreter_class, get_shell_class
from openalea.vpltk.qt import QtGui, QtCore
from openalea.oalab.applets.container import AppletContainer
from openalea.oalab.scene.vplscene import VPLScene
from openalea.oalab.project.manager import ProjectManager
from openalea.oalab.project.treeview import ProjectLayoutWidget
from openalea.oalab.package import PackageViewWidget, PackageCategorieViewWidget, PackageSearchWidget
from openalea.oalab.gui.store import Store
from openalea.core.path import path
from openalea.core.settings import get_openalea_home_dir
from openalea.oalab.scene.view3d import Viewer

from openalea.oalab.config.main import MainConfig
  

class Session(object):
    """
    Manage session and instantiate all widgets.
    
    MainWindow works thanks to the session
    """
    def __init__(self):
        self._project = None
        self._is_proj = False
        self._is_script = False

        self.applets = {}

        self._config = MainConfig()
        
        self.extension = None

        self.scene = VPLScene()
        
        # Menu
        self.menu = PanedMenu()

        # Docks
        self.applets['ControlPanel'] = ControlPanel(self)
        self.applets['Viewer3D'] = Viewer(session=self)
        
        self.interpreter = get_interpreter_class()()
        self.shell = get_shell_class()(self.interpreter)        
        
        self.project_manager = ProjectManager(parent=self)

        self.pm = PackageManager()
        self.pm.init(verbose=False)
        
        self.applets['Project'] = ProjectLayoutWidget(session=self)
        
        self.applets['Packages'] = PackageViewWidget(parent=self)
        self.applets['PackageCategories'] = PackageCategorieViewWidget(parent=self)
        self.applets['PackageSearch'] = PackageSearchWidget(parent=self)

        self.applets['Logger'] = Logger()
        self.applets['Help'] = Help()

        self.interpreter.locals['session'] = self
        
        #self.interpreter.locals['ctrl'] = self.applets['ControlPanel']
        #self.interpreter.locals['interp'] = self.interpreter
        self.interpreter.locals['shell'] = self.shell
        self._update_locals()
        
        # Applet Container : can contain text editor or/and workflow editor
        self.applet_container = AppletContainer(session=self)        
        self.interpreter.locals['applets'] = self.applet_container
        
        self.applets['Store'] = Store(session=self)
        
        self.connect_all_actions()
    
    def _update_locals(self):
        try:
            self.interpreter.locals['project'] = self.project
            self.interpreter.locals['controls'] = self.project.controls
            self.interpreter.locals['scene'] = self.scene
        except:
            pass
        
    def connect_all_actions(self):
        """
        Connect actions of different widget to the menu
        """
        self.connect_actions(self.project_manager)
        self.connect_actions(self.applet_container)

        for applet in self.applets.values():
            self.connect_actions(applet)

    def connect_actions(self, widget, menu=None):
        """
        Connect actions from 'widget' to 'menu'
        """
        # TODO : add "show/hide widget" button in menu ribbon bar
        # Maybe do it in mainwindow class to show/hide dockwidget and not widget in dock
        if not menu:
            menu = self.menu
        actions = widget.actions()

        if actions:
            for action in actions:
                menu.addBtnByAction(pane_name=action[0], group_name=action[1], action=action[2],btn_type=action[3])

    @property
    def project(self):
        """
        :return: current project if one is opened. Else return None.
        """
        return self._project
            
    def current_is_project(self):
        """
        :return: True if current document is a project
        """
        return bool(self._is_proj)

    def current_is_script(self):
        """
        :return: True if current document is a script (not a project!)
        """
        return bool(self._is_script)

    def get_project(self):
        warnings.warn('Deprecated get_project -> project')
        return self.project
    
    def load_config_file(self, filename, path=None):
        self._config.load_config_file(filename, path)
                
    config = property(fget=lambda self:self._config.config)
    
    
