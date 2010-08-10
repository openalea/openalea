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

from PyQt4 import QtGui, QtCore, QtSvg
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
        self.fontButton = AleaQGraphicsFontButton(self)
        self.fontColorButton = AleaQGraphicsFontColorButton(self)
        self.colorWheel = AleaQGraphicsColorWheel(radius=12, parent=self)
        self.colorWheel.setVanishingEnabled(False)
        self.addItem(self.fontButton)
        self.addItem(self.fontColorButton)
        self.addItem(self.colorWheel)
        self.refreshGeometry()
        self.setBaseOpactity(0.001)

    def set_annotation(self, anno):
        self.colorWheel.colorChanged.disconnect()
        self.fontButton.fontChanged.disconnect()
        self.fontColorButton.fontColorChanged.disconnect()
        if anno is not None:
            self.colorWheel.colorChanged.connect(anno._onColorWheelChanged)
            self.fontButton.fontChanged.connect(anno._onTextFontChanged)
            self.fontColorButton.fontColorChanged.connect(anno._onTextFontColorChanged)


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
        self.__textItem = AleaQGraphicsEmitingTextItem(self.__def_string__, self)
        self.__textItem.geometryModified.connect(self.__onTextModified)
        self.__textItem.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.setZValue(-100)
        self.__textItem.setZValue(-99)

    annotation = baselisteners.GraphElementListenerBase.get_observed

    def initialise_from_model(self):
        rectP2 = self.get_view_data("rectP2")
        rect = QtCore.QRectF(0,0,rectP2[0],rectP2[1])
        qtutils.MemoRects.setRect(self,rect)
        self.setHeaderRect(self.__textItem.boundingRect())

        txt = self.get_view_data("htmlText")
        if txt:
            self.set_text(txt, html=True)
        else:
            txt = self.get_view_data("text")
            self.set_text(txt)

        color = self.get_view_data("color")
        if color:
            color = QtGui.QColor(*color)
            self.setColor(color)

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
        htmlText=unicode(self.__textItem.toHtml())
        if(text != self.__def_string__):
            self.store_view_data(text=text)
            self.store_view_data(htmlText=htmlText)
        self.deaf(False)

    def _onColorWheelChanged(self, color):
        self.store_view_data(color=[color.red(),
                                    color.green(),
                                    color.blue()])

    def _onTextFontChanged(self, font):
        cursor = self.__textItem.textCursor()
        fmt = cursor.charFormat()
        fmt.setFont(font)
        cursor.mergeCharFormat(fmt)

    def _onTextFontColorChanged(self, color):
        cursor = self.__textItem.textCursor()
        fmt = cursor.charFormat()
        brush = fmt.foreground()
        brush.setColor(color)
        fmt.setForeground(QtGui.QBrush(color))
        cursor.mergeCharFormat(fmt)
        self.update()

    def setRect(self, rect):
        self.deaf(True)
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
                if event[1] == "text" and not self.htmlHasBeenSet:
                    self.set_text(event[2])
                    return
                elif event[1] == "htmlText":
                    text = event[2]
                    if text is not None:
                        self.set_text(text, html=True)
                        self.htmlHasBeenSet = True
                elif event[1] == "rectP2":
                    rect = QtCore.QRectF(0,0,event[2][0],event[2][1])
                    qtutils.MemoRects.setRect(self,rect)
                    self.setHeaderRect(self.__textItem.boundingRect())
                elif event[1] == "color":
                    col = event[2]
                    if col:
                        color = QtGui.QColor(*col)
                        self.setColor(color)
        qtgraphview.Vertex.notify(self, sender, event)

    def set_text(self, text, html=False):
        if text == u"" or text == None :
            text = self.__def_string__
        if not html:
            self.__textItem.setPlainText(text)
        else:
            self.__textItem.setHtml(text)

    def store_view_data(self, **kwargs):
        for k, v in kwargs.iteritems():
            self.vertex().get_ad_hoc_dict().set_metadata(k, v)

    def get_view_data(self, key):
        return self.vertex().get_ad_hoc_dict().get_metadata(key)
