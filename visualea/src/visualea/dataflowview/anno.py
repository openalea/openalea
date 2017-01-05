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

__license__ = "Cecill-C"
__revision__ = " $Id$ "

from Qt import QtCore, QtGui, QtWidgets

from openalea.grapheditor import qtgraphview, baselisteners
from openalea.grapheditor import qtutils
from openalea.grapheditor.qtutils import *

from openalea.visualea.graph_operator import GraphOperator
from openalea.visualea import images_rc

###############
# The toolbar #
###############
class AnnotationTextToolbar(AleaQGraphicsToolbar):
    def __init__(self, parent):
        AleaQGraphicsToolbar.__init__(self, parent)
        self.fontColorButton = AleaQGraphicsFontColorButton(self)
        self.annotationColor = AleaQGraphicsColorWheel(radius=12, parent=self)
        self.annotationColor.setVanishingEnabled(False)
        self.addItem(self.fontColorButton)
        self.addItem(self.annotationColor)
        self.refreshGeometry()
        self.setBaseOpactity(0.001)
        self.disappear()
        self.sleep()

    def set_annotation(self, anno, view=None):
        self.annotationColor.colorChanged.disconnect()
        self.fontColorButton.fontColorChanged.disconnect()
        if anno is not None:
            if view:
                pos = anno.sceneBoundingRect().topLeft()
                pos.setY(pos.y() - self.rect().height()/view.matrix().m22())
                self.setPos(pos)
            self.annotationColor.colorChanged.connect(anno._onAnnotationColorChanged)
            self.fontColorButton.fontColorChanged.connect(anno._onTextFontColorChanged)
            self.appear()
        else:
            self.disappear()


##################
# The Annotation #
##################
class GraphicalAnnotation(qtutils.MemoRects, qtgraphview.Vertex):
    """ Text annotation on the data flow """

    __def_string__ = u"click to edit"


    def __init__(self, annotation, graphadapter, parent=None):
        """ Create a nice annotation """
        qtutils.MemoRects.__init__(self, QtCore.QRectF())
        qtgraphview.Vertex.__init__(self, annotation, graphadapter)
        self.initialise(annotation.get_ad_hoc_dict())
        self.__textItem = AleaQGraphicsEmitingTextItem(self.__def_string__, self)
        self.__textItem.geometryModified.connect(self.__onTextModified)
        self.__textItem.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.setZValue(-100)
        self.__textItem.setZValue(-99)
        self.__visualStyle = 0

    annotation = baselisteners.GraphElementListenerBase.get_observed

    def initialise_from_model(self):
        rectP2 = self.get_view_data("rectP2")
        if rectP2 is not None:
            rect = QtCore.QRectF(0,0,rectP2[0],rectP2[1])
        else:
            rect = QtCore.QRectF(0,0,-1,-1)
        qtutils.MemoRects.setRect(self,rect)

        self.setHeaderRect(self.__textItem.boundingRect())

        txt = self.get_view_data("text")
        self.set_text(txt)

        txtCol = self.get_view_data("textColor")
        if txtCol:
            self.__textItem.setDefaultTextColor(QtGui.QColor(*txtCol))

        color = self.get_view_data("color")
        if color:
            color = QtGui.QColor(*color)
            self.setColor(color)

        # if an annotation has already a rectP2 field but no visualStyle,
        # it should use the new box style and
        # we should store the visualStyle in
        # the wralea (see store_view_data here below)
        vStyle = self.get_view_data("visualStyle")
        if vStyle is None:
            if rect.isValid():
                vStyle = 1 #box
            else:
                vStyle = 0 #simple
        self.store_view_data(visualStyle = vStyle)


        self.__visualStyle = vStyle
        self.__update_paint_style()

        qtgraphview.Vertex.initialise_from_model(self)

    #####################
    # ----Qt World----  #
    #####################
    itemChange = mixin_method(qtgraphview.Vertex, qtutils.MemoRects,
                              "itemChange")

    def __onTextModified(self, rect):
        self.setHeaderRect(rect)
        self.deaf(True)
        text = unicode(self.__textItem.toPlainText())
        if(text != self.__def_string__):
            self.store_view_data(text=text)
        self.deaf(False)

    def _onAnnotationColorChanged(self, color):
        self.store_view_data(color=[color.red(),
                                    color.green(),
                                    color.blue()])

    def _onTextFontColorChanged(self, color):
        self.__textItem.setDefaultTextColor(color)
        self.store_view_data(textColor=[color.red(),
                                    color.green(),
                                    color.blue()])

    def setRect(self, rect):
        self.deaf(True)
        p2 = -1, -1
        if not self.__visualStyle == 0 : #box
            p2 = rect.width(), rect.height()
        self.store_view_data(rectP2=p2)
        qtutils.MemoRects.setRect(self, rect)
        self.deaf(False)

    #########################
    # ----Other things----  #
    #########################
    def notify(self, sender, event):
        if event:
            if event[0] == "metadata_changed":
                key   = event[1]
                value = event[2]
                if value is None:
                    return
                # -- value is a string --
                if key == "text":
                    self.set_text(value)
                # -- value is a color tuple --
                elif key == "textColor":
                    if value:
                        self.__textItem.setDefaultTextColor(QtGui.QColor(*value))
                elif key == "color":
                    if value:
                        color = QtGui.QColor(*value)
                        self.setColor(color)
                # -- value is a position tuple --
                elif key == "rectP2":
                    rect = QtCore.QRectF(0,0,value[0],value[1])
                    qtutils.MemoRects.setRect(self,rect)
                    self.setHeaderRect(self.__textItem.boundingRect())
                # -- value is an int in [0, 1] --
                elif key == "visualStyle":
                    if value is None: value = 0
                    self.__visualStyle = value
                    self.__update_paint_style()
        qtgraphview.Vertex.notify(self, sender, event)

    def set_text(self, text):
        if text == u"" or text == None :
            text = self.__def_string__
        self.__textItem.setPlainText(text)

    def store_view_data(self, **kwargs):
        for k, v in kwargs.iteritems():
            self.vertex().get_ad_hoc_dict().set_metadata(k, v)

    def get_view_data(self, key):
        return self.vertex().get_ad_hoc_dict().get_metadata(key)

    def mousePressEvent(self, event):
        #let a lmb click anywhere in the header activate
        #text edition:
        if event.button()==QtCore.Qt.LeftButton and \
               self._MemoRects__headerRect.contains( event.pos() ):
            self.__textItem.setFocus()
        else:
            MemoRects.mousePressEvent(self, event)

    def contextMenuEvent(self, event):
        operator = GraphOperator(graph=self.graph(),
                                 graphScene = self.scene())
        widget = operator.get_sensible_parent()
        operator.set_annotation_item(self)

        menu = qtutils.AleaQMenu(widget)
        styleMenu = menu.addMenu("Style...")
        styleMenu.addAction(operator("Simple", styleMenu,
                                     "annotation_change_style_simple"))
        styleMenu.addAction(operator("Box", styleMenu,
                                     "annotation_change_style_box"))
        #display the menu...
        menu.move(event.screenPos())
        menu.show()
        event.accept()

    def __paint_box_style(self, painter, options, widget):
        qtutils.MemoRects.paint(self, painter, options, widget)

    def __paint_simple_style(self, painter, options, widget):
        return

    def __update_paint_style(self):
        if self.__visualStyle == 0: #simple
            self.paint = self.__paint_simple_style
            textRect = self.__textItem.boundingRect()
            self.setRect(textRect)
            self.setHeaderRect(textRect)
        elif self.__visualStyle == 1: #box
            self.paint = self.__paint_box_style
        self.update()
