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

from openalea.secondnature.extension_objects import AppletFactory
from openalea.secondnature.extension_objects import Document
from openalea.secondnature.extension_objects import UnregisterableDocument
from openalea.secondnature.extension_objects import LayoutSpace

# -- specific imports are inside the classes
# to prevent errors when import this module --



##########
# LOGGER #
##########
class LoggerFactory(AppletFactory):
    __name__ = "Logger"
    __namespace__ = "Openalea"
    __supports_open__ = False

    def __init__(self):
        AppletFactory.__init__(self)
        from openalea.core.logger import LoggerOffice
        self.loggermodel = LoggerOffice().get_handler("qt")
        self.loggerurl = "oa://logger.local/"
        self.loggerDoc = UnregisterableDocument("Logger",
                                                "Openalea",
                                                self.loggerurl,
                                                self.loggermodel)

    def new_document(self):
        return self.loggerDoc

    def get_applet_space(self, document):
        from openalea.visualea.logger import LoggerView
        view  = LoggerView(None, model=self.loggermodel)
        space = LayoutSpace(self.__name__, self.__namespace__, view )
        return space

logger_f   = LoggerFactory()


###############
# INTERPRETER #
###############
class InterpreterFactory(AppletFactory):
    __name__ = "Interpreter"
    __namespace__ = "Openalea"
    __supports_open__ = False

    def __init__(self):
        AppletFactory.__init__(self)
        from openalea.visualea.shell import get_shell_class
        from code import InteractiveInterpreter as Interpreter

        self.interpretermodel = Interpreter()
        self.interpreterurl = "oa://interpreter.local/"
        self.interpreterDoc = UnregisterableDocument("Interpreter",
                                                     "Openalea",
                                                     self.interpreterurl,
                                                     self.interpretermodel)

        self.shellCls = get_shell_class()

    def new_document(self):
        return self.interpreterDoc

    def get_applet_space(self, document):
        from openalea.core import cli

        # cheating! needed for cli.init_interpreter
        from PyQt4 import QtGui
        session = QtGui.QApplication.instance().get_session()

        #managers:
        from openalea.secondnature import managers
        mgrs = {"layMan":managers.LayoutManager(),
                "appMan":managers.AppletFactoryManager(),
                "docMan":managers.DocumentManager()}
        view  = self.shellCls(self.interpretermodel, cli.get_welcome_msg())
        cli.init_interpreter(self.interpretermodel, session, mgrs)
        space = LayoutSpace(self.__name__, self.__namespace__, view )
        return space

interpreter_f   = InterpreterFactory()


###################
# PACKAGE MANAGER #
###################
class PackageManagerFactory(AppletFactory):
    __name__ = "PackageManager"
    __namespace__ = "Openalea"
    __supports_open__ = False

    def __init__(self):
        AppletFactory.__init__(self)
        #lets create the PackageManager ressource
        from openalea.core.pkgmanager import PackageManager
        from openalea.secondnature.ripped.node_treeview import PkgModel

        self.model    = PkgModel(PackageManager())
        self.pmurl    = "oa://pm.local"
        self.pmanagerDoc = UnregisterableDocument("PackageManager", "Visualea",
                                                  self.pmurl, self.model)

    def new_document(self):
        return self.pmanagerDoc

    def get_applet_space(self, document):
        from openalea.secondnature.ripped.node_treeview import NodeFactoryTreeView

        view = NodeFactoryTreeView(None)
        view.setModel(self.model)
        space = LayoutSpace(self.__name__, self.__namespace__, view )
        return space

pmanager_f = PackageManagerFactory()

def get_builtins():
    return [logger_f, interpreter_f, pmanager_f]
