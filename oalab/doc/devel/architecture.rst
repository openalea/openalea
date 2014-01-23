##################
OALab Architecture
##################


Main classes
============

Session
-------

Session is a central class. 
It is used to centralize configuration, projects and connect (allow communication) all plugins together.

PluginManager
-------------

Class use to find and load available plugins.


MainWindow
----------

Based on Qt4.QMainWindow, this class define the whole GUI.
Available widgets, look and feel, disposition of items depends on external configuration.

MainWindow knows session.

XyzApplet
---------

An applet is a functionnal standalone widget :
  - works without other applets
  - answer to a specific problematic (display 3d object, run shell command, edit text, ...)

An applet must respect :obj:`~openalea.oalab.gui.i_applet.IApplet` interface.

It's the View part in the View/Controller/Model approach.
Real treatments are done by a controller.


Main interfaces
===============

IApplet
-------


