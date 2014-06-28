# Add header here

""" Service that implements adaptation from a Python object to a 3D shape model.

Currently, the service convert object to PlantGL shapes.
"""

from openalea.oalab.world.world import WorldObject

__all__ = ['to_shape3d', 'register_shape3d']

def find_plugins(plugin_name='oalab.service.to_shape3d', debug=False):
    """ Find plugins defined as entry points.

    A Plugin return a registry of adapters.
    A registry is a mapping between a type or a tuple of types and a functor returning a
    3D model.
    """
    register = {}
    from openalea.vpltk.plugin import iter_plugins
    for plugin in iter_plugins(plugin_name, debug=debug):
        register.update(plugin.registry)
    return register

__registry = find_plugins()

def register_shape3d(type_or_types, functor):
    __registry[type_or_types] = functor

def to_shape3d(obj):
    import openalea.plantgl.all as pgl
    import collections
    if isinstance(obj, (pgl.Scene, pgl.Shape, pgl.Geometry)):
        return obj

    if issubclass(type(obj), collections.Sequence):
        try:
            result = pgl.Scene(obj)
            return result
        except Exception, e:
            pass

    # Case _repr_geom_
    if hasattr(obj, "_repr_geom_"):
        return to_shape3d(obj._repr_geom_())

    if isinstance(obj, WorldObject):
        return to_shape3d(obj.obj)

    for types, function in __registry.iteritems():
        if isinstance(obj, types):
            return to_shape3d(function(obj))

del find_plugins
