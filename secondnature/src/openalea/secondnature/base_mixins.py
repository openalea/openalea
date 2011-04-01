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
__revision__ = " $Id$ "


from openalea.core.logger import get_logger

loffer = get_logger(__name__)

class HasName(object):
    # -- PROPERTIES --
    name = property(lambda x: x._name, lambda x, y:x.set_name(y))

    def __init__(self, name):
        assert isinstance(name, str)
        self._name = name

    def set_name(self, value):
        self._name = value



class CanBeStarted(object):
    # -- PROPERTIES --
    started    = property(lambda x:x.__started)

    def __init__(self):
        self.__started = False

    #################
    # EXTENSION API #
    #################
    def start(self):
        return True

    #################
    # Private Stuff #
    #################
    def _start_0(self):
        try:
            self.__started = self.start()
        except Exception, e:
            logger.error(str(e))

