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
################################################################################

__doc__ = """ Wralea for Colormap"""
__license__ = "Cecill-C"
__revision__ = " $Id$ "

from openalea.core import *

__name__ = "openalea.color"
__alias__ = ["catalog.color"]

__all__ = ['colormap', 'rgbcolormap',]

colormap = Factory(name='colormap', 
                   description='defines a color map from a range of values [I,J] to RGB', 
                   category='Visualisation.Color', 
                   nodemodule='py_color',
                   nodeclass='color_map',
                   inputs=({'interface': IFloat, 'name': 'val'}, 
                           {'interface': IFloat, 'name': 'minval', 'value': 0}, 
                           {'interface': IFloat, 'name': 'maxval', 'value': 1}, 
                           {'interface': IFloat, 'name': 'color1HSV', 'value': 20}, 
                           {'interface': IFloat, 'name': 'color2HSV', 'value': 80}),
                   outputs=({'interface': IRGBColor, 'name': 'color'},
                            ),
                   widgetmodule=None,
                   widgetclass=None,
                 )
		 
rgbcolormap = Factory(name='rgbcolormap', 
                   description='defines a RGB color map from 2 colors given in HSV', 
                   category='Visualisation.Color', 
                   nodemodule='py_color',
                   nodeclass='rgb_color_map',
                   inputs=({'interface': IFloat, 'name': 'val'}, 
                           {'interface': IFloat, 'name': 'minval', 'value': 0}, 
                           {'interface': IFloat, 'name': 'maxval', 'value': 1}, 
                           {'interface': IInt(0,400), 'name': 'Hue1', 'value': 0}, 
                           {'interface': IInt(0,400), 'name': 'Hue2', 'value': 100},
                           {'interface': IInt(0,255), 'name': 'Sat', 'value': 220, 'showwidget' : False, 'hide' : True},
                           {'interface': IInt(0,255), 'name': 'Val', 'value': 220, 'showwidget' : False, 'hide' : True},
                           ),
                   outputs=(dict(name="Color", interface = IRGBColor,),
                            ),
                   widgetmodule=None,
                   widgetclass=None,
                 )
	
