# -*- python -*-
#
#       OpenAlea.Core
#
#       Copyright 2006-2010 INRIA - CIRAD - INRA
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
"""Central logging module from openalea.


Simple Tutorial
===============

Just to see how easy it is to log something::

    from openalea.core import logger
    a = 1234
    logger.debug("This is an evil value %d"%a)

This examples uses the defaults of the openalea.core.logger module:
There is one base logger name "openalea" that logs to a default stream
handler (prints out the logs to stderr).

There are more default loggers available::

    logger.default_init(level=logger.DEBUG, handlers=["file"])

This line will make logs go to rotating files in ~/.openalea/.

If you're running PyQt4::

    logger.default_init(level=logger.DEBUG, handlers=["qt"])

Will make your logs go to a QStandardItemModel that you can get
this way::

    itemModel = logger.get_handler("qt")

You can directly use it in a QListView.


Per-package loggers
===================
The previous example used the central OpenAlea logger. However, we recommend
you use a specific logger for your package, eg. Openalea.MTG::

    from openalea.core import logger
    mylogger = logger.get_logger("Openalea.MTG")
    [...]
    mylogger.debug("Execution reached this place...")

This will print nothing as `mylogger` is attached to no handler.
You can attach it to Openalea's handlers if they are any available::

    logger.connect_loggers_to_handlers(mylogger, logger.get_handler_names())
    mylogger.debug("Execution reached this other place...")

This will make every handler registered to OpenAlea receive the log.

Or you can connect it to your own handlers (In this case you can completely bypass Openalea.)
::
    import logging
    mylogger.addHandler(logging.FileHandler("path_to_file", mode="w"))

Indeed, `mylogger` is a logger.PatchedPyLogger slightly derived from
standard logging.Logger.

You can disconnect loggers and handlers::
    logger.disconnect_loggers_from_handlers(mylogger, logger.get_handler_names())

This will disconnect all handlers know by openalea from `mylogger`.

Logging levels
==============

Logging typically happens at different levels, from the less important to the worst case.
You have access to 5 default logging levels: DEBUG, INFO, WARNING, ERROR and CRITICAL.

Through the openalea.core.logger module::

    logger.debug(str)
    logger.info(str)
    logger.warning(str)
    logger.error(str)
    logger.critical(str)

Or a custom logger::

    mylogger = logger.get_logger("Openalea.MTG")
    mylogger.debug(str)
    mylogger.info(str)
    mylogger.warning(str)
    mylogger.error(str)
    mylogger.critical(str)

You can also send logs of arbitrary levels using the log(level (int), msg (str)) module function (or mylogger.log(int, str)).

Logger objects can be set to ignore logs that happen at levels lower than a chosen one.
The same goes for handlers.

In openalea.core.logger, you can set all loggers and handlers to have the same level::

    logger.set_global_logger_level(logger.INFO) #DEBUG logs will not be sent to handlers
    logger.set_global_handler_level(logger.ERROR) #DEBUG and ERROR logs will be ignored by handlers.

Of course you can do this more selectively::

    lg = logger.get_logger("Openalea.MTG")
    # lg will not send logs below the CRITICAL level:
    lg.setLevel(logger.CRITICAL)

    hd = logger.get_handler("qt")
    # hd will not process logs below INFO level.
    hd.setLevel(logger.INFO)

"""

__license__ = "Cecill-C"
__revision__ = " $Id$ "


import logging
import weakref
import sys
import os
import os.path
import collections
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL, NOTSET
import logging.handlers
from logging.handlers import TimedRotatingFileHandler
from openalea.core.singleton import Singleton


#: List of default handler names:
defaultHandlerNames = ["file",  #TimedRotatingFileHandler
                       "stream", #Output to stream
                       ]

#: The QLogHandlerItemModel class is only created if PyQt4 is already loaded
# otherwise ties core with PyQt and could prevent UI-less usage of core.

if "PyQt4.QtCore" in sys.modules and "PyQt4.QtGui" in sys.modules:
    QtCore = sys.modules["PyQt4.QtCore"]
    QtGui  = sys.modules["PyQt4.QtGui"]
    QT_LOGGING_MODEL_AVAILABLE=True
    defaultHandlerNames.append("qt") #log to a QStandardItemModel
