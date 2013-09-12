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
from openalea.oalab.control.controlpanel import ControlPanel, ControlPanelManager
from openalea.oalab.control.observerpanel import ObserverPanel
from openalea.oalab.gui.logger import Logger
from openalea.oalab.gui.help import Help
from openalea.oalab.scene.view3d import Viewer
from openalea.oalab.gui.menu import PanedMenu
from openalea.vpltk.shell.shell import get_interpreter_class, get_shell_class
from openalea.oalab.applets.container import AppletContainer
from openalea.oalab.scene.vplscene import SceneWidget
from openalea.oalab.project.widgets import ProjectWidget
from openalea.oalab.project.treeview import ProjectTreeView
from openalea.oalab.package import PackageViewWidget, PackageCategorieViewWidget, PackageSearchWidget
from openalea.oalab.gui.store import Store
from openalea.vpltk.qt import QtCore

class Session(object):
    """
    Manage session and instanciate all widgets.
    """
    def __init__(self):

        self.cprojname = ""
        self.projects = dict()
        # Menu
        self.menu = PanedMenu()

        # Docks
        self.viewer = Viewer(session=self)
        self.scene_widget = SceneWidget(session=self)
        
        
        self.interpreter = get_interpreter_class()()
        self.shell = get_shell_class()(self.interpreter)        
        
        self.project_widget = ProjectWidget(parent=self)
        
        self.pm = PackageManager()
        self.pm.init(verbose=False)
        
        self.project_tree_view = ProjectTreeView(session=self)
        
        self.package_manager_widget = PackageViewWidget(parent=self)
        self.package_manager_categorie_widget = PackageCategorieViewWidget(parent=self)
        self.package_manager_search_widget = PackageSearchWidget(parent=self)
        
        self.interpreter.locals['projects'] = self.projects
        self.interpreter.locals['session'] = self
        self.interpreter.locals['viewer'] = self.viewer
        self.interpreter.locals['interp'] = self.interpreter
        self._update_locals()
        
        self.control_panel_manager = ControlPanelManager()
        self.control_panel = ControlPanel()
        self.observer_panel = ObserverPanel()
        self.logger = Logger()
        self.help = Help()
        
        # Applet Container : can contain text editor or/and workflow editor
        self.applet_container = AppletContainer(session=self)
        
        self.store = Store(session=self)
        
        self.connect_all_actions()
    
    def _update_locals(self):
        try:
            self.interpreter.locals['project'] = self.project
            self.interpreter.locals['scene'] = self.scene_widget.getScene()
        except:
            pass
        
    def connect_all_actions(self):
        """
        Connect actions of different widget to the menu
        """
        self.connect_actions(self.project_widget, self.menu)
        self.connect_actions(self.applet_container, self.menu)
        self.connect_actions(self.viewer, self.menu)
        self.connect_actions(self.help, self.menu)
        
        # TODO: uncomment for store
        # self.connect_actions(self.store, self.menu)
        
        # TODO:
        # connect control
        # connect observer

    def connect_actions(self, widget, menu):
        """
        Connect actions from 'widget' to 'menu'
        """
        actions = widget.actions()
        #connections = widget.connections()
        
        if actions is not None:
            pane_name = actions[0]
            actions = actions[1]
            for action in actions:
                btn = menu.addBtnByAction(pane_name=pane_name, group_name=action[0], action=action[1],btn_type=action[2])
                #QtCore.QObject.connect(btn, QtCore.SIGNAL('pressed()'),connection)

    @property
    def project(self):
        """
        :return: current project if one is opened. Else return None.
        """
        if len(self.cprojname) ==0:
            # Nothing opened
            return None
        elif self.cprojname.find("no-proj") == -1:
            # Script opened (no project)
            script = self.projects[self.cprojname]
            return script
        else:
            # Project opened
            proj = self.projects[self.cprojname]
            return proj
            
    def current_is_project(self):
        """
        :return: True if current document is a project
        """
        if len(self.cprojname) == 0:
            # Nothing opened
            return False
        elif bool(self.cprojname.find("no-proj") > -1):
            # Script opened (no project)
            return False
        else:
            # Project opened
            return True
            
    def current_is_script(self):
        """
        :return: True if current document is a script (not a project!)
        """
        if len(self.cprojname) ==0:
            # Nothing opened
            return False
        elif bool(self.cprojname.find("no-proj") == -1):
            # Script opened (no project)
            return False
        else:
            # Project opened
            return True

    def get_project(self):
        from warnings import warn
        warn('Deprecated get_project -> project')
        return self.project
