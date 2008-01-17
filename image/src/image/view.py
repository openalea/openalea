# -*- python -*-
# -*- coding: latin-1 -*-
#
#       basics : image package
#
#       Copyright or © or Copr. 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Da SILVA David <david.da_silva@cirad.fr>
#						Jerome Chopard <jerome.chopard@sophia.inria.fr>
#						Fernandez Romain <romain.fernandez@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#

__doc__="""
This module provide basics function to handle 2D images
"""

__license__= "Cecill-C"
__revision__=" $Id: graph.py 116 2007-02-07 17:44:59Z tyvokka $ "

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QLabel,QPixmap

class PixView (QLabel) :
    """
    minimalist widget to display an image
    """
    def __init__ (self, parent=None, image=None) :
        QLabel.__init__(self,parent)
        self.setScaledContents(True)
        self.setAlignment(Qt.AlignCenter)
        self.set_image(image)
    
    def scalable (self) :
        return self.hasScaledContents()
    
    def set_scalable (self, scalable=True) :
        self.setScaledContents(scalable)
    
    def image (self) :
        return self.pixmap().toImage()
    
    def set_image (self, image) :
        if image is None :
            self.resize(200,50)
            self.setText("No Image to display")
        else :
            pix=QPixmap.fromImage(image)
            if (pix is None) or (pix.isNull()) :
                self.set_image(None)
            else :
                s = pix.size()
                self.setPixmap(pix)
                self.setMinimumSize(s)
                self.resize(s)
    
    def keyReleaseEvent (self, event) :
        if event.key()==Qt.Key_Escape :
            self.close()
        else :
            QLabel.keyReleaseEvent(self,event)
