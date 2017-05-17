# -*- coding: utf-8 -*-
# -*- python -*-
#
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2014-2017 INRIA - CIRAD - INRA
#
#       File author(s):
#            Guillaume Cerutti <guillaume.cerutti@inria.fr>
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

from openalea.vpltk.qt import QtGui, QtCore
from openalea.oalab.utils import qicon

from openalea.core.observer import Observed

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
from matplotlib.backends.backend_qt4 import _getSaveFileName
from matplotlib.figure import Figure

from matplotlib import _pylab_helpers

import os


all_widgets = {}
figure_containers = []

class MplFigure(Figure, Observed):
    def __init__(self):
        Figure.__init__(self)
        Observed.__init__(self)
        
    def connect(self):
        self.canvas.mpl_connect('pick_event', self.onpick)

    def notify_listeners(self, event=None):
        super(MplFigure, self).notify_listeners(event)

    def onpick(self,event):
        artist = event.artist

        ind = event.ind

        if isinstance(artist,matplotlib.collections.PathCollection):
            paths = [artist.get_offsets()[i] for i in event.ind]
            axes = artist.get_axes()
            self.notify_listeners(('data_point_picked', (self, axes, artist.get_offsets()[ind[0]])))


class MplCanvas(FigureCanvasQTAgg):

    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None):
        fig = MplFigure()
        FigureCanvasQTAgg.__init__(self, fig)
        fig.connect()
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


class MplFigureTabWidget(QtGui.QFrame, Observed):
    tabCreated = QtCore.Signal(bool)
    
    def __init__(self, canvas, num=None):
        QtGui.QFrame.__init__(self)

        c = self.palette().color(self.backgroundRole())
        self._default_color = str((c.red(), c.green(), c.blue()))

        num = 0 if num is None else num

        self.canvas = MplCanvas()
        self.manager = FigureManagerQT(self.canvas, num)

        # self.mpl_toolbar = NavigationToolbar2QT(self.canvas, None)
        # self.mpl_toolbar.setStyleSheet("background-color: rgb%s;" % self._default_color)
        # self.mpl_toolbar.hide()
        # self.canvas.mpl_connect('button_press_event', self.onclick)
        # self.canvas.mpl_connect('pick_event', self.onpick)

        Gcf.figs[num] = self.manager
        all_widgets[num] = self

        self.setToolTip("Figure %d" % self.manager.num)

        self.setFrameShape(QtGui.QFrame.Box)
        self.setFrameShadow(QtGui.QFrame.Plain)
        self.setContentsMargins(1, 1, 1, 1)

        self._layout = QtGui.QVBoxLayout(self)
        self._layout.addWidget(self.canvas)
        self._layout.setContentsMargins(1, 1, 1, 1)


    # def onclick(self,event):
    #     print('button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
    #           (event.button, event.x, event.y, event.xdata, event.ydata))

    # def onpick(self,event):
    #     artist = event.artist

    #     ind = event.ind
    #     print 'Pick :',artist, ind

    #     if isinstance(artist,matplotlib.collections.PathCollection):
    #         paths = [artist.get_offsets()[i] for i in event.ind]
    #         print paths
            
    #         self.notify_listeners(('data_point_picked', (self, artist.get_offsets()[ind[0]])))



    def show_active(self):
        self.setFrameShape(QtGui.QFrame.Box)
        self.setStyleSheet("background-color: rgb(0, 150, 0);")

    def show_inactive(self):
        self.setStyleSheet("")
        self.setFrameShape(QtGui.QFrame.NoFrame)

    def hold(self, state=True):
        for axe in self.canvas.figure.axes:
            axe.hold(state)

    # def toolbar_actions(self):
        # return [['', '', action, 0] for action in self.mpl_toolbar.actions()]


