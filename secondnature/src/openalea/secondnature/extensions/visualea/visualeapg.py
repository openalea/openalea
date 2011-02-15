
from openalea.secondnature.applications import *


sk = "{0: [1, 2], 2: [3, 4]},"+\
     "{0: None, 1: 0, 2: 0, 3: 2, 4: 2},"+\
     "{0: {'amount': 0.2, 'splitDirection': 1},"+\
     "1: {},"+\
     "2: {'amount': 0.7, 'splitDirection': 2},"+\
     "3: {}, 4: {}}"


from openalea.core.pkgmanager import PackageManager

class PackageManagerFactory(SingletonWidgetFactory):
    __name__ = "PackageManager"
    def _make_instance(self, *args, **kwargs):
        from openalea.secondnature.ripped.node_treeview import NodeFactoryTreeView, PkgModel
        model = PkgModel(PackageManager())
        view  = NodeFactoryTreeView(None, None)
        view.setModel(model)
        return PaneGroup(view)

class LoggerFactory(SingletonWidgetFactory):
    __name__ = "Logger"
    def _make_instance(self, *args, **kwargs):
        from openalea.visualea.logger import LoggerView
        from openalea.core.logger import LoggerOffice
        model = LoggerOffice().get_handler("qt")
        return PaneGroup(LoggerView(None, model=model))


from openalea.visualea import dataflowview
import urlparse
from urlparse import urlparse as uparse

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


class DataflowviewFactory(WidgetFactory):
    __name__ = "Dataflowview"
    def _make_instance(self, parsedUrl, parent):
        if parsedUrl is None:
            return

        if parsedUrl.scheme != "oa":
            return #unhandled url protocol

        if parsedUrl.netloc != "local":
            return #unhandled oa location

        pName = parsedUrl.path.strip("/")
        fName = parsedUrl.query
        pm = PackageManager()
        package = pm[pName]
        factory = package.get_factory(fName)
        node = factory.instantiate()
        gwidget = dataflowview.GraphicalGraph.create_view(node, parent=parent)
        return node, gwidget

    def handles(self, parsedUrl ):
        good = True
        good &= (parsedUrl.scheme == "oa")
        good &= (parsedUrl.netloc == "local")
        return good



# -- instantiate widget factories --
pmanager_f = PackageManagerFactory("Visualea")
logger_f   = LoggerFactory("Visualea")
dataflow_f = DataflowviewFactory("Visualea")


# -- instantiate layouts --
df1 = Layout("Visualea",
             "Dataflow Editing",
             skeleton = sk,
             # the widgets we want are those  placed under the
             # `Visualea` application namespace.
             # but you could have "PlantGl.viewer" here too.
             widgetmap={1:"Visualea.PackageManager",
                        4:"Visualea.Logger"})

df2 = Layout("Visualea",
             "Dataflow Editing2",
             skeleton=sk,
             widgetmap={4:"Visualea.PackageManager",
                        3:"Visualea.Logger"})




###########################################
# Trying another sort of declaration type #
###########################################
# from openalea.visualea.mainwindow_2 import DocumentManager

# class Visualea(ExtensionBase2):
#     __layouts__ = {df1, df2}
#     __wid_factories__ = {pmanager_f, logger_f, dataflow_f}

#     def iter_layouts(self):
#         return iter(self.__layouts__)

#     def iter_widget_factories(self):
#         return iter(self.__wid_factories__)

#     def default_documents(self):






