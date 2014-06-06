
__all__ = ['get_interface']

import inspect

from openalea.vpltk.plugin import iter_plugins
from openalea.core.interface import IInterface

def new_interface(iname, constraints=None):
    if constraints is None:
        constraints = {}
    interface_class = get_interface(iname)
    return interface_class(**constraints)

def default_value(interface):
    if hasattr(interface, 'sample'):
        return interface.sample()
    elif hasattr(interface, 'default'):
        return interface.default()
    else:
        return None

def alias(interface):
    interface = get_interface(interface)
    if hasattr(interface, '__alias__'):
        return interface.__alias__
    else:
        return str(interface)

def interfaces():
    for plugin in iter_plugins('oalab.interface'):
        for interface in plugin()():
            yield interface

def get_interface(iname):

    iname_to_interface = {}
    for interface in interfaces():
        iname_to_interface[interface.__name__] = interface

    type_to_iname = {
        int:'IInt',
        float:'IFloat'
    }

    if isinstance(iname, basestring):
        return iname_to_interface[iname]
    elif isinstance(iname, IInterface):
        return iname.__class__
    elif issubclass(iname, IInterface):
        return iname
    elif isinstance(iname, type):
        return iname_to_interface[type_to_iname[iname]]
    else:
        raise ValueError, repr(iname)
