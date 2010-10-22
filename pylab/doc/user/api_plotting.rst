The 2D Plotting nodes
#####################

.. contents::
.. sectionauthor:: Thomas Cokelaer
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


=================================== ====================================
=================================== ====================================
:class:`PyLabAcorr`                 VisuAlea version of pylab.acorr
:class:`PyLabBoxPlot`               VisuAlea version of pylab.boxplot
:class:`PyLabCLabel`                VisuAlea version of pylab.clabel
:class:`PyLabCohere`                VisuAlea version of pylab.cohere
:class:`PyLabColorBar`              VisuAlea version of pylab.colorbar
:class:`PyLabContour`               VisuAlea version of pylab.contour
:class:`PyLabCsd`                   VisuAlea version of pylab.cohere
:class:`PyLabErrorBar`              VisuAlea version of pylab.errorbar
:class:`PyLabFill`                  VisuAlea version of pylab.fill
:class:`PyLabFillBetween`           VisuAlea version of pylab.fillbetween
:class:`PyLabHexBin`                VisuAlea version of pylab.hexbin
:class:`PyLabHist`                  VisuAlea version of pylab.hist
:class:`PyLabImshow`                VisuAlea version of pylab.imshow
:class:`PyLabLogLog`                VisuAlea version of pylab.loglog
:class:`PyLabPcolor`                VisuAlea version of pylab.pcolor
:class:`PyLabPie`                   VisuAlea version of pylab.pie
:class:`PyLabPlot`                  VisuAlea version of pylab.plot
:class:`PyLabPolar`                 VisuAlea version of pylab.polar
:class:`PyLabPsd`                   VisuAlea version of pylab.cohere
:class:`PyLabQuiver`                VisuAlea version of pylab.quiver
:class:`PyLabScatter`               VisuAlea version of pylab.scatter
:class:`PyLabSemiLogx`              VisuAlea version of pylab.semilogx
:class:`PyLabSemiLogy`              VisuAlea version of pylab.semilogy
:class:`PyLabSpecgram`              VisuAlea version of pylab.specgram
:class:`PyLabStem`                  VisuAlea version of pylab.stem
:class:`PyLabStep`                  VisuAlea version of pylab.step
:class:`PyLabXcorr`                 VisuAlea version of pylab.xcorr
=================================== ====================================



Api 
===

.. automodule:: openalea.pylab_plotting_wralea.py_pylab
    :members:
    :undoc-members:
    :synopsis: 2D plotting nodes



