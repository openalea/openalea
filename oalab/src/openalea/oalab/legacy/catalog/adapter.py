
from openalea.core.singleton import Singleton
from .catalog import Catalog

class Register(dict):

    __metaclass__ = Singleton

    def __init__(self):
        dict.__init__(self)
        self._load_adapters()
        self._catalog = Catalog()

    def _load_adapters(self):
        adapters = self._catalog.factories(interfaces='IAdapter', tags=['adapters'])
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
    def adapter(self, interface_in, interface_out):
        key = (interface_in, interface_out)
        if key in self :
            return self[key].classobj()
        else :
            return None

def adapt(obj, interface, interface_in=None):
    # TODO: detect interface_in from obj
    adapter = Register().adapter(interface_in, interface)
    if adapter :
        return adapter(obj)
    else :
        raise TypeError, 'cannot adapt obj type %s to %s' % (interface_in, interface)

