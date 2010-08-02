# -*- python -*-
#
#       image: image manipulation GUI
#
#       Copyright 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Jerome Chopard <jerome.chopard@sophia.inria.fr>
#                       Eric Moscardi <eric.moscardi@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
"""
Test frame manipulator
"""

__license__= "Cecill-C"
__revision__ = " $Id: __init__.py 2245 2010-02-08 17:11:34Z cokelaer $ "

from numpy import array, random, zeros
from PyQt4.QtGui import QApplication,QLabel
from openalea.image import (rainbow,grayscale,bw,
                            apply_mask,saturate,high_level,color_select,border,margin,stroke)
from openalea.image.gui import to_pix

#create image
data = array(range(30000) ).reshape( (100,300) )

pal = rainbow(30000)

img = pal[data]

img[:,:150,:] = img[:,:150,:] / 10

#saturate
sat = saturate(img)

#high_level
mask = high_level(img,100)
pal = bw()
hg = pal[mask * 1]
hgimg = apply_mask(img,mask)

#color_select
mask = color_select(img,(0,255,0),10)
sel = pal[mask * 1]
selimg = apply_mask(img,mask)

#display result
qapp = QApplication([])

w_list = []
y = 0
for im,name in [(img,"img"),
                (sat,"sat"),
                (hgimg,"hgimg"),(hg,"hg"),
                (selimg,"selimg"),(sel,"sel")] :
	w = QLabel()
	w.setWindowTitle(name)
	w.setPixmap(to_pix(im) )
	w.show()
	w.move(0,y)
	y += w.frameRect().height()
	w_list.append(w)

qapp.exec_()

def test_border():
    """Test : border 
    """

    img = random.random((1,2,3))
    
    assert img.shape == (1,2,3)

    out = border(img)
    assert out.shape == (1,2,3)
    assert (out == img).all()

    out = border(img, (0,0,1))
    assert out.shape == (1,2,4)
    assert (out[:,:,0] == array([0,0]) ).all()
    assert (out[:,:,1:] == img).all()

    out = border(img, (0,1,0))
    assert out.shape == (1,3,3)
    assert (out[:,0,:] == array([0,0,0]) ).all()
    assert (out[:,1:,:] == img).all()
    
    out = border(img, (1,0,0))
    assert out.shape == (2,2,3)
    assert (out[0,:,:] == array([[0,0,0],[0,0,0]]) ).all()
    assert (out[1,:,:] == img).all()

    out = border(img, (0,0,1), (0,0,1))
    assert out.shape == (1,2,5)
    assert (out[:,:,0] == array([0,0]) ).all()
    assert (out[:,:,4] == array([0,0]) ).all()
    assert (out[:,:,1:4] == img).all()

    out = border(img, (0,1,0), (0,1,0))
    assert out.shape == (1,4,3)
    assert (out[:,0,:] == array([0,0,0]) ).all()
    assert (out[:,3,:] == array([0,0,0]) ).all()
    assert (out[:,1:3,:] == img).all()
    
    out = border(img, (1,0,0), (1,0,0))
    assert out.shape == (3,2,3)
    assert (out[0,:,:] == array([[0,0,0],[0,0,0]]) ).all()
    assert (out[2,:,:] == array([[0,0,0],[0,0,0]]) ).all()
    assert (out[1,:,:] == img).all()

def test_margin():
    """
    Test : margin
    """
    img = random.random((3,4,5))
    
    assert img.shape == (3,4,5)

    out = margin(img,1,0)
    assert out.shape == (3,4,5)

    assert (out[0,:,:] == zeros((4,5))).all()
    assert (out[2,:,:] == zeros((4,5))).all()
    assert (out[1:2,:,:] == img[1:2,:,:]  ).all()

    out = margin(img,1,1)
    assert out.shape == (3,4,5)

    assert (out[:,0,:] == zeros((3,5))).all()
    assert (out[:,3,:] == zeros((3,5))).all()
    assert (out[:,1:3,:] == img[:,1:3,:] ).all()

    out = margin(img,1,2)
    assert out.shape == (3,4,5)

    assert (out[:,:,0] == zeros((3,4))).all()
    assert (out[:,:,4] == zeros((3,4))).all()
    assert (out[:,:,1:4] == img[:,:,1:4] ).all()

    out = margin(img,1)
    assert (out[0,:,:] == zeros((4,5))).all()
    assert (out[2,:,:] == zeros((4,5))).all()

    assert (out[:,0,:] == zeros((3,5))).all()
    assert (out[:,3,:] == zeros((3,5))).all()

    assert (out[:,:,0] == zeros((3,4))).all()
    assert (out[:,:,4] == zeros((3,4))).all()

    assert (out[1:2,1:3,1:4] == img[1:2,1:3,1:4] ).all()

    try :
        out = margin(img,1,3)
        assert False
    except :
        assert True
    

def test_input_stroke():
    """
    Test : output stroke  
    """

    img = random.random((3,4,5))
    
    assert img.shape == (3,4,5)

    out = stroke(img,1)
    assert out.shape == (3,4,5)

    assert (out[0,:,:] == zeros((4,5))).all()
    assert (out[2,:,:] == zeros((4,5))).all()

    assert (out[:,0,:] == zeros((3,5))).all()
    assert (out[:,3,:] == zeros((3,5))).all()

    assert (out[:,:,0] == zeros((3,4))).all()
    assert (out[:,:,4] == zeros((3,4))).all()

    assert (out[1:2,1:3,1:4] == img[1:2,1:3,1:4] ).all()

def test_output_stroke():
    """
    Test : output stroke  
    """

    img = random.random((3,4,5))
    
    assert img.shape == (3,4,5)

    out = stroke(img,1,True)
    assert out.shape == (5,6,7)

    assert (out[0,:,:] == zeros((6,7))).all()
    assert (out[4,:,:] == zeros((6,7))).all()

    assert (out[:,0,:] == zeros((5,7))).all()
    assert (out[:,5,:] == zeros((5,7))).all()

    assert (out[:,:,0] == zeros((5,6))).all()
    assert (out[:,:,6] == zeros((5,6))).all()

    assert (out[1:4,1:5,1:6] == img).all()
