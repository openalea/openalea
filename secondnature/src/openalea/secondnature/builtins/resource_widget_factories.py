# -*- python -*-
#
#       OpenAlea.Secondnature
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

from openalea.secondnature.extendable_objects import *



##########
# LOGGER #
##########

from openalea.visualea.logger import LoggerView
from openalea.core.logger import QLogHandlerItemModel, LoggerOffice

class LoggerFactory(ResourceWidgetFactory):
    __name__ = "Logger"
    __namespace__ = "Openalea"

    def __init__(self):
        ResourceWidgetFactory.__init__(self)
        from openalea.core.logger import LoggerOffice
        self.loggermodel = LoggerOffice().get_handler("qt")
        self.loggerurl = "oa://logger.local/"
        self.logger = Document("Logger",
                               "Openalea",
                               self.loggerurl,
                               self.loggermodel,
                               category="system")

        self.view  = LoggerView(None, model=self.loggermodel)
        self.space = LayoutSpace(self.__name__, self.__namespace__, self.view )

    def get_resource(self):
        return self.logger

    def validate_resource(self, res):
        return res == self.logger

    def get_resource_space(self, res):
        return self.space

    # def handles(self, url):
    #     return url.geturl() == "oa://logger.local/"

    # def _instanciate_space(self, url):
    #     assert self.handles(url)
    #     from . import documents


logger_f   = LoggerFactory()

def get_builtins():
    return [logger_f]
