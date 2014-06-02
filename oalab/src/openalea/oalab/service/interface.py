
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
    if hasattr(interface, 'default'):
        return interface.default()
    else:
        return None

def get_interface(iname):

    iname_to_interface = {}
    for plugin in iter_plugins('oalab.interface'):
        for interface in plugin()():
            iname_to_interface[interface.__name__] = interface

    type_to_iname = {
        int:'IInt',
        float:'IFloat'
    }

    if isinstance(iname, basestring):
        return iname_to_interface[iname]
    elif isinstance(iname, type):
        return iname_to_interface[type_to_iname[iname]]
    elif inspect.isclass(inspect):
        return iname
    elif isinstance(iname, IInterface):
        return iname.__class__
    else:
        raise ValueError, repr(iname)
