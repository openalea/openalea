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

import math

from Qt import QtCore, QtGui, QtWidgets
"""
        if style is None:
            style = self.STYLE_MEDIUM

        if style == self.STYLE_LARGE:
            button_size = QtCore.QSize(200, 100)
            icon_size = QtCore.QSize(90, 90)
        elif style == self.STYLE_MEDIUM:
            button_size = QtCore.QSize(150, 40)
            icon_size = QtCore.QSize(32, 32)
        elif style == self.STYLE_SMALL:
            button_size = QtCore.QSize(80, 30)
            icon_size = QtCore.QSize(20, 20)
        else:
            raise NotImplementedError
"""

class WelcomePage(QtWidgets.QWidget):

    """
    Create a widget page that display a list of actions as buttons
    """

    FILL_MODE_SQUARE = 'square'
    FILL_MODE_VERTICAL = 'vertical'
    FILL_MODE_HORIZONTAL = 'horizontal'

    STYLE_MEDIUM = dict(
        button_size=(150, 40),
        icon_size=(32, 32),
        stylesheet=""
    )

    STYLE_LARGE = dict(
        button_size=(200, 100),
        icon_size=(90, 90),
        stylesheet="font-size: 12pt;"
    )

    # /!\ THIS STYLE MUST CONTAIN ALL KEYS USED IN WIDGET
    _STYLE_DEFAULT = dict(
        button_size=(200, 100),
        icon_size=(90, 90),
        fill_mode=FILL_MODE_SQUARE,
        stylesheet='',
    )

    def __init__(self, actions=None, parent=None, style=None):
        QtWidgets.QWidget.__init__(self)
        self.nx = 1 # number of widget by row
        self._style_kwargs = {}
        self._style = None
        if style is None:
            style = {}
        self.set_style(**style)

        self._layout = QtWidgets.QGridLayout(self)
        self._layout.setAlignment(QtCore.Qt.AlignCenter)
        if actions is None:
            actions = []

        self.set_actions(actions)

    def set_actions(self, actions):
        self._buttons = []
        for i, action in enumerate(actions):
            button = QtWidgets.QToolButton()
            button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)

            button.setDefaultAction(action)

            self._buttons.append(button)

        self._fill_layout(self._buttons)

    def set_style(self, **kwargs):
        computed = {}
        computed.update(self._STYLE_DEFAULT)
        computed.update(self._style_kwargs)
        computed.update(kwargs)

        self._style_kwargs = computed

    def _compute_layout_info(self):
        b = len(self._buttons)
        w = self.size().width()
        h = self.size().height()

        button_size = self._style_kwargs['button_size']
        fill_mode = self._style_kwargs['fill_mode']

        bw, bh = button_size

        nx = w / bw
        ny = h / bh
        if ny == 0:
            ny = 1
        if fill_mode == self.FILL_MODE_HORIZONTAL:
            pass
        elif fill_mode == self.FILL_MODE_VERTICAL:
            nx = b / ny
            if b % ny:
                nx += 1
        elif fill_mode == self.FILL_MODE_SQUARE:
            nr = int(round(math.sqrt(b), 0))
            nx = min(nx, nr)
            if ny < nr:
                nx = b / ny
                if b % ny:
                    nx += 1

        if nx == 0:
            nx = 1

        return nx

    def _fill_layout(self, buttons):
        # compute size info
        self.nx = self._compute_layout_info()

        # clear old widgets
        for i in reversed(range(self._layout.count())):
            widget = self._layout.itemAt(i).widget()
            widget.setParent(None)
            self._layout.removeWidget(widget)

        style = self._style_kwargs

        # place new widgets
        for i, button in enumerate(buttons):
            button.setStyleSheet(style['stylesheet'])
            button.setFixedSize(QtCore.QSize(*style['button_size']))

            qsize = QtCore.QSize(*style['icon_size'])
            button.setIconSize(qsize)

            self._layout.addWidget(button, i / self.nx, i % self.nx)

    def resizeEvent(self, event):
        nx = self._compute_layout_info()
        if self.nx != nx:
            self._fill_layout(self._buttons)
