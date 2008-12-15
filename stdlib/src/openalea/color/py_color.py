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
###############################################################################


__doc__="""Colormap Nodes"""
__license__= "Cecill-C"
__revision__=" $Id$ "


from openalea.core import *
import colormap
from colorsys import rgb_to_hsv, hsv_to_rgb


class RGB:
    """
    RGB Color
    """

    def __call__(self, inputs):
        """inputs is the list of input values"""
        return (inputs, )


def color_map(val, minval=0, maxval=1, coul1=80, coul2=20):
    map = colormap.ColorMap()

    if val is None:
        return lambda x: map(x, minval, maxval, coul1, coul2)
    elif callable(val):
        return lambda x: map(val(x), minval, maxval, coul1, coul2)
    else:
        return map(val, minval, maxval, coul1, coul2),


def rgb_color_map(value, minval=0, maxval=1, hue1=0,
        hue2=100, sat=220, val=220):
    newHue = ((value - minval)/(maxval - minval))*(hue2 - hue1) + hue1
    r, g, b = hsv_to_rgb(newHue/400., sat/255., val/255.)
    return (int(r*255), int(g*255), int(b*255)),
