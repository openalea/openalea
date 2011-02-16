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

from openalea.secondnature.extendable_objects import *

import urlparse
#make urlparse correctly handle the glorious "oa" protocol :)
urlparse.uses_query.append("oa")


##################################################################
# The following dirty block code is currently needed because     #
# the GraphOperators need a reference to the main window.        #
# This is a big design flaw that will be adressed in the future. #
# Not doing this currenly breaks dataflow editing.               #
# Doing it unbreaks some parts of the dataflow editing.          #
##################################################################
from openalea.visualea.mainwindow import MainWindow
from PyQt4 import QtGui
app = QtGui.QApplication.instance()
if app:
    app.post_status_message("Discretly starting visualea because of design issues")
    va = MainWindow(None)
    va.on_session_started(app.get_session())
    va.hide()


from openalea.visualea import dataflowview
from openalea.core.pkgmanager import PackageManager

class PackageManagerFactory(SingletonWidgetFactory):
    __name__ = "PackageManager"
    __namespace__ = "Visualea"

    def handles(self, input):
        False

    def creates_without_data(self):
        return True

    def _instanciate_space(self, input, parent):
        from openalea.secondnature.ripped.node_treeview import NodeFactoryTreeView, PkgModel
        model = PkgModel(PackageManager())
        view  = NodeFactoryTreeView(None, None)
        view.setModel(model)
        return model, LayoutSpace(self.__name__, self.__namespace__, view )

class LoggerFactory(SingletonWidgetFactory):
    __name__ = "Logger"
    __namespace__ = "Visualea"

    def handles(self, input):
        False

    def creates_without_data(self):
        return True

    def _instanciate_space(self, input, parent):
        from openalea.visualea.logger import LoggerView
        from openalea.core.logger import LoggerOffice
        model = LoggerOffice().get_handler("qt")
        view = LoggerView(None, model=model)
        return model, LayoutSpace(self.__name__, self.__namespace__, view )


class DataflowviewFactory(WidgetFactory):
    __name__ = "Dataflowview"
    __namespace__ = "Visualea"
    def _instanciate_space(self, input, parent):
        if not self.handles(input):
            return

        if input is None:
            return

        if input.scheme != "oa":
            return #unhandled url protocol

        if input.netloc != "local":
            return #unhandled oa location

        pName = input.path.strip("/")
        fName = input.query
        pm = PackageManager()
        package = pm[pName]
        factory = package.get_factory(fName)
        node = factory.instantiate()
        gwidget = dataflowview.GraphicalGraph.create_view(node, parent=parent)
        return node, LayoutSpace(self.__name__, self.__namespace__, gwidget)

    def handles(self, input):
        good = isinstance(input, urlparse.ParseResult)
        good &= (input.scheme == "oa")
        good &= (input.netloc == "local")
        return good



# -- instantiate widget factories --
pmanager_f = PackageManagerFactory()
logger_f   = LoggerFactory()
dataflow_f = DataflowviewFactory()





# -- instantiate layouts --
sk = "{0: [1, 2], 2: [3, 4]},"+\
     "{0: None, 1: 0, 2: 0, 3: 2, 4: 2},"+\
     "{0: {'amount': 0.2, 'splitDirection': 1},"+\
     "1: {},"+\
     "2: {'amount': 0.7, 'splitDirection': 2},"+\
     "3: {}, 4: {}}"


df1 = Layout("Dataflow Editing",
             "Visualea",
             skeleton = sk,
             # the widgets we want are those  placed under the
             # `Visualea` application namespace.
             # but you could have "PlantGl.viewer" here too.
             widgetmap={1:"Visualea.PackageManager",
                        4:"Visualea.Logger"})

df2 = Layout("Dataflow Editing2",
             "Visualea",
             skeleton=sk,
             widgetmap={4:"Visualea.PackageManager",
                        3:"Visualea.Logger"})




