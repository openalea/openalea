
from .control import Control
from .pyserial import serialize_controls
from openalea.core.serialization import AbstractSaver, AbstractLoader


class ControlSerializer(object):
    dtype = 'openalealab/control'

    def serialize(self, obj, fmt=None, **kwds):
        if isinstance(obj, Control):
            obj = [obj]
        return serialize_controls(obj)


class ControlDeserializer(object):

    def deserialize(self, lines, fmt=None, **kwds):
        ns = {}
        for l in lines:
            exec l in ns
        controls = ns.get('controls', [])
        return controls


class ControlSaver(AbstractSaver):

    def _serialize(self, obj, fmt, **kwds):
        serializer = ControlSerializer()
        return serializer.serialize(obj, fmt, **kwds)


class ControlLoader(AbstractLoader):

    def _deserialize(self, lines, fmt, **kwds):
        serializer = ControlDeserializer()
        return serializer.deserialize(lines, fmt=fmt, **kwds)
