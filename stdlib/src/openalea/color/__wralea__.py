# -*- python -*-
#
#       OpenAlea.StdLib
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA  
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################
"""Node declaration for colors
"""

__license__ = "Cecill-C"
__revision__ = " $Id$ "

from openalea.core import *
from color_interface import IColor
from color_interface_widget import IColorWidget

__name__ = "openalea.color"
__alias__ = ["catalog.color"]

__all__ = ['colormap', 'rgbcolormap']

color = Factory(name = "color",
                description = "edit color",
                category = "datatype,image",
                nodemodule = "py_color",
                nodeclass = "ColorNode",
                inputs = (dict(name = "RGB",
                               interface = IColor,
                               value = (0,0,0) ),),
                outputs = (dict(name = "RGB", interface = IColor),),
                )

__all__.append("color")

black = Factory(name = "black",
                description = "black color",
                category = "datatype,image",
                nodemodule = "py_color",
                nodeclass = "BlackNode",
                inputs = (),
                outputs = (dict(name = "RGB", interface = IColor),),
                )

__all__.append("black")

white = Factory(name = "white",
                description = "white color",
                category = "datatype,image",
                nodemodule = "py_color",
                nodeclass = "WhiteNode",
                inputs = (),
                outputs = (dict(name = "RGB", interface = IColor),),
                )

__all__.append("white")

red = Factory(name = "red",
                description = "red color",
                category = "datatype,image",
                nodemodule = "py_color",
                nodeclass = "RedNode",
                inputs = (),
                outputs = (dict(name = "RGB", interface = IColor),),
                )

__all__.append("red")

green = Factory(name = "green",
                description = "green color",
                category = "datatype,image",
                nodemodule = "py_color",
                nodeclass = "GreenNode",
                inputs = (),
                outputs = (dict(name = "RGB", interface = IColor),),
                )

__all__.append("green")

blue = Factory(name = "blue",
               description = "blue color",
               category = "datatype,image",
               nodemodule = "py_color",
               nodeclass = "BlueNode",
               inputs = (),
               outputs = (dict(name = "RGB", interface = IColor),),
               )

__all__.append("blue")

col_item = Factory(name = "col_item",
               description = "color from color list",
               category = "datatype,image",
               nodemodule = "py_color",
               nodeclass = "col_item",
               inputs = (dict(name = "ind", interface = IInt, value = 0),),
               outputs = (dict(name = "RGB", interface = IColor),),
               )

__all__.append("col_item")

random = Factory(name = "random",
               description = "random color",
               category = "datatype,image",
               nodemodule = "py_color",
               nodeclass = "random",
               inputs = (dict(name = "alpha", interface = IInt, value = 255),),
               outputs = (dict(name = "RGB", interface = IColor),),
               )

__all__.append("random")

rgb = Factory(name="rgb",
              description="RGB tuple",
              category="datatype,image",
              nodemodule="py_color",
              nodeclass="rgb",
              inputs=(dict(name="H", interface=IInt, value=0),
                      dict(name="S", interface=IInt, value=0),
                      dict(name="V", interface=IInt, value=0),
                      dict(name="alpha", interface=IInt, value=None),),
              outputs=(dict(name="RGB", interface = IColor),),
              )

__all__.append("rgb")

hsv = Factory(name="hsv",
              description="HSV tuple",
              category="datatype,image",
              nodemodule="py_color",
              nodeclass="hsv",
              inputs=(dict(name="RGB", interface=IColor, value=(0,0,0) ),),
              outputs=(dict(name="H", interface=IInt),
                      dict(name="S", interface=IInt),
                      dict(name="V", interface=IInt),
                      dict(name="alpha", interface=IInt),),
              )

__all__.append("hsv")

colormap = Factory(name='colormap', 
                   description='defines a color map from a range of values [I,J] to RGB', 
                   category='Visualization,image', 
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
                   category='Visualization,image', 
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
	
