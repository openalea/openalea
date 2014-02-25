
from openalea.vpltk.catalog.factories import InterfaceFactory, ObjectFactory
from openalea.vpltk.sample.interfaces import IXyzReader, IXyzWriter, IInfo

__all__ = []

IInfo = InterfaceFactory(IInfo)
__all__.append('IInfo')

IXyzReader = InterfaceFactory(IXyzReader)
__all__.append('IXyzReader')

IXyzWriter = InterfaceFactory(IXyzWriter)
__all__.append('IXyzWriter')

XyzHandler = ObjectFactory(name='XyzHandler', 
                          description="A sample to show interface/implementation mechanism", 
                          category="test", 
                          interfaces=["IXyzReader", "IXyzWriter"], 
                          nodemodule="openalea.vpltk.sample.implementations", 
                          nodeclass="XyzHandler")
__all__.append('XyzHandler')

Info = ObjectFactory(name='Info', 
                          description="A sample to show interface/implementation mechanism", 
                          category="test", 
                          interfaces=["IInfo"], 
                          nodemodule="openalea.vpltk.sample.implementations", 
                          nodeclass="Info")
__all__.append('Info')
