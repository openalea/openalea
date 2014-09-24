
from openalea.oalab.legacy.catalog.factories import ObjectFactory
from openalea.vpltk.sample.interfaces import IXyzReader, IXyzWriter, IInfo
__all__ = ['IXyzReader', 'IXyzWriter', 'IInfo']


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
