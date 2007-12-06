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
from PyQt4 import QtGui, QtCore
 
class IPix(IInterface):
    """ Image interface """
    __metaclass__ = IInterfaceMetaClass
 
    # interface methods

class IPixWidget(IInterfaceWidget, QtGui.QWidget):
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
        QtGui.QWidget.__init__(self, parent)
        IInterfaceWidget.__init__(self, node, parent, parameter_str, interface)

        self.img_label = QtGui.QLabel(self)

        
        self.notify(node,None)
        #self.connect(self.spin, QtCore.SIGNAL("valueChanged(double)"), self.valueChanged)
 
    def update_state(self):
        """ Enable/Disable widget function """
        pass
 
    def notify(self, sender, event):
        """ Notification sent by node """
        img = self.node.get_input(self.param_str)
        if( img == None or img.isNull() ):
            self.img_label.resize(200,50)
            self.setMinimumSize(200,50)
            self.img_label.setText('No Image to display')
        else:
            self.img_label.resize(img.size())
            self.setMinimumSize(img.size())
            self.img_label.setPixmap(img)
            QtGui.QWidget.resize(self,img.size())
            QtGui.QWidget.update(self)

##### end of declaration of pix interface and its widget ###########



def register_packages(pkg_manager):
    
    metainfo={ 'version' : '0.0.1',
               'license' : 'CECILL-C',
               'authors' : 'D. Da Silva',
               'institutes' : 'INRIA/CIRAD',
               'description' : 'PIL wrapping and utils module.',
               'url' : 'http://www.PIL.org'
               }
    
    
    package = Package("pil", metainfo)
    
    
###### begin nodes definitions #############


    nf = Factory( name="Image size",
                  description="Defines the size of generated image",
                  category="Images",
                  nodemodule="images",
                  nodeclass= "image_size",
                  inputs= ( dict( name = "Width", interface=IInt(min=10), value = 300),
                            dict( name = "Heigth", interface=IInt(min=10), value = 300),
                          ),
                  outputs=( dict( name = "Image size", interface = ISequence),
                          ),
                  )

    package.add_factory( nf )


    nf = Factory( name="PIL to Qt",
                  description="Convert PIL image to Qt pixmap",
                  category="Images",
                  nodemodule="images",
                  nodeclass= "PIL2Qt",
                  inputs= ( dict( name = "PIL Image", interface=None,),
                          ),
                  outputs=( dict( name = "Qt Image", interface = IPix,),
                          ),
                  )

    package.add_factory( nf )


    nf = Factory( name="Pix view", 
                  description="Display image", 
                  category="Images", 
                  nodemodule="images",
                  nodeclass="Pix",

                  inputs=(dict(name="Image", interface=IPix,),),
                  outputs=(dict(name="Image", interface=IPix,),),
                  )
    
    package.add_factory( nf )

    nf = Factory( name="load image", 
                  description="Load an image from a file", 
                  category="Images", 
                  nodemodule="images",
                  nodeclass="loadimage",

                  inputs=(dict(name="Filename", interface=IFileStr,),),
                  outputs=(dict(name="Image", interface=IPix,),),
                  )


    package.add_factory( nf )



###### end nodes definitions ###############

    pkg_manager.add_package(package)
