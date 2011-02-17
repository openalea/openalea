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



from openalea.visualea.logger import LoggerView
from openalea.core.logger import QLogHandlerItemModel
class LoggerFactory(SingletonWidgetFactory):
    __name__ = "Logger"
    __namespace__ = "Openalea"

    def handles(self, input):
        return isinstance(input, QLogHandlerItemModel)

    def _instanciate_space(self, input, parent):
        assert isinstance(input, QLogHandlerItemModel)
        view = LoggerView(None, model=input)
        return None, LayoutSpace(self.__name__, self.__namespace__, view )

logger_f   = LoggerFactory()

def get_builtins():
    return [logger_f]
