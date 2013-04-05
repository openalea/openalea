# -*- python -*-
#
#       image: image morpho
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

import numpy as np
from openalea.vpltk.qt import QtGui
import matplotlib.pyplot as plt

from openalea.image.all import component_labeling

qapp = QtGui.QApplication.instance()

def test_component_labeling_with_threshold_image():
    """
    Test component_labeling :

    :Parameters :
    - `threshold image`
    """
    try:
        img = np.load('labels.npy')
    except:
        img = np.load('test/labels.npy')
    assert img.shape == (1024, 1344)

    thresh_im = np.where(img < 127, False, True)
    out,nlabels = component_labeling(thresh_im)
    assert nlabels == 18

    if qapp:
        plt.figure()
        plt.subplot(121)
        plt.imshow(img, cmap=plt.cm.gray)
        plt.title('reference image')
        plt.subplot(122)
        plt.imshow(out, cmap=plt.cm.gray)
        plt.title('labeled image')
        plt.show()

def test_component_labeling_with_threshold():
    """
    Test component_labeling :

    :Parameters :
    - `threshold`
    """

    try:
        img = np.load('labels.npy')
    except:
        img = np.load('test/labels.npy')
    assert img.shape == (1024, 1344)

    out,nlabels = component_labeling(img, threshold=127)
    assert nlabels == 18

    if qapp:
        plt.figure()
        plt.subplot(121)
        plt.imshow(img, cmap=plt.cm.gray)
        plt.title('reference image')
        plt.subplot(122)
        plt.imshow(out, cmap=plt.cm.gray)
        plt.title('labeled image')
        plt.show()

def test_component_labeling_with_number_labels():
    """
    Test component_labeling :

    :Parameters :
    - `number_labels`
    """
    try:
        img = np.load('labels.npy')
    except:
        img = np.load('test/labels.npy')
    assert img.shape == (1024, 1344)

    out,nlabels = component_labeling(img, threshold=127, number_labels=3)
    assert nlabels == 3

    if qapp:
        plt.figure()
        plt.subplot(121)
        plt.imshow(img, cmap=plt.cm.gray)
        plt.title('reference image')
        plt.subplot(122)
        plt.imshow(out, cmap=plt.cm.gray)
        plt.title('labeled image')
        plt.show()
