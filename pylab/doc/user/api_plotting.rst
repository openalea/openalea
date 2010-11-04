


2D Plotting nodes
#####################

.. contents::
.. moduleauthor:: Thomas Cokelaer
.. currentmodule:: openalea.pylab_plotting_wralea.py_pylab


Overview
========

VisuAlea nodes related to pylab 2D-plotting functionalities are available within
this module :mod:`openalea.pylab_plotting_wralea.py_pylab`. They are all based
upon the base class :class:`~openalea.pylab_plotting_wralea.py_pylab.Plotting`
that provides a common interface.

In addition, plots related to curves (plot, semilogx, csd, ...) have common x-y inputs
and curves can be customised in the same way. So, we derived them from a common
class called :mod:`openalea.pylab_plotting_wralea.py_pylab.PlotxyInterface`.

In order to tune the curves, matplotlib provides many parameters. In the visual
programming environment, VisuAlea, this implies far too many connectors. Therefore,
based on matplotlib, we prefered to provide a dictionary called `Line2D` as a special node
to set the lines parameters.

Base classes
-------------
.. autosummary::

    Plotting
    PlotxyInterface

Special Line2D node
---------------------

This node converts a x and y arrays into a fully customisable object.

.. autosummary::

    PyLabLine2D

Plots where x and y are 1-D arrays or Line2D objects
----------------------------------------------------


.. autosummary::

    PyLabAcorr
    PyLabBoxPlot
    PyLabCLabel
    PyLabCohere
    PyLabColorBar
    PyLabContour
    PyLabCsd
    PyLabErrorBar
    PyLabFill
    PyLabFillBetween
    PyLabHexBin
    PyLabHist
    PyLabImshow
    PyLabLogLog
    PyLabPcolor
    PyLabPie
    PyLabPlot
    PyLabPolar
    PyLabPsd
    PyLabQuiver
    PyLabScatter
    PyLabSemiLogx
    PyLabSemiLogy
    PyLabSpecgram
    PyLabStem
    PyLabStep
    PyLabXcorr



Api
===

.. automodule:: openalea.pylab_plotting_wralea.py_pylab
    :members:
    :undoc-members:
    :synopsis: 2D plotting nodes



