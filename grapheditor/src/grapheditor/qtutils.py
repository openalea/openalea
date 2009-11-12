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

    ############
    # QT WORLD #
    ############
    def paint(self, painter, paintOptions, widget):
    	"""Overrides the painting of a QGraphicsProxyWidget.
	
	:Parameters:
	 - painter (QtGui.QPainter) - The painter to paint with
	 - paintOptions (QtGui.QStyleOptionsGraphicsItem) - Info one can use
	   to do the painting
	 - widget (QtGui.QWidget) - The widget being painted on.

        """
        #NEEDED TO OVERLOAD THIS TO GET RID OF THE UGLY BACKGROUND
        #AROUND THE WIDGET.
        self.widget().render(painter, QtCore.QPoint(), QtGui.QRegion(), 
                             QtGui.QWidget.RenderFlags()|QtGui.QWidget.DrawChildren)
