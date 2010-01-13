""" Core interface test"""

__license__ = "Cecill-C"
__revision__ = " $Id: test_interface.py 1586 2009-01-30 15:56:25Z cokelaer $ "

from openalea.core.interface import *
from types import *



class IMyInterface(IInterface):
    """Test declation of a new interface"""

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
