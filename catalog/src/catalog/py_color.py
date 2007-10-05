

from openalea.core import *
import openalea.catalog.colormap as colormap


def color_map(val,minval = 0,maxval = 1,coul1 = 80,coul2 = 20):
    map = colormap.ColorMap()
    if val is None:
	return lambda x: map(x,minval,maxval,coul1,coul2)
    elif callable(val):
	return lambda x: map(val(x),minval,maxval,coul1,coul2)
    else: return map(val,minval,maxval,coul1,coul2),