else:
    #print __name__+".QLogHandlerItemModel won't be available"
    QT_LOGGING_MODEL_AVAILABLE=False


#######################
# TOP LEVEL FUNCTIONS #
#######################
def debug(msg):
    """Send a debug level msg to openalea's default logger.
    Handlers may or may not be connected yet."""
    LoggerOffice().get_default_logger().debug(msg)

def info(msg):
    """Send a info level msg to openalea's default logger.
    Handlers may or may not be connected yet."""
    LoggerOffice().get_default_logger().info(msg)

def warning(msg):
    """Send a warning level msg to openalea's default logger.
    Handlers may or may not be connected yet."""
    LoggerOffice().get_default_logger().warning(msg)

def error(msg):
    """Send a error level msg to openalea's default logger.
    Handlers may or may not be connected yet."""
    LoggerOffice().get_default_logger().error(msg)

def critical(msg):
    """Send a critical level msg to openalea's default logger.
    Handlers may or may not be connected yet."""
    LoggerOffice().get_default_logger().critical(msg)

def log(level, msg):
    """Send an arbitrary level msg to openalea's default logger.
    Handlers may or may not be connected yet."""
    LoggerOffice().get_default_logger().log(level, msg)

def get_logger(name):
    """Returns the logger called `name`. It will always return
    the same logger for the same name."""
    return LoggerOffice().get_logger(name)

def get_handler(name):
    """Returns the handler called `name`. It will always return
    the same handler for the same name."""
    return LoggerOffice().get_handler(name)

def get_logger_names():
    """Returns a list of logger names known by OpenAlea's LoggerOffice"""
    return LoggerOffice().get_logger_names()

def get_handler_names():
    """Returns a list of handler names known by OpenAlea's LoggerOffice"""
    return LoggerOffice().get_handler_names()

def connect_loggers_to_handlers(loggers, handlers):
    """Connects loggers to handlers. Each argument can be a single item or
    a list of them. Each item can be the name of the logger/handler or
    an instance of that."""
    LoggerOffice().connect_loggers_to_handlers(loggers, handlers)

def disconnect_loggers_from_handlers(loggers, handlers):
    """Disconnect loggers from handlers. Each argument can be a single item or
    a list of them. Each item can be the name of the logger/handler or
    an instance of that."""
    LoggerOffice().disconnect_loggers_from_handlers(loggers, handlers)

def set_global_logger_level(level):
    """Set level of all known loggers to level."""
    LoggerOffice().set_global_logger_level(level)

def set_global_handler_level(level):
    """Set level of all known handlers to level."""
    LoggerOffice().set_global_handler_level(level)

def default_init(level=logging.ERROR, handlers=defaultHandlerNames[:]):
    """Configure the LoggerOffice with a default `openalea` logger
    and handlers named in `handlers`. The latter is a list of strings
    from "qt", "file", "stream".

    - "qt" is only available if PyQt4 is installed. Logs will go to a QStandardItemModel.
    - "file" creates a rotating file handler. Logs are stored in "~/.openalea/log.log.X" files
      X get incremented every day. Beyond 20 days olds files get deleted.
    - "stream" logs to stderr.
    """
    LoggerOffice().set_defaults(level, handlers)

#####################
# END OF PUBLIC API #
#####################




