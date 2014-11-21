from __future__ import absolute_import

import os
import numpy as np

from openalea.vpltk.qt import QtGui, QtCore

import matplotlib as mpl
from matplotlib.figure import Figure
from matplotlib.backend_bases import FigureManagerBase as FigureManagerBase
from matplotlib.backends.backend_qt4agg import FigureManagerQT as mpl_FigureManagerQT
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar


def new_figure_manager_given_figure(num, figure):
    """
    Create a new figure manager instance for the given figure.
    This function is made to replace its homonyme in mpl.backends.backend_qt4agg
    """
    return FigureManagerQTwithTab(num)


class AbstractMplWidget(QtGui.QWidget):

    """
    Abstract class for widget using matplotlib

    It implement the `get_singleton` method that return the class `_singleton`
    attribute (instanciating it if necessary). Such a subclass can:
     - Have its own `_singleton` attribute, set to None by default
     - Override the class method `create_singleton` that takes no argument which
       return the singleton instance. 
       Otherwise the default method calls the class constructor with no argument

    It also duck type the QMainWindow interface used by matplotlib
    """
    _singleton = None

    @classmethod
    def get_singleton(cls):
        if cls._singleton is None:
            cls._singleton = cls.create_singleton()
        return cls._singleton

    @classmethod
    def create_singleton(cls):
        return cls()

    # duck type required QMainWidow interface
    # ---------------------------------------
    def get_window(self):
        """ return (grand)parent window, creating it if necessary """
        w = self        # top widget which is not a main window
        p = w.parent()  # its parent, which should be a main window
        while p is not None and not isinstance(p, QtGui.QMainWindow):
            w = p
            p = w.parent()

        if p is None:
            p = QtGui.QMainWindow()
            p.setCentralWidget(w)
            self._window = p  # needs to keep a ref or else it'll be deleted

        return p

    def show(self):
        """ duck typing of QMainWindow.show """
        return self.get_window().show()

    def statusBar(self):
        """ duck typing of QMainWindow.statusBar """
        return self.get_window().statusBar()


class MplTabWidget(QtGui.QTabWidget, AbstractMplWidget):

    """ Singleton class that implement mpl figure in a tab widget """
    _singleton = None                           # has its own singleton

    def __init__(self, parent=None):
        QtGui.QTabWidget.__init__(self, parent=parent)

        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.tabCloseEvent)

        self.widget = []
        self.close_fct = []

        # events & actions
        self.setFocusPolicy(QtCore.Qt.StrongFocus)  # keyboard & mouse focus
        self.setAcceptDrops(True)                  # accept drop event

    # manage canvas tabs
    # ------------------
    def add_tab_canvas(self, fig_num=None, close_function=None):
        """ add a tab canvas with mpl figure in it """
        if fig_num is None:
            fig_num = max(self.figure) + 1

        # create canvas
        widget = CanvasWidget(parent=self)

        # add canvas in a new tab
        canvas_num = self.addTab(widget, str(fig_num))
        self.setCurrentIndex(canvas_num)
        self.widget.append(widget)
        self.close_fct.append(close_function)

        return widget.canvas, widget

    def tabCloseEvent(self, tab_index):
        close_fct = self.close_fct[tab_index]
        if close_fct:
            close_fct()
        else:
            self.remove_canvas_tab(tab_index)

    def remove_canvas_tab(self, tab_index):
        self.removeTab(tab_index)
        del self.widget[tab_index]

    def remove_canvas_widget(self, widget):
        """ remove the tab containing given `widget` """
        index = self.indexOf(widget)
        if index >= 0:
            self.remove_canvas_tab(index)
        else:
            print 'MplTabWidget does not contain widget: ' + repr(widget)

    # drop event for OpenAleaLab
    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("text/plain"):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        mimeData = event.mimeData()
        if not mimeData.hasFormat("text/plain"):
            event.ignore()

        import os
        from scipy import ndimage as nd
        from matplotlib import pyplot as plt

        filename = str(mimeData.text())
        if filename.startswith("data/'"):
            # mimeData come from OpenAleaLab
            from openalea.oalab.session.session import Session
            path = Session().project.path
            filename = filename[6:].split("'")[0]
            filename = str(path / 'data' / filename)

        # load image and imshow it
        print filename
        img = nd.imread(filename)
        plt.clf()
        plt.imshow(img)
        ax = plt.gca()
        ax.set_position([0, 0, 1, 1])

    # OALab actions
    def get_plugin_actions(self):
        """ return actions list for OAlab """
        def add_some_action(name, fct, key):
            action = QtGui.QAction(name, self)
            action.triggered.connect(fct)
            self.addAction(action)

            action.setShortcuts([QtGui.QKeySequence(k).toString() for k in key])
            action.setShortcutContext(QtCore.Qt.WidgetWithChildrenShortcut)

            return action

        actions = []
        action = add_some_action('clear', self.clf, ['Ctrl+delete', 'Ctrl+backspace'])
        actions.append(['pyplot', action, 1])
        action = add_some_action('new',  self.new_figure,  ['Ctrl+N'])
        actions.append(['pyplot', action, 1])
        action = add_some_action('close', self.close_figure, ['Ctrl+W'])
        actions.append(['pyplot', action, 1])

        return actions

    def toolbar_actions(self):
        return [['Plot2D', a[0], a[1], a[2]] for a in self.get_plugin_actions()]

    def clf(self):
        from matplotlib import pyplot as plt
        plt.clf()

    def new_figure(self):
        from matplotlib import pyplot as plt
        plt.figure()

    def close_figure(self):
        from matplotlib import pyplot as plt
        plt.close()


