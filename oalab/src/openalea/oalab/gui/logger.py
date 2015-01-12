# -*- python -*-
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2013 INRIA - CIRAD - INRA
#
#       File author(s): Julien Coste <julien.coste@inria.fr>
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
__revision__ = "$Id: $"

from openalea.core import logger
from openalea.visualea.logger import LoggerView

class Logger(LoggerView):
    """
    Widget to check the log. Cf. Visualea
    
    Use it like that:
    #################
    import Logger
    widget_logger = Logger()
    
    # Put the widget in an QApplication
    
    from openalea.core import logger 
    logger.debug("my message")
    logger.warning("Can't do that!")
    logger.info("John is in the kitchen")
    """
    def __init__(self, parent=None):
        # -- reconfigure LoggerOffice to use Qt log handler and a file handler --
        logger.default_init(level=logger.DEBUG, handlers=["qt"]) #TODO get level from settings
        logger.connect_loggers_to_handlers(logger.get_logger_names(), logger.get_handler_names())
        model = logger.LoggerOffice().get_handler("qt")
        super(Logger, self).__init__(parent=parent, model=model)
        self.setAccessibleName("Logger")