############################
# Openalea Logging Central #
############################
class LoggerOffice(object):
    """ This class behaves as the central registry of loggers
    and handlers for Openalea. This way, the application can
    query information about them.
    """

    ##################################################################
    # As the top level function (public API) simply redirect to this #
    # singleton, see the documentation of the former.                #
    ##################################################################

    __metaclass__ = Singleton

    def __init__(self, level=DEBUG):
        logging.info("Logger started")
        # -- our formatter --
        self.__format = "%(levelname)s - %(asctime)s - %(message)s - %(pathname)s - %(lineno)d"
        #self.__format = "%(message)s - %(pathname)s - %(lineno)d - %(levelname)s - %(asctime)s"
        self.__dformat = "%H:%M:%S"
        self.__formatter = logging.Formatter(self.__format, self.__dformat)

        # -- user defined handlers --
        self.__handlers = {}

        # -- user defined loggers --
        self.__pyLoggers = {}
        self.__oaRootLogger = None

        # -- level of verbosity for handlers --
        self.__globalHandlerLevel    = DEBUG
        self.set_global_handler_level(self.__globalHandlerLevel)

        # -- level of verbosity for loggers --
        self.__globalLoggerLevel    = DEBUG
        self.set_global_logger_level(self.__globalLoggerLevel)

    ###################
    # Formatting logs #
    ###################
    def get_format(self):
        return self.__format

    def get_date_format(self):
        return self.__dformat

    ############
    # HANDLERS #
    ############
    def add_handler(self, name, handler):
        self.__handlers[name] = handler
        handler.setFormatter(self.__formatter)
        return handler

    def get_handler_names(self):
        return list(self.__handlers.iterkeys())

    def get_handler(self, name):
        handler =  self.__handlers.get(name)
        # if handler is None:
        #     raise Exception("LoggerOffice.get_handler: no such handler %s"%name)
        return handler

    def iter_handlers(self):
        return self.__handlers.itervalues()

    ###########
    # LOGGERS #
    ###########
    def add_logger(self, name):
        logger = logging.getLogger(name)
        self.__pyLoggers[name] = logger
        #we force the propagate attribute to False
        #otherwise the logging.root logger gets
        #called somehow
        logger.propagate=False # ugh why ?
        return logger

    def get_logger_names(self):
        return list(self.__pyLoggers.iterkeys())

    def get_logger(self, name):
        logger = self.__pyLoggers.get(name)
        if logger is None:
            logger = self.add_logger(name)
        return logger

    def iter_loggers(self):
        return self.__pyLoggers.itervalues()

    #################################
    # Logger to handler connections #
    #################################
    def connect_loggers_to_handlers(self, loggers, handlers, noDisconnect=False):
        loggers  = self.__iterable_check(loggers)
        handlers = self.__iterable_check(handlers)
        for logger in loggers:
            if isinstance(logger, str): logger = self.get_logger(logger)
            if not noDisconnect:
                for h in logger.handlers[:]:
                    logger.removeHandler(h)
            for handler in handlers:
                if isinstance(handler, str): handler = self.get_handler(handler)
                if None in [handler, logger]:
                    continue
                logger.addHandler(handler)

    def disconnect_loggers_from_handlers(self, loggers, handlers):
        loggers  = self.__iterable_check(loggers)
        handlers = self.__iterable_check(handlers)
        for logger in loggers:
            if isinstance(logger, str): logger = self.get_logger(logger)
            for handler in handlers:
                if isinstance(handler, str): handler = self.get_handler(handler)
                if None in [handler, logger]:
                    continue
                logger.removeHandler(handler)

    def __iterable_check(self, value):
        return value if issubclass(type(value), collections.MutableSequence) else [value]

    #########################
    # LOGGING LEVEL CONTROL #
    #########################
    def set_global_handler_level(self, level):
        self.__globalHandlerLevel = level
        for handler in self.iter_handlers():
            handler.setLevel(self.__globalHandlerLevel)

    def set_global_logger_level(self, level):
        self.__globalLoggerLevel = level
        for logger in self.iter_loggers():
            logger.setLevel(self.__globalLoggerLevel)

    ############
    # DEFAULTS #
    ############
    def set_defaults(self, level=logging.ERROR, handlers=None):
        if handlers is None:
            handlers = ["stream"]
        # -- default handlers --
        if QT_LOGGING_MODEL_AVAILABLE and "qt" in handlers:
            ha = self.get_handler('qt') or QLogHandlerItemModel(level=level)
            self.add_handler("qt", ha)
        elif "qt" in self.__handlers:
            del self.__handlers["qt"]

        if "file" in handlers:
            fname = os.path.expanduser("~/.openalea/log.log")
            ha = self.get_handler('file') or TimedRotatingFileHandler(fname,
                                                                      when='midnight',
                                                                      backupCount=30)
            ha.setLevel(level)
            self.add_handler("file", ha)
        elif "file" in self.__handlers:
            del self.__handlers["file"]

        if "stream" in handlers:
            ha = self.get_handler('stream') or logging.StreamHandler()
            ha.setLevel(level)
            self.add_handler("stream", ha)
        elif "stream" in self.__handlers:
            del self.__handlers["stream"]

        # -- default loggers --
        self.make_default_logger(handlers)
        self.set_global_logger_level(level)

    def make_default_logger(self, handlers=None):
        if handlers is None:
            handlers = ["stream"]
        self.__oaRootLogger = self.add_logger("openalea")
        self.disconnect_loggers_from_handlers("openalea", defaultHandlerNames[:])
        self.connect_loggers_to_handlers("openalea", handlers)
        return self.__oaRootLogger

    def set_default_logger(self, logger):
        self.__oaRootLogger = logger

    def get_default_logger(self):
        logger = self.__pyLoggers.get("openalea")
        if logger is None:
            logger = self.make_default_logger()
        return logger



