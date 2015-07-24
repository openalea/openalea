import inspect
from openalea.core.service.plugin import plugins, plugin, register_plugin


class PluginFunctor(object):

    def __init__(self, group, *args, **kwargs):
        self._group = group
        self._args = args
        self._kwargs = kwargs
        self._aliases = dict()

    def __getitem__(self, name):
        if name in self._aliases:
            name = self._aliases[name]
        return plugin(name) # Get the plugin class

    def __setitem__(self, name, value):
        if isinstance(value, basestring):
            value = plugin(value).identifier
            self._aliases[name] = value
            self.__class__.plugin = property(get_plugin, set_plugin, plugin_doc(self))
        elif inspect.isclass(value):
            if len(self._args) == 0 and not hasattr(value, 'args'):
                value.args = []
            for arg in self._args:
                if arg not in value.args:
                    raise ValueError('\'value\' parameter: missing keyword \'' + arg + '\'')
            for kwarg in self._kwargs:
                if not hasattr(value, kwarg):
                    raise ValueError('\'value\' parameter: missing attribute \'' + kwarg + '\'')
                elif not getattr(value, kwarg) == self._kwargs[kwarg]:
                    raise ValueError('\'value\' parameter: attribute \'' + kwarg
                                     + '\' not set to \'' + self._kwargs[kwarg] + '\'')
            register_plugin(self._group, value) # Add a plugin
            if name is not None:
                self[name] = plugin(value).identifier # Get the plugin unique name
            self.__class__.plugin = property(get_plugin, set_plugin, plugin_doc(self))
        else:
            raise TypeError('\'plugin\' parameter')


def get_plugin(self):
    return self._plugin


def set_plugin(self, name):
    self._plugin = name
    self.__class__.__call__ = self[self._plugin].implementation


def plugin_doc(plugin_func):
    __doc__ = ['Implemented plugins:']
    for plugin_class in plugins(plugin_func._group, *plugin_func._args, **plugin_func._kwargs):
        __doc__.append(' - `' + plugin_class.modulename + ':' + plugin_class.objectname + '`') # modulename and objectname
        if plugin_class.__doc__:
            __doc__[-1] += ' - ' + (" " * (len(__doc__[-1]) + 3)).join(line.strip() for line in plugin_class.__doc__.splitlines())
    __doc__.append('')
    __doc__.append('Defined aliases:')
    for alias in plugin_func._aliases:
        __doc__.append(' - `' + alias + '` - Alias for plugin `' + plugin_func._aliases[alias] + '`')
    return '\n'.join(__doc__)

PluginFunctor.plugin = property(get_plugin, set_plugin)
