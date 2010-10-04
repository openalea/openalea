# -*- python -*-
#
#       OpenAlea.Image
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

from PyQt4.QtCore import QObject,SIGNAL
from openalea.visualea.node_widget import NodeWidget
from openalea.core.observer import lock_notify
from openalea.image import PointSelection, SpatialImage, palette_names,palette_factory

class PointSelectionWidget(NodeWidget,PointSelection) :
    """
    """	
    def __init__ (self, node, parent = None) :
        
	PointSelection.__init__(self)
    	NodeWidget.__init__(self, node)

        self.notify(node, ('input_modified',))

        self.connect(self, SIGNAL("points_changed"), \
                     self.pointsChanged)

        self.window().setWindowTitle(node.get_caption())


    @lock_notify      
    def pointsChanged(self,event):
        """ update points """
        print "update points"
        pts = self.get_points()
        self.node.set_input(2, pts)
        self.node.set_output(1, pts)


    def notify(self, sender, event):
        """ Notification sent by node """
        if event[0] == 'caption_modified':
            self.window().setWindowTitle(event[1])
            
        if event[0] == 'input_modified' :
            image = self.node.get_input(0)
            if image is not None :
                if image.ndim == 2:
                    image = image.reshape(image.shape + (1,))
                if not isinstance(image,SpatialImage):
                    image = SpatialImage(image)
                self.set_palette(palette_factory("grayscale",image.max() ))
                self.set_image(image)

            points = self.node.get_input(1)
            self.node.set_input(2, points)
            if points is not None:
                self.set_points(points)