# Copied and hacked out of logging.__init__.py
# _srcfile is used when walking the stack to check when we've got the first
# caller stack frame that is not from this file
if __file__[-4:].lower() in ['.pyc', '.pyo']:
    _srcfile = __file__[:-4] + '.py'
else:
    _srcfile = __file__
_srcfile = os.path.normcase(_srcfile)

class PatchedPyLogger(logging.Logger):
    """Patched Logger that identifies correctly the origin of the logger relative
    to this module"""
    def findCaller(self):
        """
        Find the stack frame of the caller so that we can note the source
        file name, line number and function name.
        """
        f = sys._getframe()
        rv = "(unknown file)", 0, "(unknown function)"
        while hasattr(f, "f_code"):
            co = f.f_code
            filename = os.path.normcase(co.co_filename)
            if filename in [_srcfile, logging._srcfile]:
                f = f.f_back
                continue
            rv = (filename, f.f_lineno, co.co_name)
            break
        return rv


logging.setLoggerClass(PatchedPyLogger)
default_init(level=logging.ERROR, handlers=["stream"])



########################################################
# -------- Some Logging handlers for Openalea -------- #
########################################################
if QT_LOGGING_MODEL_AVAILABLE:
    class QLogHandlerItemModel(QtGui.QStandardItemModel, logging.Handler):
        """A Handler that stores the logs in a QStandardItemModel, directly usable
        by QtGui.QTableViews"""

        cyan    = 146, 188, 227
        green   = 146, 231, 62
        yellow  = 236, 235, 130
        orange  = 236, 169, 35
        red     = 255, 28, 28
        __colormap__ = { "DEBUG"   : QtGui.QColor(*cyan),
                         "INFO"    : QtGui.QColor(*green),
                         "WARNING" : QtGui.QColor(*yellow),
                         "ERROR"   : QtGui.QColor(*orange),
                         "CRITICAL": QtGui.QColor(*red)
                         }

        def __init__(self, length=2000, level=NOTSET):
            QtGui.QStandardItemModel.__init__(self)
            logging.Handler.__init__(self, level)
            self.fields = [s[2].upper()+s[3:-2] for s in LoggerOffice().get_format().split(" - ")]

            # -- if we find the "Levelname" column it will be used for colouring --
            try:
                self.messageTypeIndex = self.fields.index("Levelname")
            except:
                self.messageTypeIndex = None

            self.setHorizontalHeaderLabels(self.fields)
            self.length = length

        def emit(self, record):
            while self.rowCount() > self.length:
                self.removeRow(0)

            vals = self.format(record).split(" - ")
            items = map(QtGui.QStandardItem, vals )

            # -- optionnal colouring --
            if self.messageTypeIndex is not None:
                msgType = vals[self.messageTypeIndex]
                color = QtGui.QBrush(QLogHandlerItemModel.__colormap__[msgType])
                it = items[self.messageTypeIndex]
                foreground = it.foreground()
                foreground.setColor(QtCore.Qt.black)
                it.setForeground(foreground)
                it.setBackground(color)
            self.appendRow(items)
