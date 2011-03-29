#!/usr/bin/python
# -*- python -*-
#
#       OpenAlea.SecondNature
#
#       Copyright 2006-2011 INRIA - CIRAD - INRA
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

__license__ = "CeCILL v2"
__revision__ = " $Id$"

import os, sys

import traceback

def level_one(args=None):
    if args is None:
        args = sys.argv

    # Restore default signal handler for CTRL+C
    import signal


    from PyQt4 import QtGui
    from PyQt4 import QtCore

    from openalea.core import logger
    from openalea.secondnature import mainwindow

    class SecondNature(QtGui.QApplication):
        """Materialisation of the Openalea application.
        Does the basic inits. The session is initialised
        in a thread. It is safe to use once the sessionStarted
        signal has been emitted."""


        def __init__(self, argv):
            QtGui.QApplication.__init__(self, argv)
            # -- reconfigure LoggerOffice to use Qt log handler and a file handler --
            logger.default_init(level=logger.DEBUG, handlers=["stream", "qt"]) #TODO get level from settings
            logger.connect_loggers_to_handlers(logger.get_logger_names(), logger.get_handler_names())

            if __debug__:
                logger.set_global_logger_level(logger.DEBUG)
            else:
                logger.set_global_logger_level(logger.WARNING)

            # -- status clearout timer --
            self.__statusTimeout = QtCore.QTimer(self)
            self.__statusTimeout.setSingleShot(True)
            self.__statusTimeout.timeout.connect(self.clear_status_message)

            # -- main window --
            self.win = mainwindow.MainWindow(None)
            self.post_status_message("Starting up! Please wait")
            self.win.show()
            self.clear_status_message()

        def post_status_message(self, msg, timeout=2000):
            if self.__statusTimeout.isActive():
                self.__statusTimeout.stop()
            self.win.statusBar().showMessage(msg)
            self.__statusTimeout.start(timeout)

        def clear_status_message(self):
            self.win.statusBar().clearMessage()

        def event(self, e):
            if e.type() == QtCore.QEvent.ApplicationActivate and \
                   not self.win.extensions_initialised:
                self.win.init_extensions()
            return QtGui.QApplication.event(self, e)



    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = SecondNature(args)
    return app.exec_()

if( __name__ == "__main__"):
    level_one()





