.. _pylab_user:

.. topic:: in progress

OpenAlea.Pylab User Guide
##########################


.. contents::

Introduction
============

This package is a pure VisuAlea package that provides a graphical interface to `Matplotlib <http://matplotlib.sourceforge.net/index.html>`_ , which is a python package for 2D and 3D plottings. When combined with Numpy and Scipy packages, Matplotlib becomes a great tool for analysing and visualing scientific data. Due to the versatile capabilities of Matplotlib with many options and arguments, it may sometimes be quite cumbersome to know what are the possible tunable and customisable arguments -- despite the great documentation that the authors put online. This weahlt  motivated us in developing a visual interface of Matplotlib within VisuAlea.

.. note:: this package is called *openalea.pylab* instead of *openalea.matplotlib* so as to be as close as possible to the python commands that you would use in a Python environment. Indeed, if you were to use the plot command of matplotlib, you would type

:: 

    from pylab import plot, show
    plot(x,y)
    show()


Here below, you will find a tutorial that allows you to start with the `OpenAlea.Pylab`

.. warning:: because OpenAlea.Pylab is a pure VisuAlea package, you cannot import it within Python using *import openalea.pylab*. Yet, you may access to the class defined inside the __wralea__ files using e.g., *import openalea.pylab_nodes_text_wralea.py_pylab*. See the refrence guide for the filenames available.

Tutorials
=========

This tutorial presents some of the nodes implemented in the **openalea.pylab** package, which provides an interface to pylab functionalities within VisuAlea.

We do not present all the nodes but only the most relevant ones so as to describe the logic that has been used.

All public nodes can be found within VisuAlea in the Package Manager by browsing the OpenAlea directory, look for pylab sub directory


2D Plotting
-----------

First example
~~~~~~~~~~~~~
Let us start with a simple 2D plot that would be done as follows in pylab::

    from pylab import random
    from pylab import plot, show
    x = random(100)
    y = random(100)
    plot(x,y)
    show()

In VisuAlea, you first need to create the random data using the :class:`~openalea.pylab_nodes_wralea.py_pylab.PyLabRandom` node. Let us drag and drop two of those nodes in the workspace (see :ref:`Fig 1 <Fig_1>`) . Then, you need to select :class:`~openalea.pylab_nodes_wralea.py_pylab.PyLabPlot`. This node has many connectors and so will have all plotting nodes. We will explain why in a moment. For now, just keep in mind that the connectors roughly follows the same options as the original pylab.plot function. For instance, if you look at the documentation of pylab.plot you will get someting like::

    Plot lines and/or markers to the
    :class:`~matplotlib.axes.Axes`.  *args* is a variable length
    argument, allowing for multiple *x*, *y* pairs with an
    optional format string.  For example, each of the following is
    legal::

        plot(x, y)         # plot x and y using default line style and color
        plot(x, y, 'bo')   # plot x and y using blue circle markers
        plot(y)            # plot y using x as index array 0..N-1
        plot(y, 'r+')      # ditto, but with red plusses

Well, in VisuAlea the first connector of :class:`PyLabPlot` node is `x` and the second connector is `y`. As simple as that.

.. warning:: the `x` and `y` objects must have the same length.
.. warning:: if after connecting the `x` and `y` objects you decided to remove the `y` object, you will have to *reload* the *plot* node to reset the `y` data.

Now, it is time to run the dataflow. Press Ctrl+R or right click on the :class:`PyLabPlot` node and select `run`.

By default, the marker are blue circles as shown in :ref:`Fig 1 <Fig_1>`, and the linestyle is solid. To remove the lines between each point double click on the Plot node and select nothing in place of solid. Similarly if you want to change the color or marker.

.. _Fig_1:
.. figure:: plotxy_1.png

   **Figure 1: simple xy-plot in VisuAlea**

Now the first questions arise:

    1. What kind of options do I have ? What shall I do if I want to increase the size of the marker 
    2. What about xlabel and title ? (see :ref:`Enhance the layout <sec_text>` section)
    3. What if I have multiple xy data, or if I have several y-data that shares the same x-data ? (equivalent in pylab to `plot(x, y1, x, y2)`) 


Playing with the options/connectors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you right-click on the :class:`PyLabPlot` node a pop-up window appears letting you introspect the connectors. In the case of the PyLabPlot node, the following window pops up:

=============== ===============================
=============== ===============================
                .. figure:: connectors.png
                   :width: 30%
=============== ===============================

multiple data set
~~~~~~~~~~~~~~~~~

Other examples scatter, hexbin, ...
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _sec_text:
Enhance the layout
------------------

:mod:`patches <openalea.pylab_text_wralea.py_pylab>`

As seen in the previous examples, there are many connectors in each Plotting nodes. We've also seen that there are two kind of connectors. On one hand (left side), you will find the connectors dedicated to the plotting node itself. Those that are in the docstring of the original pylab function. On the other hand (right side), you will find connectors dedicated to the customised the layout of an Axes such as adding an xlabel, a title, specify the figure number and so on. 

The nodes described here correspond to the second category. Each of these connectors may be replace by a specialised nodes. For instance, if you want to add a red bold xlabel you would proceed as follows:




Adding patches
--------------
Here, we look at a particular set of nodes that can be found in :mod:`patches <openalea.pylab_patches_wralea.py_pylab>`

3D plotting
-----------


Gallery
=======

This section should put VisuAlea dataflow and the resulting pylab figure.


