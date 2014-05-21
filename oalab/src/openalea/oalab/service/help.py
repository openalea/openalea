# Add header here

""" Service that implements adaptation from a Python object to a 3D shape model.

Currently, the service convert object to PlantGL shapes.
"""

__all__ = ['help', 'register_helper']


def find_helper(plugin_name='oalab.service.register_helper'):
    """ Find Helper defined as entry points.

    A Plugin return a registry of adapters.
    A registry is a mapping between a type or a tuple of types and a functor returning a
    3D model.
    """
    register = []
    from openalea.vpltk.plugin import iter_plugins
    for plugin in iter_plugins(plugin_name):
        register.append(plugin.registry)
    return register

__registry = find_helper()


def register_helper(helper):
    __registry.append(helper)


def help(obj):
    doc = str(get_doc(obj))

    for helper in __registry:
        helper.setText(doc)


def get_doc(obj):
    # TODO: complete with other methods
    if hasattr(obj, "get_documentation"):
        return obj.get_documentation()
    elif isinstance(obj, str):
        return obj
    elif hasattr(obj, "__doc__"):
        return obj.__doc__
    else:
        return str(obj)

del find_helper
