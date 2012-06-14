# -*- python -*-
#
#       colormap manipulations
#
#       Copyright 2006 - 2011 INRIA - CIRAD - INRA
#
#       File author(s): Jerome Chopard <jerome.chopard@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
################################################################################
"""
This module provide a set of palettes to associate colors to data
"""

__license__= "Cecill-C"
__revision__=" $Id: $ "

import numpy
from colorsys import hsv_to_rgb,rgb_to_hsv
from numpy import array,uint32, uint8, arange, linspace

from matplotlib import colors, cm

fixed_palette_names = ["grayscale", "grayscale_alpha", "rainbow","bwrainbow","bw"]
palette_names = ["grayscale", "grayscale_alpha", "rainbow","bwrainbow","bw"]
palette_names.extend([m for m in cm.datad if not m.endswith("_r")])

__all__ = fixed_palette_names + ["palette_names","palette_factory"]

"""
Some developper documentation: This module implements some
color LUTs, accessible using palette_factory.

What are LUTs? They are simple vectors of color values and are used
to display scalar images. If an image has a pixel of value 10,
the display system will look in the LUT and index 10 to find what
is its favourite colour.

In some way they convert undisplayable scalars to displayable colors.
For uint8 images this isn't obvious as most display systems allow some sort
of 8 bit representation (the implicit LUT being greyscale),
but if you have higher depth images like, uint16 which is fairly frequent,
systems can't handle this. What they can handle is RGB[A], or more precisely,
[A]RGB.

What is RGB[A]? Practically, it is a color that is encoded using 8bit per channel.
So we have 24bits or 32bits deep images. This means that each channel only has to
be represented as a uint8. There IS another representation that fuses all channels
into one single uint32 (for 24bits depth, the alpha is forced to 255).

The LUTs that are created in this module treat each channel seperately, always 4 channels
(eg. 4*uint8 per value, instead of 1*uint32). This is why LUT arrays are uint8, no need
for them to be uint32.

The palette_factory has an option to combine all 4 channels of a value into the uint32 ARGB32
representation (even though to be suitable for Qt it is actually ABGR for some reason).
"""

def bw () :
    """Black and white palette
    """
    return array([(0,0,0),(255,255,255)],uint8)

def grayscale (cmax, alpha = False) :
    """Grayscale values ranging from 0 to 255

    :Parameters:
        - `cmax` (int) - data maximum value

    :Returns Type: list of (R,G,B,(A) )
    """
    if cmax==0 : cmax = 255
    pal = [(int(i * 255. / cmax),
        int(i * 255. / cmax),
        int(i * 255. / cmax),
        255) for i in xrange(cmax + 1)]

    return array(pal,uint8)

def grayscale_alpha (cmax, alpha = False) :
    """Grayscale values ranging from 0 to 255

    :Parameters:
        - `cmax` (int) - data maximum value

    :Returns Type: list of (R,G,B,(A) )
    """
    if cmax==0 : cmax = 255
    pal = [(int(i * 255. / cmax),
            int(i * 255. / cmax),
            int(i * 255. / cmax),
            int(i * 255. / cmax) ) for i in xrange(cmax + 1)]

    return array(pal,uint8)

def rainbow (cmax) :
    """Rainbow values ranging from red to blue and violet

    :Parameters:
        - `cmax` (int) - data maximum value

    :Returns Type: list of (R,G,B)
    """
    if cmax==0 : cmax = 255
    cmax = float(cmax)
    pal = [tuple(int(v * 255) for v in hsv_to_rgb(i / cmax,1.,1.) ) + (255,) \
            for i in xrange(int(cmax + 1) )]

    return array(pal,uint8)

def bwrainbow (cmax, alpha = False) :
    """Black, White plus Rainbow values ranging from red to blue and violet

    :Parameters:
        - `cmax` (int) - data maximum value

    :Returns Type: list of int
    """
    if cmax==0 : cmax = 255
    cmax = float(cmax)
    pal = [(255,255,255,0),(0,0,0,0)] \
        + [tuple(int(v * 255) for v in hsv_to_rgb(i / cmax,1.,1.) ) + (255,) \
        for i in xrange(int(cmax - 1) )]

    return array(pal,uint8)



def matplotlib(cmax,alpha=False):
    cmap = cm.get_cmap()
    return convert(cmap,cmax,alpha)

def convert(cmap, cmax, alpha=False):
    data = numpy.linspace(0,1,num=cmax+1)
    pal = cmap(data,bytes=True)
    return pal

def to_argb_swap_columns_and_recast(pal):
    # -- okay this is twisted. I originally expected
    # to put column 3 at 0 and shift the three first to the right
    # to acheive ARGB32. However, this doesn't seem to work
    # (empirically) and this is the swapping that works:
    # RGBA -> ABGR. Can someone explain ? --

    new = numpy.zeros_like(pal)
    new[:,2] = pal[:,0]
    new[:,1] = pal[:,1]
    new[:,0] = pal[:,2]
    new[:,3] = pal[:,3]
    return new.view(dtype=numpy.uint32).flatten()

def from_argb_swap_columns_and_recast(pal):

    new = pal.view(dtype=uint8).reshape((len(pal),4))
    new2 = numpy.zeros_like(pal)
    new2[:,0] = pal[:,2]
    new2[:,1] = pal[:,1]
    new2[:,2] = pal[:,0]
    new2[:,3] = pal[:,3]
    return new2

palette_to_argb_func = to_argb_swap_columns_and_recast

def palette_factory (palname, cmax, as_ARGB=False) :
    if cmax==0 : cmax = 255
    pal = None
    if palname in fixed_palette_names:
        pal = globals()[palname](cmax)
    else:
        mpal = cm.get_cmap(palname)
        if mpal:
            pal = convert(mpal,cmax)

    if as_ARGB:
        return palette_to_argb_func(pal)
    else:
        return pal


