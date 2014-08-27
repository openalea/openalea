"""
========================
OpenAleaLab's extensions
========================

.. note::

    To define a new extension for OpenAleaLab, you must
      #. write a LabPlugin class that respects IPluginLab interface (see below)
      #. add it to group "oalab.lab"

1. Copy paste this code and fill it with right names and instructions
   (replace all xyz respecting case with your lab name, for example Lab3D).

.. code-block :: python
    :filename: ex: mypackage/plugins/labs/xyz.py
    :linenos:

    class PluginXyz(object):
        name = 'Xyz'

        def __call__(self, mainwindow):
            # Write your code here

2. Fill code that loads and places applets in your lab.
   This can be hard-coded or can use plugins like 'oalab.applet' plugins.
   See :class:`details<openalea.oalab.plugins.lab.IPluginLab>`.


3. Once this class has been written, just register it in the setup.py file of your python package.

.. code-block :: python

    entry_points={
        'oalab.lab': [
            'Xyz = mypackage.plugins:PluginXyz',
            ]
        }


With **mypackage.plugins** python module path (equivalent to 'mypackage/plugins.py') and
'PluginXyz' the class name.


Details
=======

.. autoclass:: openalea.oalab.plugins.lab.IPluginLab
    :members: __call__, name

"""

class IPluginLab(object):

    name = 'xyz'

    def __call__(self, mainwin):
        """
        Load applet plugins and add its to mainwindow


        Example 1: Imports and places applets explicitly

        .. code-block:: python

            def __call__(self):
                from mypackage.plugins.applets import AbcApplet
                mainwin.add_applet(AbcApplet(), name='abc', area='inputs')


        Example 2: use oalab.applet plugins and select it by names.
        Here, plugin places himself in mainwindow.

        .. code-block:: python

            def __call__(self, mainwin):
                from openalea.vpltk.plugin import iter_plugins, check_dependencies
                for plugin in iter_plugins('oalab.applet'):
                    if plugin.name == 'AbcApplet':
                        if check_dependencies(plugin)
                            mainwin.add_plugin(plugin())

        """

