#!/usr/bin/python

# -*- python -*-
#
#       OpenAlea.Visualea: OpenAlea graphical user interface
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA
#
#       File author(s): Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#                       Christophe Pradal <christophe.prada@cirad.fr>
#
#       Distributed under the CeCILL v2 License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL_V2-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################
"""Main Module for graphical interface"""

__license__ = "CeCILL v2"
__revision__ = "$Id$"


import sys
from PyQt4 import QtGui
from PyQt4 import QtCore

from openalea.core import logger
from openalea.visualea.mainwindow import MainWindow
from openalea.core.session import Session



class Openalea(QtGui.QApplication):
    """Materialisation of the Openalea application.
    Does the basic inits. The session is initialised
    in a thread. It is safe to use once the sessionStarted
    signal has been emitted."""

    sessionStarted = QtCore.pyqtSignal(object)

    def __init__(self, args):
        QtGui.QApplication.__init__(self, args)
        # -- redirect stdout to null if pythonw --
        set_stdout()
        # -- reconfigure LoggerOffice to use Qt log handler and a file handler --
        logger.default_init(level=logger.DEBUG, handlers=["qt"])
        logger.connect_loggers_to_handlers(logger.get_logger_names(), logger.get_handler_names())
        if __debug__:
            logger.set_global_logger_level(logger.DEBUG)
        else:
            logger.set_global_logger_level(logger.WARNING)
        # -- show the splash screen --
        self.splash = show_splash_screen()
        # -- main window --
        self.win = MainWindow(None)
        self.win.show()
        self.sessionStarted.connect(self.win.on_session_started)
        # -- start session in a thread --
        self.sessionth = threadit(timeit, self, self.__cb_session_thread_end, Session)

    def __cb_session_thread_end(self):
        self.splash.finish(self.win)
        self.sessionStarted.emit(self.sessionth.retVal)

    @staticmethod
    def check_qt_version():
        """Ensure we are running a minimal version of Qt"""
        version = QtCore.QT_VERSION_STR
        # QT_VERSION_STR implement __le__ operator
        if(version < '4.5.2'):
            mess = QtGui.QMessageBox.warning(None,
                                             "Error",
                                             "Visualea needs Qt library >= 4.5.2")
            sys.exit(-1)


def main(args):
    # Restore default signal handler for CTRL+C
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    Openalea.check_qt_version()
    app = Openalea(args)
    return app.exec_()




###########################
# A few utility functions #
###########################
import os
import time


def set_stdout():
    """Disable stdout if using pythonw"""
    if("pythonw" in sys.executable):
        nullfd = open(os.devnull, "w")
        sys.stdout = nullfd
        sys.stderr = nullfd

def show_splash_screen():
    """Show a small splash screen to make people wait for OpenAlea to startup"""
    import metainfo
    pix = QtGui.QPixmap(":/icons/splash.png")
    splash = QtGui.QSplashScreen(pix, QtCore.Qt.WindowStaysOnTopHint)
    splash.show()
    message = QtCore.QString( metainfo.get_copyright() +
                              "Version : %s\n"%(metainfo.get_version(),) +
                              "Loading modules...")
    splash.showMessage(message, QtCore.Qt.AlignCenter|QtCore.Qt.AlignBottom)
    # -- make sure qt really display the message before importing the modules.--
    QtGui.QApplication.processEvents()
    return splash

def timeit(f, *args, **kwargs):
    t1 = time.time()
    ret = f(*args, **kwargs)
    t2 = time.time()
    logger.debug(f.__name__+" took "+str(t2-t1)+" seconds")
    if __debug__:
        print
    return ret

def threadit(f, parent=None, endCb=None, *args, **kwargs):
    """Utility function that takes a function f and runs it under
    a new thread. The threadit function immediately returns
    a CustomThread. If `endCb` is provided, it must be a function with
    no arguments (or an instance method). It will be called on
    thread end.

    The returned Custom thread contains the return value of the `f`::

    def func():
        return "apricots"

    def onFuncEnd():
        print th.retVal

    th = threadit(func, endCb=onFuncEnd)


    It probably requires a QApp to be started somewhere.
    """
    class CustomThread(QtCore.QThread):
        def __init__(self, target, parent=parent, args=[], kwargs={}):
            QtCore.QThread.__init__(self, parent=parent)
            self.target = target
            self.args   = args
            self.kwargs = kwargs
            self.retVal = None

        def run(self):
            self.retVal = self.target(*args,**kwargs)

    th = CustomThread( target = f,
                       args = args,
                       kwargs = kwargs)
    if endCb:
        th.finished.connect(endCb)
    th.start()
    return th








############################
# Ok, Let's start for real #
############################
if __name__ == "__main__":
    main(sys.argv)

