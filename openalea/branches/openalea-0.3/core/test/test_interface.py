# Core interface test


from openalea.core.interface import *
from types import *


# Test declation of a new interface
class IMyInterface(IInterface):

    __pytype__ = InstanceType


def test_mapper():

    map = TypeInterfaceMap()

    assert map[FloatType] == IFloat
    assert map[IntType] == IInt
    assert map[BooleanType] == IBool
    assert map[StringType] == IStr
    assert map[ListType] == ISequence
    assert map[DictType] == IDict
    
    assert map[InstanceType] == IMyInterface
    

    
