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

        def __call__(self, mainwindow):
            # Write your code here
            pass

        def instance(self):
            # Write your code here
            pass


To avoid to rewrite all plugins from scratch, you can derivate your plugin from
:class:`~openalea.oalab.plugins.applets.PluginApplet` :

.. testcode::

    from openalea.oalab.plugins.applets import PluginApplet
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

        def __call__(self, mainwindow):
            # 1. Import widget and instantiate it
            # 2. Ask to mainwindow to place it
            # 3. Fill menus, actions, toolbars, ...

            # 1.
            from mypackage import MyApplet
            self._applet = MyApplet()

            # 2
            mainwindow.add_applet(self._applet, self.alias, area='inputs')

            # 3.
            if self._applet.actions():
                for action in self._applet.actions():
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
        Optionnal, common to all applets
        """
        pass



class IPluginApplet(object):
    """
    Graphical component displayed in main window.
    Component must respect :class:`~openalea.oalab.plugins.applet.IApplet` interface.
    """

    name = 'AppletName'
    alias = 'Applet alias'

    def __call__(self, mainwindow):
        """
        Load and instantiate graphical component that actually provide feature.
        Then, place it in mainwindow (QMainWindow).
        """

    def instance(self):
        """
        returns widget instance if plugin has been called, else None.

        .. code-block :: python

            return self._applet

        """


