import os 
import numpy as np

from openalea.vpltk.qt import QtGui, QtCore

import matplotlib as mpl
from matplotlib.figure import Figure
from matplotlib.backend_bases           import FigureManagerBase as FigureManagerBase
from matplotlib.backends.backend_qt4agg import FigureManagerQT   as mpl_FigureManagerQT
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar


def new_figure_manager_given_figure(num, figure):
    """
    Create a new figure manager instance for the given figure.
    This function is made to replace its homonyme in mpl.backends.backend_qt4agg
    """
    return FigureManagerQTwithTab( num )


class MplTabWidget(QtGui.QTabWidget):
    """ Singleton class that implement mpl figure in a tab widget """
    _singleton = None
    def __init__(self, parent=None):
        QtGui.QTabWidget.__init__(self, parent=parent)
        
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.tabCloseEvent)
        
        self.canvas = []
        self.figure = []
        self.close_fct = []
        
    @staticmethod
    def get_singleton():
        if MplTabWidget._singleton is None:
            MplTabWidget._singleton = MplTabWidget()
        return MplTabWidget._singleton

    # manage canvas tabs
    # ------------------
    def add_tab_canvas(self, fig_num=None, close_function=None):
        """ add a tab canvas with mpl figure in it """
        figure  = Figure()
        if fig_num is None:
            fig_num = max(self.figure)+1
        
        # create canvas
        canvas = FigureCanvas(figure)
        widget = CanvasWidget(canvas, parent=self)
        
        # add canvas in a new tab
        canvas_num = self.addTab(widget, str(fig_num))
        self.setCurrentIndex(canvas_num)
        self.canvas.append(canvas)
        self.figure.append(fig_num)
        self.close_fct.append(close_function)
        
        return canvas, widget
        
    def tabCloseEvent(self, tab_index):
        close_fct = self.close_fct[tab_index]
        if close_fct:
            close_fct()
        else:
            self.remove_canvas_tab(tab_index)

    def remove_canvas_tab(self, tab_index):
        self.removeTab(tab_index)
        del self.canvas[tab_index]
        del self.figure[tab_index]

    def remove_canvas_widget(self, widget):
        """ remove the tab containing given `widget` """
        index = self.indexOf(widget)
        if index>=0:
            self.remove_canvas_tab(index)
        else:
            print 'MplTabWidget does not contain widget:', widget

    # duck type required QMainWidow interface
    # ---------------------------------------
    def get_window(self):
        """ return parent window, creating it if necessary """
        if self.parent() is None:
            self._window = QtGui.QMainWindow()
            self._window.setCentralWidget(self)
        p = self.parent()
        while not isinstance(p,QtGui.QMainWindow):
            p = p.parent()
        return p

    def show(self):
        """ duck typing of QMainWindow.show """
        return self.get_window().show()

    def statusBar(self):
        """ duck typing of QMainWindow.statusBar """
        return self.get_window().statusBar()
        
    ##def __del__(self):
    ##    print 'MplTabWidget __del__'
    ##    if self is self._singleton:
    ##        MplTabWidget._singleton = None

class CanvasWidget(QtGui.QWidget):
    """ Widget that contains a mpl canvas """
    def __init__(self, canvas, parent=None):
        QtGui.QWidget.__init__(self, parent=parent)
        self.setLayout(QtGui.QVBoxLayout())
        layout = self.layout()
        layout.setSpacing(0)
        layout.setMargin(0)
        layout.addWidget(canvas)
        
    def addToolBar(self, toolbar):
        self.layout().insertWidget(0,toolbar)

class FigureManagerQTwithTab(mpl_FigureManagerQT):
    """ qt4agg.FigureManageQT subclass that put mpl figures in a MplTabWidget """
    def __init__( self, num ):
        """ overwrite the FigureManageAt.__init__ """
        focused = QtGui.QApplication.focusWidget()
        self.window = MplTabWidget.get_singleton()
        self.canvas, self.widget = self.window.add_tab_canvas(num, self._widgetclosed)
        FigureManagerBase.__init__( self, self.canvas, num )
        
        ##self.window.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        ##image = os.path.join( mpl.rcParams['datapath'],'images','matplotlib.png' )
        ##self.window.setWindowIcon(QtGui.QIcon( image ))

        # Give the keyboard focus to the figure instead of the
        # manager; StrongFocus accepts both tab and click to focus and
        # will enable the canvas to process event w/o clicking.
        # ClickFocus only takes the focus is the window has been
        # clicked
        # on. http://developer.qt.nokia.com/doc/qt-4.8/qt.html#FocusPolicy-enum
        self.canvas.setFocusPolicy( QtCore.Qt.StrongFocus )
        self.canvas.setFocus()

        ##QtCore.QObject.connect( self.widget, QtCore.SIGNAL( 'destroyed()' ),
        ##                    self._widgetclosed )
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
        ##self.window.setCentralWidget(self.canvas)

        if mpl.is_interactive():
            self.window.show()

        def notify_axes_change( fig ):
            # This will be called whenever the current axes is changed
            self.window.setCurrentWidget( self.widget )
            if self.toolbar is not None:
                self.toolbar.update()
        self.canvas.figure.add_axobserver( notify_axes_change )
        
        if focused is not None:
            focused.setFocus()

    def destroy( self, *args ):
        """ override to close only the suitable tab, not the whole MplTabWidget """
        if self.toolbar: self.toolbar.destroy()
        self.window.remove_canvas_widget(self.widget)

    ##def _widgetclosed( self ):
    ##    print 'FigureManagerQTwithTab._widgetclosed'
    ##    mpl_FigureManagerQT._widgetclosed(self)