class CanvasWidget(QtGui.QWidget):

    """ Widget that contains a mpl canvas """

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent=parent)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        self.setLayout(QtGui.QVBoxLayout())
        layout = self.layout()
        layout.setSpacing(0)
        layout.setMargin(0)
        layout.addWidget(self.canvas)

        self.setFocusPolicy(QtCore.Qt.StrongFocus)  # strong = keyboard & mouse focus

    def addToolBar(self, toolbar):
        self.layout().insertWidget(0, toolbar)


class FigureManagerQTwithTab(mpl_FigureManagerQT):

    """ qt4agg.FigureManageQT subclass that put mpl figures in a MplTabWidget """

    def __init__(self, num):
        """ overwrite the FigureManageAt.__init__ """
        focused = QtGui.QApplication.focusWidget()
        self.window = MplTabWidget.get_singleton()
        self.canvas, self.widget = self.window.add_tab_canvas(num, self._widgetclosed)
        FigureManagerBase.__init__(self, self.canvas, num)

        # self.window.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        ##image = os.path.join( mpl.rcParams['datapath'],'images','matplotlib.png' )
        ##self.window.setWindowIcon(QtGui.QIcon( image ))

        # Give the keyboard focus to the figure instead of the
        # manager; StrongFocus accepts both tab and click to focus and
        # will enable the canvas to process event w/o clicking.
        # ClickFocus only takes the focus is the window has been
        # clicked
        # on. http://developer.qt.nokia.com/doc/qt-4.8/qt.html#FocusPolicy-enum
        self.canvas.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.canvas.setFocus()

        # QtCore.QObject.connect( self.widget, QtCore.SIGNAL( 'destroyed()' ),
        # self._widgetclosed )
        self.window._destroying = False

        self.toolbar = self._get_toolbar(self.canvas, self.widget)
        if self.toolbar is not None:
            self.widget.addToolBar(self.toolbar)
            QtCore.QObject.connect(self.toolbar, QtCore.SIGNAL("message"),
                                   self._show_message)
            tbs_height = self.toolbar.sizeHint().height()
        else:
            tbs_height = 0

        # resize the main window so it will display the canvas with the
        # requested size:
        ##cs = canvas.sizeHint()
        ##sbs = self.window.statusBar().sizeHint()
        ##self._status_and_tool_height = tbs_height+sbs.height()
        ##height = cs.height() + self._status_and_tool_height
        ##self.window.resize(cs.width(), height)
        ##
        # self.window.setCentralWidget(self.canvas)

        if mpl.is_interactive():
            self.window.show()

        def notify_axes_change(fig):
            # This will be called whenever the current axes is changed
            self.window.setCurrentWidget(self.widget)
            if self.toolbar is not None:
                self.toolbar.update()
        self.canvas.figure.add_axobserver(notify_axes_change)

        if focused is not None:
            focused.setFocus()

    def destroy(self, *args):
        """ override to close only the suitable tab, not the whole MplTabWidget """
        if self.toolbar:
            self.toolbar.destroy()
        self.window.remove_canvas_widget(self.widget)

    # def _widgetclosed( self ):
    # print 'FigureManagerQTwithTab._widgetclosed'
    # mpl_FigureManagerQT._widgetclosed(self)
