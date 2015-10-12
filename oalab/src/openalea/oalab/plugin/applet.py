"""
=======
Applets
=======

Overview
========

.. note::

    To define an applet plugin, you must
      #. write an AppletPlugin class that respects IPluginApplet interface (see below)
      #. add it to group :dfn:`oalab.applet`

1. Copy paste this code and fill it with right names and instructions.
(replace all xyz, respecting case, with your applet name).
For example Xyz -> HelpApplet


.. testcode::

    class PluginXyz(object):

        name = 'Xyz'
        label = 'Xyz'
        modulename = 'mypackage.myapplet'
        objectname = 'MyApplet'

2. Once this class has been written, just register it in the setup.py file of
your python package.

.. testcode::

    entry_points={
        'oalab.applet': [
            'oalab.applet/mypackage = mypackage.plugin.builtin.applet',
        ],
        }



With **mypackage.plugin.builtin.applet** python module path (equivalent to 'mypackage/plugin/builtin/applet.py').


Details
=======


"""
from openalea.core.interface import IInterface


class IApplet(IInterface):

    """
    Autonomous Graphical component
    """

    def initialize(self):
        """
        Optional method, called after instantiation
        """

    def actions(self):
        """
        Optional: list of all actions available for this applet
        See original QtGui.QWidget.actions method.

        Example::

            # instructions written in constructor
            action_new = QtGui.QAction('New', self)
            self.addAction(action_new)
        """
        pass

    def toolbars(self):
        """
        Optional: return a list of QToolBar
        """

    def global_toolbar_actions(self):
        """
        Optional: list of actions to use in main toolbar.
        See toolbar

        ..warning::

            these actions must have a global effect as they are added only one time in application.
            For example, if you add two time applet "Viewer3D", menu_actions are added only one time.

            To get global effects, action cat ...
                - manipulate core managers directly
                - manipulate singleton
                - iter on all applets of same type and apply effect on each

            A contextual menu is also generated dynamically for current applet, see toolbar_actions, menu_actions
        """
        pass

    def toolbar_actions(self):
        """
        Optional: list of actions to use in contextual toolbar

        Example::

            def toolbar_actions(self):
                action_new = QtGui.QAction("New")
                action_open = QtGui.QAction("Open")
                action_save = QtGui.QAction("Save")

                action_run = QtGui.QAction("Run")
                action_debug = QtGui.QAction("Debug")
                menu_run = QtGui.QMenu("Run")
                menu_run.addActions([action_run, action_debug])

                actions = [
                    menu_run, # Menu syntax (generally transformed as toolbutton)
                    action_new, # Default syntax
                    {'action': action_open, 'style':0} # Dict syntax
                ]

        .. warning ::

            List syntax ["Panel", "Group", action, style] is now deprecated.
            Use dict syntax instead

        """
        pass

    def menus(self):
        """
        Optional: list of QMenu to use in main menu
        """

    def menu_actions(self):
        """
        Optional: list of QAction/QMenu to use in contextual menu
        """


class IPluginApplet(object):

    """
    Graphical component displayed in main window.
    Component must respect :class:`~openalea.oalab.plugins.applet.IApplet` interface.
    """