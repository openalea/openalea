import inspect
from openalea.core.service.plugin import plugins, plugin, register_plugin


class PluginFunctor(object):

    @staticmethod
    def factory(group, default=None, *tags, **criteria):

        class PluginFunctorSingleton(PluginFunctor):
            _group = group
            _tags = tags
            _criteria = criteria
            _aliases = dict()

            def __call__(self):
                """No implementation precised"""
                return NotImplemented

            _plugin = None

        functor = PluginFunctorSingleton()
        if default:
            functor.plugin = default
        functor.__class__.plugin = property(get_plugin, set_plugin, doc=plugin_doc(functor))
        return functor

    def __contains__(self, name):
        if not name in self._aliases:
            try:
                plugin(name, self._group)
            except:
                return False
            else:
                return True
        else:
            return True

    def __delitem__(self, name):
        if not name in self._aliases:
            raise KeyError('\'name\' parameter is not a plugin alias')
        del self._aliases[name]

    def __getitem__(self, name):
        if name in self._aliases:
            name = self._aliases[name]
        return plugin(name, self._group) # Get the plugin class

    def __setitem__(self, name, value):
        if isinstance(value, basestring):
            value = plugin(value, self._group).identifier
            self._aliases[name] = value
            self.__class__.plugin = property(get_plugin, set_plugin, doc=plugin_doc(self))
        elif inspect.isclass(value):
            if len(self._tags) == 0 and not hasattr(value, 'tags'):
                value.tags = []
            for tag in self._tags:
                if tag not in value.tags:
                    raise ValueError('\'value\' parameter: missing tag \'' + tag + '\'')
            for criterion in self._criteria:
                if not hasattr(value, criterion):
                    raise ValueError('\'value\' parameter: missing criterion \'' + criterion + '\'')
                elif not getattr(value, criterion) == self._criteria[criterion]:
                    raise ValueError('\'value\' parameter: criterion \'' + criterion
                                     + '\' not equal to \'' + self._criteria[criterion] + '\'')
            value = register_plugin(value, self._group).identifier # Add a plugin
            if name is not None:
                self[name] = value # Get the plugin unique name
            self.__class__.plugin = property(get_plugin, set_plugin, doc=plugin_doc(self))
        else:
            raise TypeError('\'plugin\' parameter')


def get_plugin(self):
    return self._plugin


def set_plugin(self, name):
    self._plugin = name
    self.__class__.__call__ = staticmethod(self[self._plugin].implementation)


def plugin_doc(plugin_func):
    __doc__ = ['Implemented plugins:']
    for plugin_class in plugins(plugin_func._group, plugin_func._tags, plugin_func._criteria):
        __doc__.append(' * "' + plugin_class.identifier + '"') # modulename and objectname
        if plugin_class.__doc__:
            __doc__[-1] += ' - ' + (" " * (len(__doc__[-1]) + 3)).join(line.strip()
                                                                       for line in plugin_class.__doc__.splitlines())
    __doc__.append('')
    __doc__.append('Defined aliases:')
    for alias in plugin_func._aliases:
        __doc__.append(' * "' + alias + '" - Alias for plugin "' + plugin_func._aliases[alias] + '"')
    return '\n'.join(__doc__)

PluginFunctor.plugin = property(get_plugin, set_plugin)
