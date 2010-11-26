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
"""Central logging module.

"""

__license__ = "Cecill-C"
__revision__ = " $Id$ "


import logging, weakref, sys, os, os.path
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL, NOTSET
from openalea.core.singleton import Singleton


#: If True, no default initialisation will be done. Not recommended though.
DONT_DEFAULT = False


#: The QLogHandlerItemModel class is only created if PyQt4 is available
# otherwise ties core with PyQt and could prevent UI-less usage of core.
try:
    from PyQt4 import QtCore, QtGui
    QT_LOGGING_MODEL_AVAILABLE=True
except Exception, e:
    print __name__+".QLogHandlerItemModel won't be available"
    QT_LOGGING_MODEL_AVAILABLE=False



#######################
# TOP LEVEL FUNCTIONS #
#######################
def debug(msg):
    LoggerOffice().get_default_logger().debug(msg)

def info(msg):
    LoggerOffice().get_default_logger().info(msg)

def warning(msg):
    LoggerOffice().get_default_logger().warning(msg)

def error(msg):
    LoggerOffice().get_default_logger().error(msg)

def critical(msg):
    LoggerOffice().get_default_logger().critical(msg)

def get_logger(name):
    return BaseLogger(name)


class BaseLogger(object):
    def __init__(self, name):
        self.__name = name.lower()
        self.__pyLogger = weakref.proxy(LoggerOffice().add_py_logger(self.__name))

    def get_name(self):
        return self.__name

    def debug(self, msg):
        self.__pyLogger.debug(msg)

    def info(self, msg):
        self.__pyLogger.info(msg)

    def warning(self, msg):
        self.__pyLogger.warning(msg)

    def error(self, msg):
        self.__pyLogger.error(msg)

    def critical(self, msg):
        self.__pyLogger.critical(msg)




############################
# Openalea Logging Central #
############################
class LoggerOffice(object):
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
        self.__useGlobalHandlerLevel = True
        self.__globalHandlerLevel    = DEBUG
        self.set_global_handler_level(self.__globalHandlerLevel)

        # -- level of verbosity for loggers --
        self.__useGlobalLoggerLevel = True
        self.__globalLoggerLevel    = DEBUG
        self.set_global_logger_level(self.__globalLoggerLevel)

    def get_format(self):
        return self.__format

    def get_date_format(self):
        return self.__dformat



    ############
    # HANDLERS #
    ############
    def add_handler(self, name, handler, attachToLoggers=set()):
        if self.__useGlobalHandlerLevel:
            handler.setLevel(self.__globalHandlerLevel)
        self.__handlers[name] = handler

        if attachToLoggers is None: #don't attach to anything
            pass
        else:
            sz = len(attachToLoggers)
            if sz > 0:
                for loggerName in attachToLoggers:
                    logger = self.get_py_logger(loggerName)
                    if logger:
                        logger.addHandler(handler)
            elif sz == 0: #all:
                for logger in self.iter_py_loggers():
                    logger.addHandler(handler)
                logging.root.addHandler(handler)


    def get_handler_names(self):
        return list(self.__handlers.iterkeys())

    def get_handler(self, name):
        return self.__handlers.get(name)

    def iter_handlers(self):
        return self.__handlers.itervalues()

    ###########
    # LOGGERS #
    ###########
    def add_py_logger(self, name, attachToHandlers=set()):
        logger = logging.getLogger(name)
        self.__pyLoggers[name] = logger
        logger.propagate=False
        if self.__useGlobalLoggerLevel:
            logger.setLevel(self.__globalLoggerLevel)

        if attachToHandlers is None: #don't attach to anything
            pass
        else:
            sz = len(attachToHandlers)
            if sz > 0:
                for handlerName in attachToHandlers:
                    handler = self.get_handler(handlerName)
                    if handler:
                        logger.addHandler(handler)
            elif sz == 0: #all:
                for handler in self.iter_handlers():
                    logger.addHandler(handler)
        return logger

    def get_py_logger_names(self):
        return list(self.__pyLoggers.iterkeys())

    def get_py_logger(self, name):
        return self.__pyLoggers.get(name)

    def iter_py_loggers(self):
        return self.__pyLoggers.itervalues()

    #########################
    # LOGGING LEVEL CONTROL #
    #########################
    # -- HANDLERS --
    def not_use_global_handler_level(self):
        self.__useGlobalHandlerLevel = False

    def use_global_handler_level(self):
        self.__useGlobalHandlerLevel = True
        for handler in self.iter_handlers():
            handler.setLevel(self.__globalHandlerLevel)

    def set_global_handler_level(self, level):
        self.__globalHandlerLevel = level
        if self.__useGlobalHandlerLevel:
            self.use_global_handler_level()

    # -- LOGGERS --
    def not_use_global_logger_level(self):
        self.__useGlobalLoggerLevel = False

    def use_global_logger_level(self):
        self.__useGlobalLoggerLevel = True
        for logger in self.iter_py_loggers():
            logger.setLevel(self.__globalLoggerLevel)

    def set_global_logger_level(self, level):
        self.__globalLoggerLevel = level
        if self.__useGlobalLoggerLevel:
            self.use_global_logger_level()

    ############
    # DEFAULTS #
    ############
    def set_defaults(self, level=None):
        # -- some standard handlers --
        level = level if level else \
                self.__globalHandlerLevel if self.__useGlobalHandlerLevel else DEBUG
        # -- default handlers --
        if QT_LOGGING_MODEL_AVAILABLE:
            ha = QLogHandlerItemModel(level=level)
            ha.setFormatter(self.__formatter)
            self.__handlers["qt"] = ha

        flogger = logging.FileHandler(os.path.expanduser("~/.openalea/log.log"))
        flogger.setLevel(level)
        self.__handlers["file"] = flogger

        # -- default loggers --
        self.make_default_logger()

    def make_default_logger(self):
        self.__oaRootLogger = BaseLogger("openalea")

    def set_default_logger(self, logger):
        assert isinstance(logger, BaseLogger)
        self.__oaRootLogger = logger

    def get_default_logger(self):
        if self.__oaRootLogger is None:
            raise Exception("Default logger not set, call self.make_default_logger()")
        return self.__oaRootLogger



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
            self.__length = length

        def emit(self, record):
            if self.rowCount() > self.__length:
                self.removeRow(0)
            vals = self.format(record).split(" - ")
            items = map(QtGui.QStandardItem, vals )

            # -- optionnal colouring --
            if self.messageTypeIndex is not None:
                msgType = vals[self.messageTypeIndex]
                color = QtGui.QBrush(QLogHandlerItemModel.__colormap__[msgType])
                items[self.messageTypeIndex].setBackground(color)
            self.appendRow(items)




if not DONT_DEFAULT:
    LoggerOffice().set_defaults(DEBUG)



# # passThroughLogging = False
# # def loggingDecorator(f, f2):
# #     if passThroughLogging:
# #         return f
# #     else:
# #         return f2(f)

# def timeMe(f):
#     import time
#     def timedFunc(*args, **kwargs):
#         c1 = time.clock()
#         f(*args, **kwargs)
#         c2 = time.clock()
#         diff = c2-c1
#         msg = "Function " + f.__name__ + " took " + str(diff) + " to acheive."
#         Logger()._info(f.__module__, msg)
#     return timedFunc


# @timeMe
# def func(r=1000000):
#     for i in xrange(r):
#         i += i

