# -*- python -*-
#
#       OpenAlea.StdLib
#
#       Copyright 2006 - 2008 INRIA - CIRAD - INRA  
#
#       File author(s): Da SILVA David <david.da_silva@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#

"""declaration of pix interface and its widget"""

__license__ = "Cecill-C"
__revision__ = " $Id$"

from openalea.image.interface import IPix, IImageMode
from openalea.visualea.gui_catalog import IEnumStrWidget
from openalea.visualea.node_widget import NodeWidget
from openalea.core.metaclass import make_metaclass
from openalea.core.interface import IInterfaceWidget


#from PyQt4 import QtGui, QtCore
#from PyQt4.QtGui import QLabel, QPixmap
from PyQt4.QtGui import QPixmap


from ImageQt import ImageQt
#import Image
from view import PixView



class IImageModeWidget (IEnumStrWidget) :
    """
    widget for modes
    """
    __interface__ = IImageMode
    __metaclass__ = make_metaclass()
    def __init__ (self, node, parent, parameter_str, interface) :
        IEnumStrWidget.__init__(self,node,parent,parameter_str,interface)



class IPixWidget(IInterfaceWidget, PixView):
    """
    Float spin box widget
    """
 
    # Associate widget with the IFloat interface
    __interface__ = IPix
    __metaclass__ = make_metaclass()
 
    def __init__(self, node, parent, parameter_str, interface):
        """
        @param parameter_str : the parameter key the widget is associated to
        @param interface : instance of interface object
        """
        PixView.__init__(self, parent)
        IInterfaceWidget.__init__(self, node, parent, parameter_str, interface)

        self.parent = parent
        self.notify(node, None)
        #self.connect(self.spin, QtCore.SIGNAL("valueChanged(double)"), self.valueChanged)

    def update_state(self):
        """ Enable/Disable widget function """
        pass
 
    def notify(self, sender, event):
        """ Notification sent by node """
        img = self.node.get_input(self.param_str)
        img_pil = img.copy()
        img_pil.thumbnail((100, 100))
        if img_pil != None:
            if img_pil.mode in ("RGB", "RGBA", "L"):
                img = ImageQt(img_pil)
            else :
                img = ImageQt(img.convert("RGBA"))
            pix = QPixmap.fromImage(img)
            self.set_image(pix)
            self.set_scalable(False)
        else :
            pix = QPixmap()
            self.set_image(pix)


            
class PixVisu(PixView, NodeWidget):

    def __init__(self, node, parent):
        PixView.__init__(self, parent)
        NodeWidget. __init__(self, node)
        self.parent = parent
        self.notify(node, None)

    def notify(self, sender, event):
        """ Notification sent by node """
        img_pil = self.node.get_input(0)
        if img_pil != None:
            if img_pil.mode in ("RGB", "RGBA"):
                img = ImageQt(img_pil)
            else :
                img = ImageQt(img_pil.convert("RGBA"))
            pix = QPixmap.fromImage(img)
            self.set_image(pix)
        else :
            pix = QPixmap()
            self.set_image(pix)


    #def resizeEvent(self, event):
    #  print "resized", event
##### end of declaration of pix interface and its widget ###########
