
class IReader(object):
    identifier = 'openalea-test:IReader'

    def read(self, filepath):
        raise NotImplementedError

class IWriter(object):
    identifier = 'openalea-test:IWriter'

    def write(self, filepath, data):
        raise NotImplementedError

class IXyzRepr(object):
    identifier = 'openalea-test:IXyzRepr'

class IXyzReader(IReader):
    identifier = 'openalea-test:IXyzReader'

    def read(self, filepath):
        raise NotImplementedError

class IXyzWriter(IWriter):
    identifier = 'openalea-test:IXyzWriter'

    def save(self, filepath, data):
        raise NotImplementedError
