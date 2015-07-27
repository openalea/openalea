"""
To define a new extension (ex: an applet called MyApplet) corresponding to a category (ex: oalab.applet), you must
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
        __plugin__ = True

        def __call__(self):
            from mypackage.gui.applet.myapplet import MyApplet
            return MyApplet


Once this class has been written, just register it in the setup.py file of your python package.

.. code-block :: python

    entry_points={
        'oalab.applet': [
            'MyApplet = mypackage.plugin.applet', # read all plugins defined in this module ...
            ]
        }


.. note::

    You can also define a plugin explicitly with:

    .. code-block: python

      'MyApplet = mypackage.plugin.applet:PluginMyApplet', # read only specified plugin


With **mypackage.plugin.applet** python module path (equivalent to 'mypackage/plugin/applet.py').


Coding conventions
==================

In openalea packages, plugin follow this convention:

package.plugin.category 
-----------------------
Describe how to extend this package:
  - entry point category supported by this package (generally "package.category")
  - API of plugin class (required attributes, optional meta-info, ...)
  - API of implementation (can be function or class)

Generally, API are described from documentation or interface classes.

ex: :mod:`openalea.core.plugin.applet`

package.plugin.builtin
----------------------
This module contains Plugin class, describing plugins that extend package itself or another package.
Generally, these plugin define "default" or "standard" implementation and algorithms (if extend package itself) or 
alternatives (if extends an other package). 
Real implementation (class, algo, ...) are generally defined in an other module with explicit name.

Builtin plugin for package itself can also be used, by contributors, as real example of how to create a new plugin.

ex: :mod:`openalea.core.plugin.builtin.applet`

package.*
------------------

You are free to put real implementation (class or algo) in the module of your choice.
Implementation are classical python objects (except that its follow a special API), so you can put code where you want,
like you will do for other libraries.
Follow a special interface doesn't mean class is derivated from an interface, just is has same public attributes and 
same methods.

Generally, package.category.implementation_name fit well.

ex: :mod:`openalea.oalab.applet.filebrowser`

or with a more generic package name:

ex: :mod:`openalea.oalab.widget.filebrowser`

In all cases, this path is defined in plugin class and you don't need to remember were package is defined.

"""

from .plugin import discover, iter_groups, iter_plugins, Plugin, PluginDef
