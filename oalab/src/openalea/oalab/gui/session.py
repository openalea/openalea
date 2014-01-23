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

from openalea.core.pkgmanager import PackageManager
from openalea.oalab.gui.logger import Logger
from openalea.oalab.control.controlpanel import ControlPanel
from openalea.oalab.gui.help import Help
from openalea.oalab.scene.view3d import Viewer
from openalea.oalab.gui.menu import PanedMenu
from openalea.vpltk.shell.shell import get_interpreter_class, get_shell_class
from openalea.oalab.applets.container import AppletContainer
from openalea.oalab.scene.vplscene import VPLScene
from openalea.oalab.project.widgets import ProjectWidget
from openalea.oalab.project.treeview import ProjectLayoutWidget
from openalea.oalab.package import PackageViewWidget, PackageCategorieViewWidget, PackageSearchWidget
from openalea.oalab.gui.store import Store
import warnings

class Session(object):
    """
    Manage session and instanciate all widgets.
    
    MainWindow works thanks to the session
    """
    def __init__(self):
        self._project = None
        self._is_proj = False
        self._is_script = False
        self.scene = VPLScene()
        
        # Menu
        self.menu = PanedMenu()

        # Docks
        self.control_panel = ControlPanel(self)
        
        self.viewer = Viewer(session=self)
        
        self.interpreter = get_interpreter_class()()
        self.shell = get_shell_class()(self.interpreter)        
        
        self.project_widget = ProjectWidget(parent=self)
        
        self.pm = PackageManager()
        self.pm.init(verbose=False)
        
        self.project_layout_widget = ProjectLayoutWidget(session=self)
        
        self.package_manager_widget = PackageViewWidget(parent=self)
        self.package_manager_categorie_widget = PackageCategorieViewWidget(parent=self)
        self.package_manager_search_widget = PackageSearchWidget(parent=self)

        self.logger = Logger()
        self.help = Help()

        self.interpreter.locals['session'] = self
        self.interpreter.locals['viewer'] = self.viewer
        #self.interpreter.locals['ctrl'] = self.control_panel
        #self.interpreter.locals['interp'] = self.interpreter
        self.interpreter.locals['shell'] = self.shell
        self._update_locals()
        
        # Applet Container : can contain text editor or/and workflow editor
        self.applet_container = AppletContainer(session=self)
        
        self.interpreter.locals['applets'] = self.applet_container
        
        self.store = Store(session=self)
        
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
        self.connect_actions(self.project_widget)
        self.connect_actions(self.applet_container)
        self.connect_actions(self.viewer)
        self.connect_actions(self.help)
        self.connect_actions(self.store)        
        # TODO:
        # connect control
        # connect observer

    def connect_actions(self, widget, menu=None):
        """
        Connect actions from 'widget' to 'menu'
        """
        if not menu:
            menu = self.menu
        actions = widget.actions()
        
        if actions is not None:
            pane_name = actions[0]
            actions = actions[1]
            for action in actions:
                menu.addBtnByAction(pane_name=pane_name, group_name=action[0], action=action[1],btn_type=action[2])

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
