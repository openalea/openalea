# -*- python -*-
#
#       image: image algo
#
#       Copyright 2006 INRIA - CIRAD - INRA
#
#       File author(s): Eric Moscardi <eric.moscardi@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
"""
Test image algo
"""

__license__= "Cecill-C"
__revision__ = " $Id:  $ "

from numpy import array, random, zeros
from openalea.image.all import border,end_margin,stroke

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

def test_end_margin():
    """
    Test : end_margin
    """
    img = random.random((3,4,5))

    assert img.shape == (3,4,5)

    out = end_margin(img,1,0)
    assert out.shape == (3,4,5)

    #assert (out[0,:,:] == zeros((4,5))).all()
    assert (out[2,:,:] == zeros((4,5))).all()
    assert (out[1:2,:,:] == img[1:2,:,:]  ).all()

    out = end_margin(img,1,1)
    assert out.shape == (3,4,5)

    #assert (out[:,0,:] == zeros((3,5))).all()
    assert (out[:,3,:] == zeros((3,5))).all()
    assert (out[:,1:3,:] == img[:,1:3,:] ).all()

    out = end_margin(img,1,2)
    assert out.shape == (3,4,5)

    #assert (out[:,:,0] == zeros((3,4))).all()
    assert (out[:,:,4] == zeros((3,4))).all()
    assert (out[:,:,1:4] == img[:,:,1:4] ).all()

    out = end_margin(img,1)
    #assert (out[0,:,:] == zeros((4,5))).all()
    assert (out[2,:,:] == zeros((4,5))).all()

    #assert (out[:,0,:] == zeros((3,5))).all()
    assert (out[:,3,:] == zeros((3,5))).all()

    #assert (out[:,:,0] == zeros((3,4))).all()
    assert (out[:,:,4] == zeros((3,4))).all()

    assert (out[0:2,0:3,0:4] == img[0:2,0:3,0:4] ).all()

    try :
        out = end_margin(img,1,3)
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
