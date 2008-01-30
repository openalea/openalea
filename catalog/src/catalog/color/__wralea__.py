# -*- python -*-
#
#       OpenAlea.Catalog
#
#       Copyright 2006 - 2007 INRIA - CIRAD - INRA  
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

__name__ = "catalog.color"

__all__ = ['colormap']

colormap = Factory(name='colormap', 
                   description='defines a color map from a range of values [I,J] to RGB', 
                   category='Visualisation.Color', 
                   nodemodule='py_color',
                   nodeclass='color_map',
                   inputs=[{'interface': IFloat, 'name': 'val'}, 
                           {'interface': IFloat, 'name': 'minval', 'value': 0}, 
                           {'interface': IFloat, 'name': 'maxval', 'value': 1}, 
                           {'interface': IFloat, 'name': 'color1HSV', 'value': 20}, 
                           {'interface': IFloat, 'name': 'color2HSV', 'value': 80}],
                   outputs=[{'interface': IRGBColor, 'name': 'color'}],
                   widgetmodule=None,
                   widgetclass=None,
                 )
		 

