The Plotting nodes
##################

.. contents::
.. sectionauthor:: Thomas Cokelaer
.. moduleauthor:: Thomas Cokelaer
.. currentmodule:: openalea.pylab_nodes_wralea.py_pylab


Overview
========

All standard pylab plotting functionalities are available within the module :mod:`openalea.pylab_nodes_wralea.py_pylab`. They 
are all based upon the base class :class:`~openalea.pylab_nodes_wralea.py_pylab.Plotting` that provides common connectors
such as the grid button, the xlabel, the title and so on. Then, each plotting functions has its own connectors such as an 
`x` connector for the x-data, a `marker` connector and so on. Some plotting functions are specialised. This is the case of 
:class:`PyLabPsd`, :class:`PyLabCsd` and :class:`PyLabSpecgram` that inherits from the base class :class:`PsdInterface`. Another type
of plotting functions are those that accepts x and y data sets such as :class:`PyLabPlot`, :class:`PyLabLogLog` that inherits from 
:class:`PlotxyInterface`. 


Most of the classes uses the :class:`Colors`, :class:`Markers` and :class:`LineStyles` classes that are just a dictionary or list to ease
management of the line's style.

Here is a general overview of the relation between classes.

.. inheritance-diagram:: openalea.pylab_nodes_wralea.py_pylab
    :parts: 1

This package also provides a node to create random data :class:`PyLabRandom` that is implemented for test purpose. It does not plot anything but returns a uniformly distributed data set.



Base classes
============
.. autosummary::

    Plotting
    PlotxyInterface
    PsdInterface

Special Line2D node
===================

This node converts a x and y arrays into a fully customisable object.

.. autosummary::

    PyLabLine2D

Plots where x and y are 1-D arrays
==================================


=================================== ====================================
=================================== ====================================
:class:`PyLabErrorBar`              VisuAlea version of pylab.
:class:`PyLabFill`                  VisuAlea version of pylab.
:class:`PyLabFillBetween`           VisuAlea version of pylab.
:class:`PyLabHist`                  VisuAlea version of pylab.
:class:`PyLabLogLog`                VisuAlea version of pylab.
:class:`PyLabPlot`                  VisuAlea version of pylab.
:class:`PyLabScatter`               VisuAlea version of pylab.
:class:`PyLabSemiLogx`              VisuAlea version of pylab.
:class:`PyLabSemiLogy`              VisuAlea version of pylab.
:class:`PyLabStem`                  VisuAlea version of pylab.
:class:`PyLabStep`                  VisuAlea version of pylab.
:class:`PyLabBoxPlot`               VisuAlea version of pylab.
:class:`PyLabAcorr`                 VisuAlea version of pylab.
:class:`PyLabLine2D`                VisuAlea version of pylab.
:class:`PyLabPolar`                 VisuAlea version of pylab.
:class:`PyLabPie`                   VisuAlea version of pylab.
:class:`PyLabCohere`                VisuAlea version of pylab.
:class:`PyLabHexBin`                VisuAlea version of pylab.
:class:`PyLabContour`               VisuAlea version of pylab.
:class:`PyLabCLabel`                VisuAlea version of pylab.
:class:`PyLabPcolor`                VisuAlea version of pylab.
:class:`PyLabQuiver`                VisuAlea version of pylab.
:class:`PyLabImshow`                VisuAlea version of pylab.
=================================== ====================================

Power spectral densities related
================================

.. autosummary::

    PyLabCsd
    PyLabPsd
    PyLabSpecgram


Api 
===

.. automodule:: openalea.pylab_nodes_wralea.py_pylab
    :members:
    :undoc-members:
    :synopsis: plotting nodes

.. autoclass:: openalea.pylab_nodes_wralea.py_pylab.PyLabHist



..     :show-inheritance:
