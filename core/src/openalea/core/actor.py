# -*- coding: utf-8 -*-
#
#       OpenAlea.Core
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA
#
#       File author(s): Jerome Chopard <jerome.chopard@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite: http://openalea.gforge.inria.fr
#
###############################################################################
"""This module provides an actor interface"""

__license__ = "Cecill-C"
__revision__ = " $Id$ "

class IActor(object):
    """Interface to emulate a function

    The class :class:`IActor` implements an interface to emulate a function.
    It has functions to :func:`inputs` and :func:`outputs`.

    :Examples:

    >>> import openalea.core
    >>> a = openalea.core.actor.IActor()

    """

    def inputs(self):
        """Iterates on all input descriptions

        :Returns: iter of (input key, input interface)
        """
        raise NotImplementedError

    def outputs(self):
        """Iterates on all output descriptions

        :Returns: iter of (output key, output interface)
        """
        raise NotImplementedError

    def eval(self):
        """Computes output values when input is set"""
        raise NotImplementedError

    def set_input(self, key, value):
        """Set input specified by a key to the given value

        :param key: the input key
        :param value: the value key corresponding to the key
        """
        raise NotImplementedError

    def output(self, key):
        """Get value computed of the output

        :param key: a specified key
        :returns: the corresponding value

        """
        raise NotImplementedError


if __name__ == "__main__":
    import doctest
    doctest.testmod()
