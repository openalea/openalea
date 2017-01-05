# -*- coding: utf-8 -*-
# -*- python -*-
#
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2014 INRIA - CIRAD - INRA
#
#       File author(s):
#            Julien Diener <julien.diener@inria.fr>
#            Guillaume Baty <guillaume.baty@inria.fr>
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

from Qt import QtWidgets, QtGui, QtCore

import matplotlib

from matplotlib import pyplot

from matplotlib.backends import backend_qt4agg
from matplotlib.backends import backend_qt4

from matplotlib.backend_bases import FigureManagerBase
from matplotlib._pylab_helpers import Gcf

try:
    import matplotlib.backends.qt4_editor.figureoptions as figureoptions
except ImportError:
    figureoptions = None

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure

from matplotlib import _pylab_helpers

all_widgets = []


class MplFigure(Figure):
    pass


class MplCanvas(FigureCanvasQTAgg):

    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None):
        fig = MplFigure()
        FigureCanvasQTAgg.__init__(self, fig)
#         self.figure.add_axobserver(self._on_axes_changed)
#
#     def _on_axes_changed(self, *args):
#         self.draw()
#         self.draw_idle()


class FigureManagerQT(FigureManagerBase):

    """
    Public attributes

    canvas      : The FigureCanvas instance
    num         : The Figure number
    toolbar     : The qt.QToolBar
    window      : The qt.QMainWindow
    """

    def __getattribute__(self, *args, **kwargs):
        return FigureManagerBase.__getattribute__(self, *args, **kwargs)

    def __init__(self, canvas, num):
        FigureManagerBase.__init__(self, canvas, num)
        self.canvas = canvas
        self.canvas.setFocusPolicy(QtCore.Qt.StrongFocus)

    def show(self):
        print 'pylab.plot'


class MplFigureWidget(QtWidgets.QFrame):

    count = 0

    def __init__(self):
        QtWidgets.QFrame.__init__(self)

        c = self.palette().color(self.backgroundRole())
        self._default_color = str((c.red(), c.green(), c.blue()))

        self.canvas = MplCanvas()
        self.manager = FigureManagerQT(self.canvas, MplFigureWidget.count)
        self.mpl_toolbar = NavigationToolbar2QT(self.canvas, None)
        self.mpl_toolbar.setStyleSheet("background-color: rgb%s;" % self._default_color)
        self.mpl_toolbar.hide()

        MplFigureWidget.count += 1
        all_widgets.append(self)

        self.setToolTip("Figure %d" % self.manager.num)

        self.setFrameShape(QtWidgets.QFrame.Box)
        self.setFrameShadow(QtWidgets.QFrame.Plain)
        self.setContentsMargins(1, 1, 1, 1)

        self._layout = QtWidgets.QVBoxLayout(self)
        self._layout.addWidget(self.canvas)
        self._layout.setContentsMargins(1, 1, 1, 1)

    def initialize(self):
        self.activate()

    def toolbar_actions(self):
        return [['', '', action, 0] for action in self.mpl_toolbar.actions()]

    def show_active(self):
        self.setFrameShape(QtWidgets.QFrame.Box)
        self.setStyleSheet("background-color: rgb(0, 150, 0);")

    def show_inactive(self):
        self.setStyleSheet("")
        self.setFrameShape(QtWidgets.QFrame.NoFrame)

    def hold(self, state=True):
        for axe in self.canvas.figure.axes:
            axe.hold(state)

    def set_num(self, num):
        if num == self.manager.num:
            return
        else:
            self.manager.num = num
            Gcf.figs[num] = self.manager
            self.setToolTip("Figure %d" % self.manager.num)

    def properties(self):
        return dict(num=self.manager.num)

    def set_properties(self, properties):
        get = properties.get
        num = get('num', None)
        if num is not None:
            self.set_num(num)

    def activate(self):
        def make_active(event):
            for widget in all_widgets:
                if widget.manager is self.manager:
                    _pylab_helpers.Gcf.set_active(self.manager)
                    widget.show_active()
                else:
                    widget.show_inactive()

        pyplot.ion()

        cid = self.manager.canvas.mpl_connect('button_press_event', make_active)
        self.manager._cidgcf = cid

        _pylab_helpers.Gcf.set_active(self.manager)


def new_figure_manager_given_figure(num, figure):
    """
    Create a new figure manager instance for the given figure.
    """
    canvas = MplCanvas(figure)
    return FigureManagerQT(canvas, num)


def draw_if_interactive():
    """
    Is called after every pylab drawing command
    """
    # if matplotlib.is_interactive():
    figManager = Gcf.get_active()
    if figManager is not None:
        figManager.canvas.draw_idle()


def activate():
    pyplot.switch_backend('qt4agg')
    backend_qt4.draw_if_interactive = draw_if_interactive
    backend_qt4agg.draw_if_interactive = draw_if_interactive

    backend_qt4.new_figure_manager_given_figure = new_figure_manager_given_figure
    backend_qt4agg.new_figure_manager_given_figure = new_figure_manager_given_figure

    backend_qt4agg.show = lambda: None

activate()
