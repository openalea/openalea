"""
To define a new extension for OpenAleaLab (ex: MyApplet) corresponding to a category (ex: oalab.applet) , you must
  #. write a Plugin class (ex: "PluginMyApplet") that respects a special "IPlugin" interface (ex: IPluginApplet)
  #. write or use a class that actually does the job (ex: MyApplet) that respects a special "interface" (ex: IApplet)
  #. add it to the right "entry_point" (ex: oalab.applet)

Interfaces and entry_points are described in plugin documentation.
Generally, a plugin code looks like:

.. code-block :: python
    :filename: ex: mypackage/plugin/applet.py
    :linenos:

    class PluginMyApplet(object):
        name = 'MyApplet'
        alias = 'My Applet'

        def __call__(self):
            from mypackage.gui.applet.myapplet import MyApplet
            return MyApplet


Once this class has been written, just register it in the setup.py file of your python package.

.. code-block :: python

    entry_points={
        'oalab.applet': [
            'MyApplet = mypackage.plugin.applet:PluginMyApplet',
            ]
        }


With **mypackage.plugin.applet** python module path (equivalent to 'mypackage/plugin/applet.py').
"""

from .plugin import discover, iter_groups, iter_plugins, Plugin

