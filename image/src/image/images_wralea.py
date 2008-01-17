# -*- python -*-
#
#       OpenAlea.Core.Library: OpenAlea Core Library module
#
#       Copyright 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Da SILVA David <david.da_silva@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#


from openalea.core import *


##### declaration of pix interface and its widget ###########

from openalea.core.interface import *
from openalea.visualea.gui_catalog import IEnumStrWidget
import ImageQt
import Image
from PyQt4 import QtGui, QtCore
from view import PixView

class IImageMode (IEnumStr) :
    """
    interface for differents mode of an image
    """
    def __init__ (self) :
        IEnumStr.__init__(self, ["RGB","RGBA"])

class IImageModeWidget (IEnumStrWidget) :
    """
    widget for modes
    """
    __interface__ = IImageMode
    __metaclass__ = make_metaclass()
    def __init__ (self, node, parent, parameter_str, interface) :
        IEnumStrWidget.__init__(self,node,parent,parameter_str,interface)

class IColor (IInterface) :
    """
    interface for image color
    a tuple RGBA or a single value
    """
    __metaclass__ = IInterfaceMetaClass

class IPix(IInterface):
    """ Image interface """
    __metaclass__ = IInterfaceMetaClass
 
    # interface methods

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
        self.notify(node,None)
        #self.connect(self.spin, QtCore.SIGNAL("valueChanged(double)"), self.valueChanged)

    def update_state(self):
        """ Enable/Disable widget function """
        pass
 
    def notify(self, sender, event):
        """ Notification sent by node """
        img_pil = self.node.get_input(self.param_str)
        if img_pil != None:
            img = self.set_image(ImageQt.ImageQt(img_pil))
        else :
            self.set_image(None)

    #def resizeEvent(self, event):
    #  print "resized", event
##### end of declaration of pix interface and its widget ###########

import basics_factory
import data_access_factory
import geom_transfo_factory
import image_transfo_factory


def register_packages(pkg_manager):
    
    metainfo={ 'version' : '0.0.1',
               'license' : 'CECILL-C',
               'authors' : 'D. Da Silva',
               'institutes' : 'INRIA/CIRAD',
               'description' : 'PIL wrapping and utils module.',
               'url' : 'http://www.PIL.org'
               }
    
    
    package = Package("image", metainfo)
    basics_factory.define_factory(package)
    data_access_factory.define_factory(package)
    geom_transfo_factory.define_factory(package)
    image_transfo_factory.define_factory(package)

    pkg_manager.add_package(package)
