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
# from openalea.visualea.mainwindow import MainWindow
# from PyQt4 import QtGui
# app = QtGui.QApplication.instance()
# if app:
#     app.post_status_message("Discretly starting visualea because of design issues")
#     va = MainWindow(None)
#     va.on_session_started(app.get_session())
#     va.hide()


from openalea.visualea import dataflowview
from openalea.core.pkgmanager import PackageManager
from openalea.core.compositenode import CompositeNodeFactory, CompositeNode

from openalea.secondnature.ripped.node_treeview import NodeFactoryTreeView, PkgModel
model = PkgModel(PackageManager())
pmanager = Document("PackageManager", "Visualea", "PackageManager", model, category="system")


class PackageManagerFactory(SingletonWidgetFactory):
    __name__ = "PackageManager"
    __namespace__ = "Visualea"

    def handles(self, input):
        return isinstance(input, PkgModel)

    def _instanciate_space(self, input, parent):
        assert isinstance(input, PkgModel)
        view  = NodeFactoryTreeView(None, None)
        view.setModel(input)
        return None, LayoutSpace(self.__name__, self.__namespace__, view )




class DataflowviewFactory(WidgetFactory):
    __name__ = "Dataflowview"
    __namespace__ = "Visualea"

    def __init__(self):
        WidgetFactory.__init__(self)
        self.__emptyNodeFactory = CompositeNodeFactory("Dataflow")

    def _instanciate_space(self, input, parent):
        node = None
        if input is None:
            node = self.__emptyNodeFactory.instantiate()
            node.set_caption("new dataflow")

        if node is None and isinstance(input, urlparse.ParseResult):
            if input.scheme != "oa":
                return None, None #unhandled url protocol

            if input.netloc != "local":
                return None, None#unhandled oa location

            pName = input.path.strip("/")
            fName = input.query
            pm = PackageManager()
            package = pm[pName]
            factory = package.get_factory(fName)
            node = factory.instantiate()

        gwidget = dataflowview.GraphicalGraph.create_view(node, parent=parent)
        document = Document(node.caption, "Visualea", input, node)
        return document, LayoutSpace(self.__name__, self.__namespace__, gwidget)

    def handles(self, input):
        good = isinstance(input, (urlparse.ParseResult, CompositeNode))
        good &= (input.scheme == "oa")
        good &= (input.netloc == "local")
        return good



# -- instantiate widget factories --
dataflow_f = DataflowviewFactory()
pmanager_f = PackageManagerFactory()




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
                        4:"Openalea.Logger"})

df2 = Layout("Dataflow Editing2",
             "Visualea",
             skeleton=sk,
             widgetmap={4:"Visualea.PackageManager",
                        3:"Openalea.Logger"})




