# -*- python -*-
#
#       OpenAlea.StdLib
#
#       Copyright 2006 - 2008 INRIA - CIRAD - INRA
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
#############################################################################


__doc__="""String manipulation"""
__license__= "Cecill-C"
__revision__=" $Id$ "

from openalea.core import *

# File name manipulation


def str_split(string_, char):
    """Split a String

    :param string_ : a String
    :param char : a split character
    :returns: the splitted string
    """
    return (string_.split(char), )


def str_join(list_, char):
    """Join a list

    :param list_: A list of String
    :param char: the join character
    :returns:  the joinned string
    """
    return (char.join(list_), )


def str_strip(string_, chars):
    """
    Return a copy of the string with leading and trailing whitespace removed.
    """
    return (string_.strip(chars), )


class String(Node):
    """
    String Variable

    :param 0: the stored value
    :returns 0: transmit the stored value
    """

    def __call__(self, inputs):
        """ inputs is the list of input values """
        s = str(inputs[0])
        self.set_caption(repr(s))
        return (s, )


def text(long_str):
    """ Return a copy of the input string. """
    return (str(long_str), )
