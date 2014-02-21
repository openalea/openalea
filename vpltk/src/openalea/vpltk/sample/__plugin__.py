
from openalea.vpltk.catalog.factories import InterfaceFactory, ObjectFactory
from openalea.vpltk.sample.interfaces import IXyzReader, IXyzWriter

__all__ = []

IXyzReader = InterfaceFactory(IXyzReader)
__all__.append('IXyzReader')

IXyzWriter = InterfaceFactory(IXyzWriter)
__all__.append('IXyzWriter')

XyzHandler = ObjectFactory(name='openalea-test:XyzHandler', 
                          description="A sample to show interface/implementation mechanism", 
                          category="test", 
                          interfaces=["openalea-test:IXyzReader", "openalea-test:IXyzWriter"], 
                          nodemodule="openalea.vpltk.sample.implementations", 
                          nodeclass="XyzHandler")
__all__.append('XyzHandler')