class MplTabContainerWidget(QtGui.QWidget):

    def __init__(self, parent=None):
        
        QtGui.QWidget.__init__(self, parent=parent)

        c = self.palette().color(self.backgroundRole())
        self._default_color = str((c.red(), c.green(), c.blue()))

        self.tabs = QtGui.QTabWidget()        

        self._layout = QtGui.QVBoxLayout(self)
        self._layout.addWidget(self.tabs)

        # self.mpl_toolbar = NavigationToolbar2QT(MplCanvas(), None)
        # self.mpl_toolbar.setStyleSheet("background-color: rgb%s;" % self._default_color)

        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.tab_closed)
        self.tabs.currentChanged.connect(self.activate_figure)

        self._tab_toolbars = {}

        self.tabs.setFocusPolicy(QtCore.Qt.StrongFocus) 
        self._create_actions()
        self._create_connections()

        # add_drop_callback(self, 'pandas/dataframe', self.drop_dataframe)

    def _create_actions(self):
        self.action_save_figure = QtGui.QAction(qicon("matplotlib_filesave.png"), 'Save Figure', self)
        self.action_clear_figure = QtGui.QAction(qicon("matplotlib_clf.png"), 'Clear Figure', self)
        # self.action_zoom_in = QtGui.QAction(qicon("matplotlib_zoom_in.png"), 'Zoom In', self)

    def _create_connections(self):
        self.action_save_figure.triggered.connect(self.save_figure)
        self.action_clear_figure.triggered.connect(self.clear_figure)
        # self.action_zoom_in.triggered.connect(self.zoom_in)

    def refresh_tab_widgets(self):
        for num in all_widgets.keys():
            widget = all_widgets[num]
            figure_label = widget.canvas.figure.get_label()

            if len(figure_label) == 0:
                figure_label = "Figure "+str(num)
            else:
                figure_label += " ["+str(num)+"]"
            widget.setToolTip(figure_label)
            tab_num = self.tabs.addTab(widget, figure_label)
            # self._tab_toolbars[tab_num] = NavigationToolbar2QT(widget.canvas,None)
        self.tabs.setCurrentIndex(tab_num)


    def tab_closed(self, tab_index):
        widget = self.tabs.widget(tab_index)
        num = widget.manager.num
        self.tabs.removeTab(tab_index)
        del Gcf.figs[num]
        del widget.manager
        del widget.canvas
        del all_widgets[num]

    def activate_figure(self, tab_index):
        widget = self.tabs.widget(tab_index)

        # self.mpl_toolbar = NavigationToolbar2QT(widget.canvas, None)
        # widget.canvas.draw()

        # cid = widget.manager.canvas.mpl_connect('button_press_event', make_active)
        # widget.manager._cidgcf = cid
        # _pylab_helpers.Gcf.set_active(widget.manager)

    def initialize(self):
        figure_containers.append(self)


    def toolbars(self):
        toolbar = QtGui.QToolBar("Matplotlib Figures")
        toolbar.addActions([self.action_save_figure])
        toolbar.addActions([self.action_clear_figure])
        # toolbar.addActions([self.action_zoom_in])
        return [toolbar]


    def global_toolbar_actions(self):
        return []

    def toolbar_actions(self):
        return [self.action_save_figure, self.action_clear_figure]


    def save_figure(self):
        widget = self.tabs.currentWidget()

        if widget:

            filetypes = widget.canvas.get_supported_filetypes_grouped()
            import six        
            sorted_filetypes = list(six.iteritems(filetypes))
            sorted_filetypes.sort()
            default_filetype = widget.canvas.get_default_filetype()

            startpath = matplotlib.rcParams.get('savefig.directory', '')
            startpath = os.path.expanduser(startpath)
            start = os.path.join(startpath, widget.canvas.get_default_filename())
            filters = []
            selected_filter = None
            for name, exts in sorted_filetypes:
                exts_list = " ".join(['*.%s' % ext for ext in exts])
                filter = '%s (%s)' % (name, exts_list)
                if default_filetype in exts:
                    selected_filter = filter
                filters.append(filter)
            filters = ';;'.join(filters)

            fname, filter = _getSaveFileName(None,"Choose a filename to save to",start, filters, selected_filter)

            if fname:
                widget.canvas.figure.savefig(fname)

    def clear_figure(self):
        widget = self.tabs.currentWidget()
        if widget:
            widget.canvas.figure.clf()
            widget.canvas.draw()

    # def zoom_in(self):
    #     widget = self.tabs.currentWidget()
    #     mpl_toolbar = NavigationToolbar2QT(widget.canvas,None)
    #     zoom_action = [a for a in mpl_toolbar.actions() if a.text()=='Zoom'][0]
    #     zoom_action.trigger()





    # def toolbar_actions(self):
    #     print self.mpl_toolbar
    #     return [['', '', action, 0] for action in self.mpl_toolbar.actions()]


def new_figure_manager_given_figure(num, figure):
    """
    Create a new figure manager instance for the given figure.
    """
    canvas = MplCanvas(figure)
    widget = MplFigureTabWidget(canvas, num)
    # print all_widgets
    # return FigureManagerQT(canvas, num)

    for f in figure_containers:
        f.refresh_tab_widgets()
    return widget.manager


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
    pyplot.ion()

    backend_qt4.draw_if_interactive = draw_if_interactive
    backend_qt4agg.draw_if_interactive = draw_if_interactive

    backend_qt4.new_figure_manager_given_figure = new_figure_manager_given_figure
    backend_qt4agg.new_figure_manager_given_figure = new_figure_manager_given_figure

    backend_qt4agg.show = lambda: None

activate()
