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

import weakref,sys
from PyQt4 import QtCore, QtGui
from openalea.core import observer
from openalea.grapheditor import qtutils
from openalea.grapheditor import qtgraphview


"""

"""

class GraphicalVertex(QtGui.QGraphicsWidget, qtgraphview.QtGraphViewVertex):

    #color of the small box that indicates evaluation
    eval_color = QtGui.QColor(255, 0, 0, 200)

    def __init__(self, vertex, graphadapter, parent=None):
        QtGui.QGraphicsWidget.__init__(self, parent)
        qtgraphview.QtGraphViewVertex.__init__(self, vertex, graphadapter)

        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
        self.setZValue(1)

        # ---Small box when the vertex is being evaluated---
        self.modified_item = QtGui.QGraphicsRectItem(5,5,7,7, self)
        self.modified_item.setBrush(self.eval_color)
        self.modified_item.setAcceptedMouseButtons(QtCore.Qt.NoButton)
        self.modified_item.setVisible(False)

        # ---Sub items layout---
        layout = QtGui.QGraphicsLinearLayout()
        layout.setOrientation(QtCore.Qt.Vertical)
        layout.setSpacing(2)

        self._inPortLayout  = QtGui.QGraphicsLinearLayout()
        self._outPortLayout = QtGui.QGraphicsLinearLayout()
        self._caption            = QtGui.QLabel(vertex.internal_data["caption"])
        captionProxy             = qtutils.AleaQGraphicsProxyWidget(self._caption)

        layout.addItem(self._inPortLayout)
        layout.addItem(captionProxy)
        layout.addItem(self._outPortLayout)

        layout.setAlignment(self._inPortLayout, QtCore.Qt.AlignHCenter)
        layout.setAlignment(self._outPortLayout, QtCore.Qt.AlignHCenter)
        layout.setAlignment(captionProxy, QtCore.Qt.AlignHCenter)
        self._inPortLayout.setSpacing(8)
        self._outPortLayout.setSpacing(8)

        self.setLayout(layout)

        # ---reference to the widget of this vertex---
        self._vertexWidget = None

        #hack around a Qt4.4 limitation
        self.__inPorts=[]
        self.__outPorts=[]
        #do the port layout
        self.__layout_ports()
        #tooltip
        self.set_tooltip(vertex.__doc__)
        self.initialise_from_model()


    #################
    # private stuff #
    #################
    def __layout_ports(self):
        """ Add ports """
        self.nb_cin = 0
        for desc in self.graph.get_vertex_inputs(self.vertex().get_id()):
            self.__add_in_connection(desc)

        for desc in self.graph.get_vertex_outputs(self.vertex().get_id()):
            self.__add_out_connection(desc)

    def __update_ports_ad_hoc_position(self):
        """the canvas position held in the adhoc dict of the ports has to be changed
        from here since the port items, being childs, don't receive moveEvents..."""
        [port.update_canvas_position() for port in self.__inPorts+self.__outPorts]        
        
    def __add_in_connection(self, port):
        graphicalConn = GraphicalPort(self, port)
        self._inPortLayout.addItem(graphicalConn)
        self.__inPorts.append(graphicalConn)

    def __add_out_connection(self, port):
        graphicalConn = GraphicalPort(self, port)
        self._outPortLayout.addItem(graphicalConn)
        self.__outPorts.append(graphicalConn)


    ####################
    # Observer methods #
    ####################
    def notify(self, sender, event): 
        """ Notification sent by the vertex associated to the item """
        if(event and event[0] == "start_eval"):
            self.modified_item.setVisible(self.isVisible())
            self.modified_item.update()
            self.update()
            QtGui.QApplication.processEvents()

        elif(event and event[0] == "stop_eval"):
            self.modified_item.setVisible(False)
            self.modified_item.update()
            self.update()
            QtGui.QApplication.processEvents()

        elif(event and event[0] == "caption_modified"):
            self.set_caption(event[1])

        elif(event and event[0] == "MetaDataChanged" and event[1]=="user_color"):
            self.update()

        qtgraphview.QtGraphViewVertex.notify(self, sender, event)

    def set_tooltip(self, doc=None):
        """ Sets the tooltip displayed by the vertex item. Doesn't change
        the data."""
        try:
            vertex_name = self.vertex().factory.name
        except:
            vertex_name = self.vertex().__class__.__name__

        try:
            pkg_name = self.vertex().factory.package.get_id()
        except:
            pkg_name = ''

        if doc:
            doc = doc.split('\n')
            doc = [x.strip() for x in doc] 
            doc = '\n'.join(doc)
        else:
            if(self.vertex().factory):
                doc = self.vertex().factory.description
        
        # here, we could process the doc so that the output is nicer 
        # e.g., doc.replace(":params","Parameters ") and so on

        mydoc = doc

        for name in [':Parameters:', ':Returns:', ':Keywords:']:
            mydoc = mydoc.replace(name, '<b>'+name.replace(':','') + '</b><br/>\n')

        self.setToolTip( "<b>Name</b> : %s <br/>\n" % (vertex_name) +
                         "<b>Package</b> : %s<br/>\n" % (pkg_name) +
                         "<b>Documentation :</b> <br/>\n%s" % (mydoc,))

    def set_caption(self, caption):
        """Sets the name displayed in the vertex widget, doesn't change
        the vertex data"""
        self._caption.setText(caption)
        self.layout().updateGeometry()

    ###############################
    # ----Qt World overloads----  #
    ###############################
    def select_drawing_strategy(self, state):
        if self.vertex().get_ad_hoc_dict().get_metadata("use_user_color"):
            return qtgraphview.QtGraphViewVertex.select_drawing_strategy(self, "use_user_color")
        else:
            return qtgraphview.QtGraphViewVertex.select_drawing_strategy(self, state)

    def polishEvent(self):
        self.__update_ports_ad_hoc_position()
        qtgraphview.QtGraphViewVertex.polishEvent(self)
        QtGui.QGraphicsWidget.polishEvent(self)

    def moveEvent(self, event):
        self.__update_ports_ad_hoc_position()
        qtgraphview.QtGraphViewVertex.moveEvent(self, event)
        QtGui.QGraphicsWidget.moveEvent(self, event)

    def mousePressEvent(self, event):
        """Overloaded or else edges are created from the vertex
        not from the ports"""
        QtGui.QGraphicsWidget.mousePressEvent(self, event)




