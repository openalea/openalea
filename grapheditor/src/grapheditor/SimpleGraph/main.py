import sys

from PyQt4 import QtGui
from PyQt4 import QtCore
from openalea.grapheditor.qtgraphview import QtGraphView
from openalea.grapheditor.grapheditor_baselisteners import StrategyError
from custom_graph_model import Graph
import custom_graph_view


#CUSTOMISING THE GRAPH VIEW FOR THIS PARTICULAR DEMO:
def dropHandler(widget, event):
    position = widget.mapToScene(event.pos())
    position = [position.x(), position.y()]
    widget.graph().new_vertex(position)


QtGraphView.set_default_drop_handler(dropHandler)



#THE APPLICATION'S MAIN WINDOW
class MainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        """                """
        QtGui.QMainWindow.__init__(self, parent)

        self.__graph = Graph()
        self.__graphView = QtGraphView(self, self.__graph)
        self.__graphView.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setCentralWidget(self.__graphView)


#THE ENTRY POINT
def main(args):
    app = QtGui.QApplication(args)

    # Check Version
    version = QtCore.QT_VERSION_STR
    # QT_VERSION_STR implement __le__ operator
    if(version < '4.5.1'):

        mess = QtGui.QMessageBox.error(None, "Error",
                                       "Visualea need QT library >=4.5.1")
        return


    QtGui.QApplication.processEvents()
    win = MainWindow()
    win.show()
    return app.exec_()



if __name__ == "__main__":
    main(sys.argv)
