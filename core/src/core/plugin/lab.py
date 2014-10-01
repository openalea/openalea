"""
========================
OpenAleaLab's extensions
========================


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
                from openalea.core.plugin import iter_plugins
                for plugin in iter_plugins('oalab.applet'):
                    if plugin.name == 'AbcApplet':
                        mainwin.add_plugin(plugin())

        """

