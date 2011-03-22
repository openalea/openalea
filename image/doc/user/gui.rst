GUI Package
###########

Display images
==============
:class:`openalea.image.gui.display` can be used for displaying a matrix as an image.

.. code-block:: python
    :linenos:
    
    from openalea.image import display
    from PyQt4 import QtGui
    app = QtGui.QApplication([])
    w1 = display(im)


.. image:: ./images/lena.png

In VisuAlea, the same function exits in the package :class:`openalea.image.gui`. Let us drag and drop the node :class:`~openalea.display` in the workspace.

.. dataflow:: openalea.image.demo display


Point Selection Tool
====================

:class:`openalea.image.gui.point_selection` is a tool that enables you to select points in an images.

.. code-block:: python
    :linenos:

    from openalea.image import point_selection
    from PyQt4 import QtGui
    app = QtGui.QApplication([])

    ps1 = point_selection(im1)

.. image:: ./images/point_selection.png
    :width: 35%

It is possible to load any points from a txt file and use them.

.. code-block:: python
    :linenos:

    import numpy as np
    pts1 = np.loadtxt("pts1.txt")
    ps1.set_points(pts1)

The following points can be get with :class:`openalea.gui.point_selection.get_points()` and save to .txt file with :class:`numpy.savetxt`.

.. code-block:: python
    :linenos:
    
    pts1 = ps1.get_points()
    np.savetxt("pts1.txt",pts1)
