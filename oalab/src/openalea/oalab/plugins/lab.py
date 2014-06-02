"""
===========================
Lab plugin documentation
===========================

To define a new extension for OpenAleaLab, you must
  #. write a LabPlugin class that respects IPluginLab interface (see below)
  #. add it to group "oalab.lab"

1. Copy paste this code and fill it with right names and instructions.
(replace all xyz, respecting case, with your applet name).
For example Xyz -> PythonLab


.. code-block :: python

    from openalea.vpltk.plugin import Plugin

    class PluginXyz(Plugin):

        name = 'Xyz'

        def __call__(self, mainwindow):
            # Write your code here


2. Once this class has been written, just register it in the setup.py file of
your python package.

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

        .. code-block:: python

            for plugin in iter_plugins('oalab.applet'):
                if plugin.name = 'AbcApplet':
                    mainwin.add_plugin(plugin())

        """

