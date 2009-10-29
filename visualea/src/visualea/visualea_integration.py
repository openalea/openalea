# -*- python -*-
#
#       OpenAlea.Visualea: OpenAlea graphical user interface
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA
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

from PyQt4 import QtCore, QtGui
from openalea.core.pkgmanager import PackageManager
from openalea.core.node import RecursionError
from openalea.grapheditor import qtgraphview
import weakref,sys

from openalea.visualea.util import open_dialog

#Drag and drop handlers
def OpenAleaNodeFactoryHandler(view, event):
    """ Drag and Drop from the PackageManager """
    if (event.mimeData().hasFormat("openalea/nodefactory")):
        pieceData = event.mimeData().data("openalea/nodefactory")
        dataStream = QtCore.QDataStream(pieceData, QtCore.QIODevice.ReadOnly)
        
        package_id = QtCore.QString()
        factory_id = QtCore.QString()
        
        dataStream >> package_id >> factory_id
        
        # Add new node
        pkgmanager = PackageManager()
        pkg = pkgmanager[str(package_id)]
        factory = pkg.get_factory(str(factory_id))
        
        position = view.mapToScene(event.pos())
        try:
            node = factory.instantiate([view.observed().factory.get_id()])
            view.graph.add_vertex(node, position=[position.x(), position.y()])
        except RecursionError:
            mess = QtGui.QMessageBox.warning(view, "Error",
                                             "A graph cannot be contained in itself.")
            return
        
        event.setDropAction(QtCore.Qt.MoveAction)
        event.accept()


def OpenAleaNodeDataPoolHandler(view, event):
    # Drag and Drop from the DataPool
    if(event.mimeData().hasFormat("openalea/data_instance")):
        pieceData = event.mimeData().data("openalea/data_instance")
        dataStream = QtCore.QDataStream(pieceData, QtCore.QIODevice.ReadOnly)

        data_key = QtCore.QString()

        dataStream >> data_key
        data_key = str(data_key)

        # Add new node
        pkgmanager = PackageManager()
        pkg = pkgmanager["system"]
        factory = pkg.get_factory("pool reader")

        position = view.mapToScene(event.pos())

        # Set key val
        try:
            node = factory.instantiate([view.observed().factory.get_id()])
            view.graph.add_vertex(node, [position.x(), position.y()])
        except RecursionError:
            mess = QtGui.QMessageBox.warning(view, "Error",
                                             "A graph cannot be contained in itself.")
            return

        node.set_input(0, data_key)
        node.set_caption("pool ['%s']"%(data_key,))

        event.setDropAction(QtCore.Qt.MoveAction)
        event.accept()


mimeFormats = ["openalea/nodefactory", "openalea/data_instance"]
mimeDropHandlers = [OpenAleaNodeFactoryHandler, OpenAleaNodeDataPoolHandler]
def get_drop_mime_handlers():
    return dict(zip(mimeFormats, mimeDropHandlers))

qtgraphview.QtGraphView.set_mime_handler_map(get_drop_mime_handlers())


#configuring event handlers

def vertexMouseDoubleClickEvent(widget, event):
    # Read settings
    try:
        localsettings = Settings()
        str = localsettings.get("UI", "DoubleClick")
    except:
        str = "['open']"

    if('open' in str):
        if(widget._vertexWidget):
            if(widget.isVisible()):
                widget.raise_ ()
                widget.activateWindow ()
            else:
                widget.show()
            return
            
        factory = widget.vertex().get_factory()
        if(not factory) : return
        # Create the dialog. 
        # NOTE: WE REQUEST THE MODEL TO CREATE THE DIALOG
        # THIS IS NOT DESIRED BECAUSE IT COUPLES THE MODEL
        # TO THE UI.
        innerWidget = factory.instantiate_widget(widget.vertex(), None)

        if(not innerWidget) : return 
        if (innerWidget.is_empty()):
            innerWidget.close()
            del innerWidget
            return

        widget._vertexWidget = open_dialog(None, innerWidget, factory.get_id(), False)


    if('run' in str):
        widget.graph.graph().eval_as_expression(widget.vertex().get_id())

qtgraphview.QtGraphViewVertex.set_event_handler("mouseDoubleClickEvent", 
                                                vertexMouseDoubleClickEvent)
