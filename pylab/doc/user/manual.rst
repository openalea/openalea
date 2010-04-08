Tutorials
#########

This tutorial presents some of the nodes implemented in the **openalea.pylab** package, which provides an interface to pylab functionalities within VisuAlea.

We do not present all the nodes but only the most relevant ones so as to describe the logic that has been used.


Plot
=====

In order to to a simple 2D plot, create some x and y data (here the PyLabRandom node) and connect them to the first and second PyLabPlot connector. the two entries must have the same length. Then run the PyLabPlot node. By default, the marker are blue circles as shown here below, and the linestyle is solid. To remove the lines between each point double click on the Plot node and select nothin in place of solid. 

.. image:: plotxy_1.png
