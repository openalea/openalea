# Version: $Id$
#
#

# Commentary:
#
#

# Change Log:
#
#

# Code:

import sys

from Qt import QtGui, QtWidgets

from openalea.grapheditor import qt

from custom_graph_model import Graph

class SimpleView( qt.View ):
    def __init__(self, *args, **kwargs):
        qt.View.__init__(self, *args, **kwargs)
        self.set_default_drop_handler(self.dropHandler)

    def dropHandler(self, event):
        position = self.mapToScene(event.pos())
        position = [position.x(), position.y()]
        self.scene().new_vertex(position=position)

    mouseDoubleClickEvent = dropHandler

class SimpleVertex(qt.DefaultGraphicalVertex):
    def __init__(self, *args, **kwargs):
        qt.DefaultGraphicalVertex.__init__(self, *args, **kwargs)
        self.initialise(self.get_observed().get_ad_hoc_dict())
    def get_view_data(self, key):
        return self.get_observed().get_ad_hoc_dict().get_metadata(key)

SimpleGraph = qt.QtGraphStrategyMaker( graphView            = SimpleView,
                                       vertexWidgetMap      = {"vertex":SimpleVertex},
                                       edgeWidgetMap        = {"default":qt.DefaultGraphicalEdge,
                                                               "floating-default":qt.DefaultGraphicalFloatingEdge},
                                       graphViewInitialiser = None,
                                       adapterType          = None )

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        """                """
        QtWidgets.QMainWindow.__init__(self, parent)
        self.__graph = Graph()
        self.__graphView = SimpleGraph.create_view(self.__graph, parent=self)
        self.setCentralWidget(self.__graphView)

def main(args):
    app = QtWidgets.QApplication(args)
    QtWidgets.QApplication.processEvents()
    win = MainWindow()
    win.show()
    return app.exec_()

if __name__ == "__main__":
    main(sys.argv)

#
# main.py ends here
