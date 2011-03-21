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
    __name__      = "Logger"
    __created_mimetype__ = "application/openalea-logger"
    __icon_rc__   = ":icons/logger.png"

    def __init__(self):
        DataFactory.__init__(self)
        from openalea.core.logger import LoggerOffice
        self.loggermodel = LoggerOffice().get_handler("qt")
        self.loggerDoc = self.wrap_data(self.__name__,  self.loggermodel, "g")

    def new(self):
        return self.loggerDoc

class LoggerFactory(AbstractApplet):
    __name__ = "Logger"
    __namespace__ = "Openalea"

    def __init__(self):
        AbstractApplet.__init__(self)
        self.add_data_type(DT_Logger())

    def create_space_content(self, data):
        from openalea.visualea.logger import LoggerView
        view  = LoggerView(None, model=data.obj)
        space = SpaceContent(view)
        return space

logger_f   = LoggerFactory()


###############
# INTERPRETER #
###############
class DT_Interpreter(DataFactory):
    __name__      = "Interpreter"
    __created_mimetype__ = "application/openalea-interpreter"
    __icon_rc__   = ":icons/interpreter.png"

    def __init__(self):
        DataFactory.__init__(self)
        from code import InteractiveInterpreter as Interpreter
        self.interpretermodel = Interpreter()
        self.interpreterDoc = self.wrap_data(self.__name__,  self.interpretermodel, "g")

    def new(self):
        return self.interpreterDoc

class InterpreterFactory(AbstractApplet):
    __name__ = "Interpreter"

    def __init__(self):
        AbstractApplet.__init__(self)
        from openalea.visualea.shell import get_shell_class
        self.shellCls = get_shell_class()
        self.add_data_type(DT_Interpreter())

    def create_space_content(self, data):
        from openalea.core import cli

        # cheating! needed for cli.init_interpreter
        from PyQt4 import QtGui
        session = QtGui.QApplication.instance().get_session()

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

interpreter_f   = InterpreterFactory()

###################
# PACKAGE MANAGER #
###################
class DT_PackageManager(DataFactory):
    __name__             = "PackageManager"
    __created_mimetype__ = "application/openalea-packagemanager"
    __icon_rc__          = ":icons/packagemanager.png"

    def __init__(self):
        DataFactory.__init__(self)
        #lets create the PackageManager ressource
        from openalea.core.pkgmanager import PackageManager
        from openalea.secondnature.ripped.node_treeview import PkgModel

        self.model    = PkgModel(PackageManager())
        self.pmanagerDoc = self.wrap_data(self.__name__, self.model, "g")

    def new(self):
        return self.pmanagerDoc

class PackageManagerFactory(AbstractApplet):
    __name__ = "PackageManager"

    def __init__(self):
        AbstractApplet.__init__(self)
        self.add_data_type(DT_PackageManager())

    def create_space_content(self, data):
        from openalea.secondnature.ripped.node_treeview import NodeFactoryTreeView

        view = NodeFactoryTreeView(None)
        view.setModel(data.obj)
        space = SpaceContent(view)
        return space

pmanager_f = PackageManagerFactory()


###################
# PROJECT MANAGER #
###################
class DT_ProjectManager(DataFactory):
    __name__      = "ProjectManager"
    __created_mimetype__ = "application/openalea-projectmanager"
    __icon_rc__   = ":icons/projectmanager.png"

    def __init__(self):
        DataFactory.__init__(self)
        #lets create the PackageManager ressource
        from openalea.secondnature.project_view import ProjectManagerTreeModel

        self.model    = ProjectManagerTreeModel()
        self.pmanagerDoc = self.wrap_data(self.__name__, self.model, "g")

    def new(self):
        return self.pmanagerDoc

class ProjectManagerFactory(AbstractApplet):
    __name__ = "ProjectManager"

    def __init__(self):
        AbstractApplet.__init__(self)
        self.add_data_type(DT_ProjectManager())

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
        def onContextMenuRequest(pos):

            from openalea.secondnature.data import DataSourceManager
            datafactories = sorted(DataSourceManager().gather_items().itervalues(),
                               lambda x,y:cmp(x.name, y.name))

            menu = QtGui.QMenu(widget)
            for dt in datafactories:
                action = menu.addAction(dt.icon, dt.name)
                func = self.__make_datafactory_chosen_handler(dt)
                action.triggered.connect(func)

            menu.popup(widget.viewport().mapToGlobal(pos))
        return onContextMenuRequest

    def __make_datafactory_chosen_handler(self, dt):
        def on_datafactory_chosen(checked):
            data = dt._new_0()
        return on_datafactory_chosen


projmanager_f = ProjectManagerFactory()


def get_builtins():
    return [logger_f, interpreter_f, pmanager_f, projmanager_f]
