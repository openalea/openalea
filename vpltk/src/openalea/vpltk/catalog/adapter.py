
from openalea.core.singleton import Singleton
from .catalog import CATALOG
# TODO
# global ? CATAL or Catal()

class Register(dict):

    __metaclass__ = Singleton

    def __init__(self):
        dict.__init__(self)
        self._load_adapters()

    def _load_adapters(self):
        adapters = CATALOG.factories(interfaces='IAdapter', tags=['adapters'])
        for adapter in adapters :
            try:
                inputs = adapter.kargs['adapter_inputs']
                outputs = adapter.kargs['adapter_outputs']
            except (AttributeError, KeyError):
                pass
            else:
                for in_ in inputs:
                    for out_ in outputs:
                        self[(in_, out_)] = adapter

REGISTER = Register()
# TODO
# global ?

def adapt(obj, interface, interface_in=None):
    # TODO: detect interface_in from obj
    key = (interface_in, interface)
    if key in REGISTER :
        return REGISTER[key].instantiate(obj)
    else :
        raise TypeError, 'cannot adapt obj type %s to %s' %(interface_in, interface)

