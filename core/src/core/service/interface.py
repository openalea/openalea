# TODO: Header
#

""" TODO: Documentation

"""

from openalea.core.plugin.manager import PluginManager, get_implementation
from openalea.core.interface import IInterface, TypeInterfaceMap

pm = PluginManager()

__all__ = [
    'get_interface',
    'guess_interface',
    'interface_label',
    'interface_class',
    'interface_name',
    'new_interface',
]


def load_interfaces():
    """
    Need to load interface classes to auto register them
    (see :class:`openalea.core.interface.IInterfaceMetaClass`)
    """
    for plugin in pm.plugins('openalea.interface'):
        plugin.implementation

load_interfaces()


def interfaces(debug=False):
    """
    Iterator that returns all interface found
    """
    for interface in set(IInterface.all):
        yield interface

# guess is not explicit enough
# interface(1) is better than guess(1)
# or to_interface(obj) -> interface


def guess_interface(obj):
    """
    Returns interfaces than can correspond to object

    >>> guess(1)
    ['IInt']
    """
    interfaces = []
    type_to_iname = {}
    for (typ, interface) in TypeInterfaceMap().items():
        type_to_iname[typ] = [interface.__name__]
    classname_to_iname = {
        'NurbsCurve2D': ['ICurve2D'],
        'Material': ['IColor'],
        'NurbsPatch': ['IPatch'],
    }
    if obj and isinstance(obj, list):
        if obj[0].__class__.__name__ == 'Material':
            interfaces.append('IColorList')

    cname = obj.__class__.__name__
    if cname in classname_to_iname:
        interfaces += classname_to_iname[cname]

    if type(obj) in type_to_iname:
        interfaces += type_to_iname[type(obj)]

    return interfaces


def interface_class(interface=None):
    """
    Returns interface class corresponding to interface
    """
    if interface is None:
        return interfaces()

    _interface_class = None

    # interface is a builtin type (int, float, ...)
    if isinstance(interface, type):
        type_to_iname = {}
        for (typ, interface) in TypeInterfaceMap().items():
            type_to_iname[typ] = [interface.__name__]

        if interface in type_to_iname:
            return interface_class(type_to_iname[interface][0])

    # interface is a string of an interface or builtin type ('int', 'IInt', ...)
    if isinstance(interface, basestring):
        for _interface in interfaces():
            if _interface.__name__ == interface:
                _interface_class = _interface
                break

        # If interface has not been found, it may be because a string representing
        # type has been passed, for example 'int' instead of 'IInt' or int
        if _interface_class is None:
            try:
                interface_eval = eval(interface)
            except NameError:
                pass
            else:
                return interface_class(interface_eval)
        else:
            return _interface_class

    # interface is an IInterface instance
    elif isinstance(interface, IInterface):
        return interface.__class__

    # interface is an IInterface class
    elif issubclass(interface, IInterface):
        return interface

    # Nothing found
    else:
        raise ValueError, 'Interface %s not found ' % repr(interface)


def interface_name(interface=None):
    """
    Returns interface name corresponding to interface
    """
    if interface is None:
        return interface_names()
    else:
        cls = interface_class(interface)
        return cls.__name__


def get_interface(interface, *args, **kwargs):
    """
    If interface is yet an instance of interface, returns it else, return an
    instance based on interface.
    """
    if isinstance(interface, IInterface):
        return interface
    else:
        iclass = interface_class(interface)
        return iclass(*args, **kwargs)


def check_value(value, interface):
    pass


def new_interface(interface=None, value=None, *args, **kwargs):
    if interface is not None and value is None:
        return get_interface(interface, *args, **kwargs)
    elif interface is not None and value is not None:
        interface = get_interface(interface, *args, **kwargs)
        check_value(value, interface)
        return interface
    elif interface is None and value is not None:
        interface = guess_interface(value)
        if interfaces:
            return get_interface(interface[0], *args, **kwargs)
        else:
            raise ValueError, 'Cannot infer interface from %s' % value
    else:
        raise ValueError, 'you must define at least one of interface or value'


def interface_names(debug=False):
    names = [interface.__name__ for interface in interfaces()]
    return sorted(list(set(names)))


def interface_default_value(interface):
    if hasattr(interface, 'sample'):
        return interface.sample()
    elif hasattr(interface, 'default'):
        return interface.default()
    else:
        return None


def interface_label(interface):
    interface = interface_class(interface)
    if hasattr(interface, '__alias__'):
        return interface.__alias__
    else:
        return str(interface)