class GraphicalPort(QtGui.QGraphicsWidget, observer.AbstractListener):
    """ A vertex port """
    WIDTH =  10
    HEIGHT = 10

    __size = QtCore.QSizeF(WIDTH, 
                           HEIGHT)

    def __init__(self, parent, port):
        """
        """
        QtGui.QGraphicsWidget.__init__(self, parent)
        self.initialise(port)
        self.observed = weakref.ref(port)
        try:
            port.get_ad_hoc_dict().add_metadata("canvasPosition", list)
        except:
            pass
        port.get_ad_hoc_dict().set_metadata("canvasPosition", [0,0])
        port.get_ad_hoc_dict().simulate_full_data_change()

    def port(self):
            return self.observed()

    def notify(self, sender, event):
        if(event[0]=="MetaDataChanged"):
            if(event[1]=="hide"):
                if event[2]:
                    self.setVisible(False)
                else:
                    self.setVisible(True)

    def canvas_position(self):
        pos = self.rect().center() + self.scenePos()
        return[pos.x(), pos.y()]
        
    def update_canvas_position(self):
        self.port().get_ad_hoc_dict().set_metadata("canvasPosition", 
                                                   self.canvas_position())
        

    ##################
    # QtWorld-Layout #
    ##################
    def size(self):
        return self.__size

    def sizeHint(self, blop, blip):
        return self.size()

    def minimumSizeHint(self):
        return self.size()

    def sizePolicy(self):
        return QtGui.QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    ##################
    # QtWorld-Events #
    ##################
    def moveEvent(self, event):
        self.update_canvas_position()
        QtGui.QGraphicsWidget.moveEvent(self, event)

    def mousePressEvent(self, event):
        graphview = self.scene().views()[0]
        if (graphview and event.buttons() & QtCore.Qt.LeftButton):
            graphview.new_edge_start(self.canvas_position())
            return

    def paint(self, painter, option, widget):
        size = self.size()
        
        painter.setBackgroundMode(QtCore.Qt.TransparentMode)
        gradient = QtGui.QLinearGradient(0, 0, 10, 0)
        gradient.setColorAt(1, QtGui.QColor(QtCore.Qt.yellow).light(120))
        gradient.setColorAt(0, QtGui.QColor(QtCore.Qt.darkYellow).light(120))
        painter.setBrush(QtGui.QBrush(gradient))
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 0))

        painter.drawEllipse(1,1,size.width()-2,size.height()-2)

