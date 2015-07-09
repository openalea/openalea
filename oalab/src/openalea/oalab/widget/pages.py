# -*- python -*-
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2013 INRIA - CIRAD - INRA
#
#       File author(s): Julien Coste <julien.coste@inria.fr>
#                       Guillaume Baty <guillaume.baty@inria.fr>
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

__all__ = ['WelcomePage']

from openalea.vpltk.qt import QtCore, QtGui

class WelcomePage(QtGui.QWidget):

    """
    Create a widget page that display a list of actions as buttons
    """
    button_size = QtCore.QSize(200, 100)
    icon_size = QtCore.QSize(80, 80)
    stylesheet = "font-size: 12pt;"

    def __init__(self, actions=None, parent=None):
        QtGui.QWidget.__init__(self)
        self._layout = QtGui.QGridLayout(self)
        self._layout.setAlignment(QtCore.Qt.AlignCenter)
        if actions:
            self.set_actions(actions)

    def set_actions(self, actions):
        for i in reversed(range(self._layout.count())):
            widget = self._layout.itemAt(i).widget()
            widget.setParent(None)
            self._layout.removeWidget(widget)

        w = self.size().width()

        nx = w / self.button_size.width()
        if nx == 0:
            nx = 1

        for i, action in enumerate(actions):
            button = QtGui.QToolButton()
            button.setFixedSize(self.button_size)
            # button.setStyleSheet(self.stylesheet)
            button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)

            qsize = QtCore.QSize(self.icon_size)
            button.setDefaultAction(action)
            button.setIconSize(qsize)

            self._layout.addWidget(button, i / nx, i % nx)


