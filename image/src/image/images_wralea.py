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
import ImageQt
from PyQt4 import QtGui, QtCore
 
class IPix(IInterface):
    """ Image interface """
    __metaclass__ = IInterfaceMetaClass
 
    # interface methods

class IPixWidget(IInterfaceWidget, QtGui.QLabel):
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
        QtGui.QLabel.__init__(self, parent)
        IInterfaceWidget.__init__(self, node, parent, parameter_str, interface)

        self.parent = parent
        self.setScaledContents(True)
        self.notify(node,None)
        #self.connect(self.spin, QtCore.SIGNAL("valueChanged(double)"), self.valueChanged)
        self.resize(400,400)

    def update_state(self):
        """ Enable/Disable widget function """
        pass
 
    def notify(self, sender, event):
        """ Notification sent by node """
        img_pil = self.node.get_input(self.param_str)
        if img_pil != None:
          img = QtGui.QPixmap.fromImage(ImageQt.ImageQt(img_pil))

        if( img_pil == None or img.isNull() ):
            self.resize(200,50)
            #self.setMinimumSize(200,50)
            self.setText('No Image to display')
        else:
            #self.setMinimumSize(img.size())
            s = img.size()
            self.setPixmap(img)
            self.parent.setMinimumSize(s)
            self.resize(s)
            #QtGui.QWidget.resize(self,img.size())
            #QtGui.QWidget.update(self)

    #def resizeEvent(self, event):
    #  print "resized", event
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

    nf = Factory( name="rotate image", 
                  description="Direct rotation of an image", 
                  category="Images", 
                  nodemodule="images",
                  nodeclass="rotate",

                  inputs=(dict(name="Image", interface=IPix,),
                          dict(name="Angle", interface=IFloat(min=0, max=359), value = 90),
                          dict(name="Clockwise", interface=IBool, value=False),
                        ),
                  outputs=(dict(name="Image", interface=IPix,),),
                  )


    package.add_factory( nf )

    nf = Factory( name="Perspective", 
                  description="Perspective transformation", 
                  category="Images", 
                  nodemodule="images",
                  nodeclass="perspectiveTransform",

                  inputs=(dict(name="Image", interface=IPix,),),
                  outputs=(dict(name="Image", interface=IPix,),),
                  )
    
    package.add_factory( nf )





###### end nodes definitions ###############

    pkg_manager.add_package(package)
