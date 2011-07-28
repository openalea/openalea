# -*- python -*-
#
#       image: image manipulation
#
#       Copyright 2006 INRIA - CIRAD - INRA
#
#       File author(s): Jerome Chopard <jerome.chopard@sophia.inria.fr>
#                       Eric Moscardi <eric.moscardi@gmail.com>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#       http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#

__license__= "Cecill-C"
__revision__=" $Id: $ "

from openalea.image.all import SpatialImage, SlideViewer, palette_factory

def display (image, palette_name, title, color_index_max) :

    if not isinstance(image,SpatialImage) :
	image = SpatialImage(image)

    if image.ndim < 3 :
        image = image.reshape(image.shape + (1,))

    w = SlideViewer()

    if color_index_max is None :
	cmax = image.max()
    else :
	cmax = color_index_max

    palette = palette_factory(palette_name,cmax)
    w.set_palette(palette,palette_name)

    if image.ndim == 2:
        image = image.reshape(image.shape + (1,))

    w.set_image(image)
    w.set_title(title)

    w.show()

    return w


