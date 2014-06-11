
__all__ = []

from openalea.vpltk.plugin import iter_plugins
from openalea.core.interface import IInterface

def guess(obj):
    """
    Returns interfaces than can correspond to object

    >>> guess(1)
    ['IInt']
    """
    type_to_iname = {
        int:['IInt'],
        float:['IFloat']
    }
    if type(obj) in type_to_iname:
        return type_to_iname[type(obj)]
    else:
        return []

def get_class(interface=None):
    """
    Returns interface class corresponding to interface
    """
    if interface is None:
        return interfaces()

    interface_class = None
    if isinstance(interface, basestring):
        for _interface in interfaces():
            if _interface.__name__ == interface:
                interface_class = _interface
                break
    elif isinstance(interface, IInterface):
        interface_class = interface.__class__
    elif issubclass(interface, IInterface):
        interface_class = interface

    if interface_class is None:
        raise ValueError, 'Interface %s not found' % repr(interface)
    else:
        return interface_class

def get_name(interface=None):
    """
    Returns interface name corresponding to interface
    """
    if interface is None:
        return names()
    else:
        cls = get_class(interface)
        return cls.__name__

def get(interface, *args, **kwargs):
    iclass = get_class(interface)
    return iclass(*args, **kwargs)

def check(value, interface):
    print 'check %s match %s' % (value, interface)
    pass

def new(interface=None, value=None, *args, **kwargs):
    if interface is not None and value is None:
        return get(interface, *args,**kwargs)
    elif interface is not None and value is not None:
        interface = get(interface, *args,**kwargs)
        check(value, interface)
        return interface
    elif interface is None and value is not None:
        interface = guess(value)
        if interfaces:
            return get(interface[0], *args, **kwargs)
        else:
            raise ValueError, 'Cannot infer interface from %s' % value
    else:
        raise ValueError, 'you must define at least one of interface or value'

def interfaces():
    for plugin in iter_plugins('oalab.interface'):
        for interface in plugin()():
            yield interface

def names():
    for plugin in iter_plugins('oalab.interface'):
        for interface in plugin()():
            yield interface.__name__


def default_value(interface):
    if hasattr(interface, 'sample'):
        return interface.sample()
    elif hasattr(interface, 'default'):
        return interface.default()
    else:
        return None

def alias(interface):
    interface = get_class(interface)
    if hasattr(interface, '__alias__'):
        return interface.__alias__
    else:
        return str(interface)
