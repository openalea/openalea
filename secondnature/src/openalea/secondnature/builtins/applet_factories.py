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
class DT_Logger(DataTypeNoOpen):
    __name__      = "Logger"
    __created_mimetype__ = "application/openalea-logger"
    __icon_rc__   = ":icons/logger.png"

    def __init__(self):
        DataTypeNoOpen.__init__(self)
        from openalea.core.logger import LoggerOffice
        self.loggermodel = LoggerOffice().get_handler("qt")
        self.loggerDoc = self.container_global_data(self.__name__,  self.loggermodel)

    def new(self):
        return self.loggerDoc

class LoggerFactory(AppletBase):
    __name__ = "Openalea.Logger"
    __namespace__ = "Openalea"

    def __init__(self):
        AppletBase.__init__(self)
        self.add_data_type(DT_Logger())

    def get_applet_space(self, data):
        from openalea.visualea.logger import LoggerView
        view  = LoggerView(None, model=data.obj)
        space = LayoutSpace(view)
        return space

logger_f   = LoggerFactory()


###############
# INTERPRETER #
###############
class DT_Interpreter(DataTypeNoOpen):
    __name__      = "Interpreter"
    __created_mimetype__ = "application/openalea-interpreter"
    __icon_rc__   = ":icons/interpreter.png"

    def __init__(self):
        DataTypeNoOpen.__init__(self)
        from code import InteractiveInterpreter as Interpreter
        self.interpretermodel = Interpreter()
        self.interpreterDoc = self.container_global_data(self.__name__,  self.interpretermodel)

    def new(self):
        return self.interpreterDoc

class InterpreterFactory(AppletBase):
    __name__ = "Openalea.Interpreter"

    def __init__(self):
        AppletBase.__init__(self)
        from openalea.visualea.shell import get_shell_class
        self.shellCls = get_shell_class()
        self.add_data_type(DT_Interpreter())

    def get_applet_space(self, data):
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
        return LayoutSpace(view)

interpreter_f   = InterpreterFactory()

###################
# PACKAGE MANAGER #
###################
class DT_PackageManager(DataTypeNoOpen):
    __name__             = "PackageManager"
    __created_mimetype__ = "application/openalea-packagemanager"
    __icon_rc__          = ":icons/packagemanager.png"

    def __init__(self):
        DataTypeNoOpen.__init__(self)
        #lets create the PackageManager ressource
        from openalea.core.pkgmanager import PackageManager
        from openalea.secondnature.ripped.node_treeview import PkgModel

        self.model    = PkgModel(PackageManager())
        self.pmanagerDoc = self.container_global_data(self.__name__, self.model)

    def new(self):
        return self.pmanagerDoc

class PackageManagerFactory(AppletBase):
    __name__ = "Openalea.PackageManager"

    def __init__(self):
        AppletBase.__init__(self)
        self.add_data_type(DT_PackageManager())

    def get_applet_space(self, data):
        from openalea.secondnature.ripped.node_treeview import NodeFactoryTreeView

        view = NodeFactoryTreeView(None)
        view.setModel(data.obj)
        space = LayoutSpace(view)
        return space

pmanager_f = PackageManagerFactory()


###################
# PROJECT MANAGER #
###################
class DT_ProjectManager(DataTypeNoOpen):
    __name__      = "ProjectManager"
    __created_mimetype__ = "application/openalea-projectmanager"
    __icon_rc__   = ":icons/projectmanager.png"

    def __init__(self):
        DataTypeNoOpen.__init__(self)
        #lets create the PackageManager ressource
        from openalea.secondnature.project_view import ProjectManagerTreeModel

        self.model    = ProjectManagerTreeModel()
        self.pmanagerDoc = self.container_global_data(self.__name__, self.model)

    def new(self):
        return self.pmanagerDoc

class ProjectManagerFactory(AppletBase):
    __name__ = "Openalea.ProjectManager"

    def __init__(self):
        AppletBase.__init__(self)
        self.add_data_type(DT_ProjectManager())

    def get_applet_space(self, data):
        from PyQt4 import QtGui, QtCore

        itemDelegate = QtGui.QItemDelegate()

        view = QtGui.QTreeView(None)
        view.setDragEnabled(True)
        view.setModel(data.obj)
        view.setIconSize(QtCore.QSize(16,16))
        view.setItemDelegate(itemDelegate)
        space = LayoutSpace(view)
        return space

projmanager_f = ProjectManagerFactory()


def get_builtins():
    return [logger_f, interpreter_f, pmanager_f, projmanager_f]
