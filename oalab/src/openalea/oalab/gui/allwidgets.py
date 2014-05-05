from openalea.oalab.gui.logger import Logger
from openalea.oalab.control.controlpanel import ControlPanel
from openalea.oalab.gui.help import HelpWidget
from openalea.oalab.gui.menu import PanedMenu
from openalea.vpltk.shell.shell import get_shell_class
from openalea.oalab.applets.container import AppletContainer
from openalea.oalab.project.manager import ProjectManagerWidget
from openalea.oalab.project.treeview import ProjectLayoutWidget
from openalea.oalab.package.widgets import PackageViewWidget, PackageCategorieViewWidget, PackageSearchWidget
from openalea.oalab.scene.view3d import Viewer
from openalea.vpltk.qt import QtGui

class AllWidgets(QtGui.QWidget):
    """
    TODO:  This class must be replaced by independent widgets !
    """
    def __init__(self, session):

        super(AllWidgets, self).__init__()

        self.applets = {}
        self.session = session

        # Menu
        self.menu = PanedMenu()
        self.classical_menu = QtGui.QMenuBar()

        self.applets['HelpWidget'] = HelpWidget(session=self.session, controller=self, parent=self)

        # Docks
        self.applets['ControlPanel'] = ControlPanel(session=self.session, controller=self, parent=self)
        self.applets['Viewer3D'] = Viewer(session=self.session, controller=self, parent=self)

        self.shell = get_shell_class()(self.session.interpreter)

        # Applet Container : can contain text editor or/and workflow editor
        self.applet_container = AppletContainer(session=self.session, controller=self, parent=self)
        self.session.interpreter.locals['applets'] = self.applet_container

        self.applets['Project'] = ProjectLayoutWidget(session=self.session, controller=self, parent=self)

        self.project_manager = ProjectManagerWidget(session=self.session, controller=self, parent=self)

        self.helper = self.applets['HelpWidget']
        self.applets['Packages'] = PackageViewWidget(session=self.session, controller=self, parent=self)
        self.applets['PackageCategories'] = PackageCategorieViewWidget(session=self.session, controller=self, parent=self)
        self.applets['PackageSearch'] = PackageSearchWidget(session=self.session, controller=self, parent=self)

        self.applets['Logger'] = Logger(session=self.session, controller=self, parent=self)


        self.session.project_manager.discover()

        """
        proj_model = PrjctManagerModel(self.session.project_manager)
        treeView = QtGui.QTreeView()
        treeView.setModel(proj_model)
        treeView.setHeaderHidden(True)
        self.applets['ProjectManager'] = treeView"""

        self.session.interpreter.locals['shell'] = self.shell
        self.session.interpreter.locals['controller'] = self
        self.update_namespace()

        # self.applets['Store'] = Store(session=self.session, controller=self, parent=self)

        self.connect_all_actions()

    def update_namespace(self):
        self.session.interpreter.locals['project'] = self.session.project
        self.session.interpreter.locals['world'] = self.session.world

        try:
            self.session.interpreter.locals['control'] = self.session.project.control
        except AttributeError:
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
        if not menu:
            menu = self.menu
        actions = widget.actions()

        if actions:
            for action in actions:
                menu.addBtnByAction(pane_name=action[0], group_name=action[1], action=action[2], btn_type=action[3])


                #### Add a classical menu too
                """
                if isinstance(action[2], QtGui.QAction):
                    menus = [men.text() for men in self.classical_menu.actions()]
                    if not action[0] in menus:
                        print [men.text() for men in self.classical_menu.actions()]

                        submenu = self.classical_menu.addMenu(action[0])
                        submenu.addAction(action[2])
                    else:
                        #get menu
                        #add action in menu"""
