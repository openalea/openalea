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

class AleaQGraphicsProxyWidget(QtGui.QGraphicsProxyWidget):
    def __init__(self, widget, parent=None):
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
        #NEEDED TO OVERLOAD THIS TO GET RID OF THE UGLY BACKGROUND
        #AROUND THE WIDGET.
        self.widget().render(painter, QtCore.QPoint(), QtGui.QRegion(), 
                             QtGui.QWidget.RenderFlags()|QtGui.QWidget.DrawChildren)
