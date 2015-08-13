#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
# -*- python -*-
#
#       openalea.image.analysis.gui.colormaps
#
#       Copyright 2010-2011 INRIA - CIRAD - INRA - ENS-Lyon
#
#       File author(s): Vincent Mirabet
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#       http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################
__license__= "Cecill-C"
__revision__=" $Id$ "

# import libraries
import sys
import numpy as np

def liste():
    """
    list of accessible colormaps
    """
    l=["black_and_white", "white_and_black", "rainbow_full", "rainbow_green2red", "rainbow_red2blue", "rainbow_green2blue", "rainbow_red2green", "rainbow_blue2red", "rainbow_blue2green"]
    print 


def black_and_white(lut):
    """
    creates a black and white lut
    """
    lut.alpha_range=[1.,1.]
    lut.hue_range=[0.,1.]
    lut.value_range=[1.0, 2.0]
    lut.saturation_range=[0.,0.]
    return lut

def white_and_black(lut):
    """
    creates a black and white lut
    """
    lut.alpha_range=[1.,1.]
    lut.hue_range=[0.,1.]
    lut.value_range=[1.0, 2.0]
    lut.saturation_range=[0.,0.]
    return lut


def rainbow_full(lut, begin=0., end=1.):
    """
    creates a rainbow lut
    """
    lut.alpha_range=[1.,1.]
    lut.hue_range=[begin,end]
    lut.value_range=[1.0, 1.0]
    lut.saturation_range=[1.,1.]
    return lut


def rainbow_green2red(lut, begin=0.33, end=1.):
    """
    creates a rainbow lut
    """
    lut.alpha_range=[1.,1.]
    lut.hue_range=[begin,end]
    lut.value_range=[1.0, 1.0]
    lut.saturation_range=[1.,1.]
    return lut


def rainbow_red2blue(lut, begin=0., end=0.66):
    """
    creates a rainbow lut
    """
    lut.alpha_range=[1.,1.]
    lut.hue_range=[begin,end]
    lut.value_range=[1.0, 1.0]
    lut.saturation_range=[1.,1.]
    return lut


def rainbow_green2blue(lut, begin=0.33, end=0.66):
    """
    creates a rainbow lut
    """
    lut.alpha_range=[1.,1.]
    lut.hue_range=[begin,end]
    lut.value_range=[1.0, 1.0]
    lut.saturation_range=[1.,1.]
    return lut


def rainbow_red2green(lut, begin=1., end=.33):
    """
    creates a rainbow lut
    """
    lut.alpha_range=[1.,1.]
    lut.hue_range=[begin,end]
    lut.value_range=[1.0, 1.0]
    lut.saturation_range=[1.,1.]
    return lut


def rainbow_blue2red(lut, begin=0.66, end=0.):
    """
    creates a rainbow lut
    """
    lut.alpha_range=[1.,1.]
    lut.hue_range=[begin,end]
    lut.value_range=[1.0, 1.0]
    lut.saturation_range=[1.,1.]
    return lut


def rainbow_blue2green(lut, begin=0.66, end=0.33):
    """
    creates a rainbow lut
    """
    lut.alpha_range=[1.,1.]
    lut.hue_range=[begin,end]
    lut.value_range=[1.0, 1.0]
    lut.saturation_range=[1.,1.]
    return lut

