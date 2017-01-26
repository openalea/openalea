# -*- python -*-
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#        http://qt.developpez.com/doc/4.7/widgets-codeeditor/
#
#       Copyright 2013 INRIA - CIRAD - INRA
#
#       File author(s): Julien Coste <julien.coste@inria.fr>
#
#       File contributor(s):
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

__revision__ = ""

from Qt import QtCore, QtGui, QtWidgets

class Margin(QtWidgets.QWidget):
    # Come from LPy

    def __init__(self, parent, editor):
        QtWidgets.QWidget.__init__(self, parent)
        self.editor = editor
        self.showLines = True

    def paintEvent(self, paintEvent):
        if self.showLines:
            maxheight = self.editor.viewport().height()
            maxline = self.editor.document().blockCount()
            painter = QtGui.QPainter(self)
            painter.setPen(QtGui.QPen(QtGui.QColor(100, 100, 100)))
            h = 0
            line = -1
            while h < maxheight and line < maxline:
                cursor = self.editor.cursorForPosition(QtCore.QPoint(1, h))
                nline = cursor.blockNumber() + 1
                rect = self.editor.cursorRect(cursor)
                if nline > line:
                    line = nline
                    painter.drawText(0, rect.top() + 2, 40, rect.height() + 2,
                                     QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop, str(line))
                h = rect.top() + rect.height() + 1
            painter.end()

    def mousePressEvent(self, event):
        line = self.editor.cursorForPosition(event.pos()).blockNumber()
        self.lineClicked[int].emit(line + 1)
