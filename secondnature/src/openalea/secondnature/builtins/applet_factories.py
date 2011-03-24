# -*- python -*-
#
#       OpenAlea.Secondnature
#
#       Copyright 2006-2011 INRIA - CIRAD - INRA
#
#       File author(s): Daniel Barbeau <daniel.barbeau@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

__license__ = "CeCILL v2"
__revision__ = " $Id$ "

from openalea.secondnature.api import *

# -- specific imports are inside the classes
# to prevent errors when import this module --

import builtin_icons

##########
# LOGGER #
##########
class DT_Logger(DataFactory):
    __name__             = "Logger"
    __created_mimetype__ = "application/openalea-logger"
    __icon_rc__          = ":icons/logger.png"

    def start(self):
        from openalea.core.logger import LoggerOffice
        self.loggermodel = LoggerOffice().get_handler("qt")
        self.loggerDoc = self.wrap_data(self.__name__,  self.loggermodel, "g")
        return True

    def new(self):
        return self.loggerDoc

class LoggerFactory(AbstractApplet):
    __name__          = "Logger"
    __datafactories__ = [DT_Logger]

    def create_space_content(self, data):
        from openalea.visualea.logger import LoggerView
        view  = LoggerView(None, model=data.obj)
        space = SpaceContent(view)
        return space



###############
# INTERPRETER #
###############
class DT_Interpreter(DataFactory):
    __name__             = "Interpreter"
    __created_mimetype__ = "application/openalea-interpreter"
    __icon_rc__          = ":icons/interpreter.png"

    def start(self):
        from code import InteractiveInterpreter as Interpreter
        self.interpretermodel = Interpreter()
        self.interpreterDoc = self.wrap_data(self.__name__,  self.interpretermodel, "g")
        return True

    def new(self):
        return self.interpreterDoc


class DT_Session(DataFactory):
    __name__             = "Session"
    __created_mimetype__ = "application/openalea-session"

    def start(self):
        from openalea.core.session import Session
        self.__session = Session()
        self.session = self.wrap_data(self.__name__, self.__session, "g")
        return True

    def new(self):
        return self.session


class InterpreterFactory(AbstractApplet):
    __name__ = "Interpreter"
    __datafactories__ = [DT_Interpreter]

    def start(self):
        from openalea.visualea.shell import get_shell_class
        self.shellCls = get_shell_class()

        # just call it, we don't register it as a user visible type
        # because it's just a global thing that can be used
        # by other applets and that has no editor.
        sessionFac = DT_Session()
        DataFactoryManager().add_custom_item("Session", sessionFac)

        return True

    def create_space_content(self, data):
        from openalea.core import cli

        session = GlobalDataManager().get_data_by_name("Session")
        if not session:
            self.logger.error("Couldn't retreive session, logger view cannot be created")
            return
        session = session.obj

        interpreterModel = data.obj
        #managers:
        from openalea.secondnature import layouts
        from openalea.secondnature import applets
        from openalea.secondnature import project
        mgrs = {"layMan":layouts.LayoutManager(),
                "appMan":applets.AppletFactoryManager(),
                "prjMan":project.ProjectManager()}
        view  = self.shellCls(interpreterModel, cli.get_welcome_msg())
        cli.init_interpreter(interpreterModel, session, mgrs)
        return SpaceContent(view)


###################
# PACKAGE MANAGER #
###################
class DT_PackageManager(DataFactory):
    __name__             = "PackageManager"
    __created_mimetype__ = "application/openalea-packagemanager"
    __icon_rc__          = ":icons/packagemanager.png"

    def start(self):
        #lets create the PackageManager ressource
        from openalea.core.pkgmanager import PackageManager
        from openalea.secondnature.ripped.node_treeview import PkgModel
        self.model    = PkgModel(PackageManager())
        self.pmanagerDoc = self.wrap_data(self.__name__, self.model, "g")
        return True

    def new(self):
        return self.pmanagerDoc


class PackageManagerFactory(AbstractApplet):
    __name__ = "PackageManager"
    __datafactories__ = [DT_PackageManager]

    def create_space_content(self, data):
        from openalea.secondnature.ripped.node_treeview import NodeFactoryTreeView

        view = NodeFactoryTreeView(None)
        view.setModel(data.obj)
        space = SpaceContent(view)
        return space



###################
# PROJECT MANAGER #
###################
class DT_ProjectManager(DataFactory):
    __name__      = "ProjectManager"
    __created_mimetype__ = "application/openalea-projectmanager"
    __icon_rc__   = ":icons/projectmanager.png"

    def start(self):
        #lets create the PackageManager ressource
        from openalea.secondnature.project_view import ProjectManagerTreeModel
        self.model       = ProjectManagerTreeModel()
        self.pmanagerDoc = self.wrap_data(self.__name__, self.model, "g")
        return True

    def new(self):
        return self.pmanagerDoc

class ProjectManagerFactory(AbstractApplet):
    __name__ = "ProjectManager"
    __datafactories__ = [DT_ProjectManager]

    def create_space_content(self, data):
        from PyQt4 import QtGui, QtCore

        itemDelegate = QtGui.QItemDelegate()

        view = QtGui.QTreeView(None)
        view.setDragEnabled(True)
        view.setModel(data.obj)
        view.setIconSize(QtCore.QSize(16,16))
        view.setItemDelegate(itemDelegate)
        view.expandAll()
        view.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        menuFunc = self.__make_bound_menu_request_handler(view)
        view.customContextMenuRequested.connect(menuFunc)
        space = SpaceContent(view)
        return space

    def __make_bound_menu_request_handler(self, widget):
        from PyQt4 import QtGui, QtCore
        menu = get_datafactory_menu()
        def onContextMenuRequest(pos):
            menu.popup(widget.viewport().mapToGlobal(pos))
        return onContextMenuRequest

    def __make_datafactory_chosen_handler(self, dt):
        def on_datafactory_chosen(checked):
            data = dt._new_0()
        return on_datafactory_chosen



def get_builtins():
    # interpreter depends on manager being initialised
    return [ProjectManagerFactory(),
            PackageManagerFactory(),
            InterpreterFactory(),
            LoggerFactory()]
