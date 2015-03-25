# -*- python -*-
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2014 INRIA
#
#       File author(s): Guillaume Cerutti <guillaume.cerutti@inria.fr>
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

from openalea.core.interface import IInterface

class IColormap(IInterface):

    """
    Dict of rgb colors with 0-1 positions as keys.
    Example:

    dict([(0.0, (0.0, 0.0, 0.0)),
          (1.0, (1.0, 1.0, 1.0))])

    """
    __alias__ = u'Colormap'

    def __init__(self,**kargs):
        IInterface.__init__(self, **kargs)
        self.value = self.default()

    @classmethod
    def default(cls):
        """
        Reinitialize control to default grey colormap
        """
        value = dict([(0.0, (0.0, 0.0, 0.0)), (1.0, (1.0, 1.0, 1.0))])
        return value

    def __repr__(self):
        return self.__class__.__name__


class IIntRange(IInterface):

    """
    Tuple of two ordered integers
    Example:

    (0, 255)

    """
    __alias__ = u'Integer range'

    def __init__(self, min= -2**24, max=2**24,  **kargs):
        IInterface.__init__(self, **kargs)
        self.min = min
        self.max = max

    @classmethod
    def default(cls):
        return (0, 255)

    def __repr__(self):
        default_min = -2**24
        default_max = 2**24
        if (self.min == default_min and
            self.max == default_max):
            return self.__class__.__name__
        else:
            return 'IIntRange(min=%d, max=%d)' % (self.min, self.max)

