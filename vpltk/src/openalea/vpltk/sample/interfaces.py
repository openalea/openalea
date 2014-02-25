
class IInfo(object):
    identifier = 'IInfo'

class IReader(object):
    identifier = 'IReader'

    def read(self, filepath):
        raise NotImplementedError

class IWriter(object):
    identifier = 'IWriter'

    def write(self, filepath, data):
        raise NotImplementedError

class IXyzRepr(object):
    identifier = 'IXyzRepr'

class IXyzReader(IReader):
    identifier = 'IXyzReader'

    def read(self, filepath):
        raise NotImplementedError

class IXyzWriter(IWriter):
    identifier = 'IXyzWriter'

    def save(self, filepath, data):
        raise NotImplementedError
