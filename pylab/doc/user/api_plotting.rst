The 2D Plotting nodes
#####################

.. contents::
.. sectionauthor:: Thomas Cokelaer
.. moduleauthor:: Thomas Cokelaer
.. currentmodule:: openalea.pylab_plotting_wralea.py_pylab


Overview
========

VisuAlea nodes related to pylab 2D-plotting functionalities are available within 
the module :mod:`openalea.pylab_plotting_wralea.py_pylab`. They are all based 
upon the base class :class:`~openalea.pylab_plotting_wralea.py_pylab.Plotting` 
that provides a common interface:

    * first input connector is reserved to pass an input axes.
    * last output is reserved for the figure connector. 
    * first output connector is reserved to pass an output axes.
    * remaining output connectors should correspond to the output of the pylab function called.

Then, each node has its own set of connectors such as an `x` connector for the x-data, a `marker`, 
that are as close as possible to the Matplotlib API.



Base classes
============
.. autosummary::

    Plotting
    PlotxyInterface

Special Line2D node
===================

This node converts a x and y arrays into a fully customisable object.

.. autosummary::

    PyLabLine2D

Plots where x and y are 1-D arrays
==================================


=================================== ====================================
=================================== ====================================
:class:`PyLabAcorr`                 VisuAlea version of pylab.acorr
:class:`PyLabCLabel`                VisuAlea version of pylab.clabel
:class:`PyLabCohere`                VisuAlea version of pylab.cohere
:class:`PyLabContour`               VisuAlea version of pylab.contour
:class:`PyLabBoxPlot`               VisuAlea version of pylab.boxplot
:class:`PyLabErrorBar`              VisuAlea version of pylab.errorbar
:class:`PyLabFill`                  VisuAlea version of pylab.fill
:class:`PyLabFillBetween`           VisuAlea version of pylab.fillbetween
:class:`PyLabHexBin`                VisuAlea version of pylab.hexbin
:class:`PyLabHist`                  VisuAlea version of pylab.hist
:class:`PyLabImshow`                VisuAlea version of pylab.imshow
:class:`PyLabLine2D`                VisuAlea version of pylab.line2d
:class:`PyLabLogLog`                VisuAlea version of pylab.loglog
:class:`PyLabPcolor`                VisuAlea version of pylab.pcolor
:class:`PyLabPlot`                  VisuAlea version of pylab.plot
:class:`PyLabPie`                   VisuAlea version of pylab.pie
:class:`PyLabPolar`                 VisuAlea version of pylab.polar
:class:`PyLabQuiver`                VisuAlea version of pylab.quiver
:class:`PyLabScatter`               VisuAlea version of pylab.scatter
:class:`PyLabSemiLogx`              VisuAlea version of pylab.semilogx
:class:`PyLabSemiLogy`              VisuAlea version of pylab.semilogy
:class:`PyLabStem`                  VisuAlea version of pylab.stem
:class:`PyLabStep`                  VisuAlea version of pylab.step
:class:`PyLabXcorr`                 VisuAlea version of pylab.xcorr
=================================== ====================================

Power spectral densities related
================================

.. autosummary::

    PyLabCsd
    PyLabPsd
    PyLabSpecgram


Api 
===

.. automodule:: openalea.pylab_plotting_wralea.py_pylab
    :members:
    :undoc-members:
    :synopsis: 2D plotting nodes



