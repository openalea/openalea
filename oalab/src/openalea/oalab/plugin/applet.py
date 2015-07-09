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
        alias = 'Xyz'

        def __call__(self):
            # Write your code here
            pass

        def graft(self, **kwds):
            # Write your code here
            pass


To avoid to rewrite all plugins from scratch, you can derivate your plugin from
:class:`~openalea.oalab.plugins.applets.PluginApplet` :

.. testcode::

    from openalea.core.plugin import PluginDef

    @PluginDef
    class PluginXyz(PluginApplet):
        pass

2. Once this class has been written, just register it in the setup.py file of
your python package.

.. testcode::

    entry_points={
        'oalab.applet': [
            'Xyz = mypackage.plugins:PluginXyz',
            ]
        }


With **mypackage.plugins** python module path (equivalent to 'mypackage/plugins.py') and
'PluginXyz' the class name.

Example
=======

The module called oalab.gui.help provides this help widget:

.. code-block:: python
    :filename: oalab/gui/help.py
    :linenos:

    from openalea.vpltk.qt import QtGui

    class HelpWidget(QtGui.QWidget):
        def openWeb(self, url):
            # Specific to this applet
            pass

        def actions(self):
            # optionnal, common to all applets
            pass

        def initialize(self):
            # optionnal, common to all applets
            pass

OpenAleaLab is the main application that gather all widgets.
We want to add HelpWidget in the MainWindow and allow communication between both classes.
For that purpose, we create a Plugin called HelpWidgetPlugin in helper package:

.. code-block:: python
    :filename: helper/plugins/oalab/helpwidget.py
    :linenos:

    class HelpWidgetPlugin(object):

        data = {
        # Data that describe plugin
        }

        def __call__(self):
            # Import widget and return it
            from mypackage import MyApplet
            return MyApplet

        def graft(self, **kwds):
            # 1. Ask to mainwindow to place it
            # 2. Fill menus, actions, toolbars, ...

            # 1.
                mainwindow.add_applet(applet, self.alias, area='inputs')

            # 2.
            if applet.actions():
                for action in applet.actions():
                    # Add actions in PanedMenu
                    mainwindow.menu.addBtnByAction(*action)

                    # add action in classical menu
                    pane_name, group_name, act, btn_type = action
                    mainwindow.add_action_to_existing_menu(action=act, menu_name=pane_name, sub_menu_name=group_name)

It is very important to notice that adding widget in the right area is done by
the plugin, not the application. Application does almost nothing, it is just
a container of widgets. Real application intelligence is delegated to Plugins
(placing and linking components) and components (doing real treatments).

Finally, we register this plugin in setup.py of package helper.

.. code-block:: python
    :filename: helper/setup.py
    :linenos:
    :emphasize-lines: 5,7

    setup(
        # setup instructions

        entry_points = {
            'oalab.applet':                                                  # Plugin category
                [
                'HelpWidgetPlugin = helper.plugins.oalab:HelpWidgetPlugin'   # Plugin name = path to plugin (factory)
                ]
            }
        )


Details
=======

.. autoclass:: openalea.oalab.plugins.applet.IPluginApplet
    :members: __call__, instance, name, alias

.. autoclass:: openalea.oalab.plugins.applets.PluginApplet
    :members: __call__, instance, _fill_menu

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

    name = 'AppletName'
    alias = 'Applet alias'

    def __call__(self):
        """
        Return applet class
        """
