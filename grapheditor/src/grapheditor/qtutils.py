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


from PyQt4 import QtCore, QtGui

class AleaQGraphicsProxyWidget(QtGui.QGraphicsProxyWidget):
    """Embed a QWidget in a QGraphicsItem without the ugly background.

    When embedding for ex. a QLabel in a QGraphicsLayout using the normal
    QGraphicsProxyWidget, the QLabel is rendered with its ugly background
    and the custom drawing of the QGraphicsItem is hidden.
    This class overrides the painting routine or the QGraphicsProxyWidget
    to paint the child widget without the background.
    """
    def __init__(self, widget, parent=None):
        """
        Ctor.

        :Parameters:
	 - widget (QtGui.QWidget) - The QWidget to embed
	 - parent (QtGui.QGraphicsItem) - Reference to the parent.

        """
        QtGui.QGraphicsProxyWidget.__init__(self, parent)
        dummy=QtGui.QWidget()
        dummy.setContentsMargins(0,0,0,0)
        layout=QtGui.QGridLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(widget,0,0,
                         QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        dummy.setLayout(layout)
        self.setWidget(dummy)

        
    def setWidget(self, widget):
        widget.setBackgroundRole(QtGui.QPalette.Background)
        widget.setAutoFillBackground(True)
        widget.setStyleSheet("background-color: transparent")
        QtGui.QGraphicsProxyWidget.setWidget(self, widget)

    ############
    # QT WORLD #
    ############
    # def paint(self, painter, paintOptions, widget):
    # 	"""Overrides the painting of a QGraphicsProxyWidget.
	
    #     :Parameters:
    #      - painter (QtGui.QPainter) - The painter to paint with
    #      - paintOptions (QtGui.QStyleOptionsGraphicsItem) - Info one can use
    #        to do the painting
    #      - widget (QtGui.QWidget) - The widget being painted on.

    #     """
    #     #NEEDED TO OVERLOAD THIS TO GET RID OF THE UGLY BACKGROUND
    #     #AROUND THE WIDGET.
    #     self.widget().render(painter, QtCore.QPoint(), QtGui.QRegion(), 
    #                          QtGui.QWidget.RenderFlags()|QtGui.QWidget.DrawChildren)



def mixin_method(mixinOne, mixinTwo, methodname, firstWins = False, invert=False, caller=None):
    """A function that returns a method calling method \"methodname\"
    from mixinOne and then from mixinTwo, or the reverse order
    if invert is True.
    Can be used to quickly reimplement simple overloads.
    """

    first =  None
    second = None

    if(not invert):
        first = None if (mixinOne is None) else getattr(mixinOne, methodname, None)
        second = None if (mixinTwo is None) else getattr(mixinTwo, methodname, None)
    else:
        second = None if (mixinOne is None) else getattr(mixinOne, methodname, None)
        first = None if (mixinTwo is None) else getattr(mixinTwo, methodname, None)

    def simple_call(self, *args, **kwargs):
        return first(self, *args, **kwargs)

    def mixin_call(self, *args, **kwargs):
        v1 = first(self, *args, **kwargs)
        v2 = second(self, *args, **kwargs)
        if(firstWins): return v1
        else: return v2

    if(second and first is None):
        first = second
        second = None

    if(first and second is None):
        return simple_call
    else:
        return mixin_call


def extend_qt_scene_event(qtcls):
    def event_handler(self, event):
        t = event.type()
        if t == QtCore.QEvent.GraphicsSceneMouseMove:
            self.moveEvent(event)
        elif t == QtCore.QEvent.Show:
            self.polishEvent()
        return qtcls.sceneEvent(self, event)

    return event_handler
