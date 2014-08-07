
__all__ = ['IInterface']

from openalea.core.interface import IInterface as CoreIInterface

class IInterface(CoreIInterface):

    category = 'interfaces'

    @classmethod
    def is_valid(cls):
        return True
