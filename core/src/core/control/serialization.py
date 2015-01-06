
from .control import Control
from .pyserial import serialize_controls
from openalea.core.serialization import AbstractSaver, AbstractLoader, AbstractDeserializer


class ControlSerializer(object):

    def serialize(self, obj, protocol=None, **kwds):
        if isinstance(obj, Control):
            obj = [obj]
        return serialize_controls(obj)


class ControlDeserializer(AbstractDeserializer):

    def deserialize(self, lines, protocol=None, **kwds):
        ns = {}
        for l in lines:
            exec l in ns
        controls = ns.get('controls', [])
        return controls


class ControlSaver(AbstractSaver):
    dtype = 'IControl'
    protocols = ['text/x-python']

    def _serialize(self, obj, protocol, **kwds):
        serializer = ControlSerializer()
        return serializer.serialize(obj, protocol=protocol, **kwds)


class ControlLoader(AbstractLoader):
    dtype = 'IControl'
    protocols = ['text/x-python']

    def _deserialize(self, lines, protocol, **kwds):
        serializer = ControlDeserializer()
        return serializer.deserialize(lines, protocol=protocol, **kwds)
