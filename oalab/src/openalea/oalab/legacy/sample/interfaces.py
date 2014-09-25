
from openalea.oalab.legacy.catalog.interface import IInterface

class IInfo(IInterface):
    name = 'IInfo'

class IReader(IInterface):
    name = 'IReader'

    def read(self, filepath):
        raise NotImplementedError

class IWriter(IInterface):
    name = 'IWriter'

    def write(self, filepath, data):
        raise NotImplementedError

class IXyzRepr(IInterface):
    name = 'IXyzRepr'

class IXyzReader(IReader):
    name = 'IXyzReader'

    def read(self, filepath):
        raise NotImplementedError

class IXyzWriter(IWriter):
    name = 'IXyzWriter'

    def save(self, filepath, data):
        raise NotImplementedError
