from openalea.vpltk.catalog import Catalog

catalog = Catalog()

def test_services():
 
    service1 = catalog.service(name='XyzHandler')
    service2 = catalog.service(name='XyzHandler')
 
    assert service1 is service2
    assert hasattr(service1, 'read')
    assert hasattr(service1, 'write')


def test_get_factories():

    interfaces = list(catalog.interfaces())
    assert 'IXyzReader' in interfaces
    assert 'IXyzWriter' in interfaces

    factories = catalog.factories(tags=['plugin'])
    names = [factory.name for factory in factories]
    assert 'XyzHandler' in names

    xyzhandlers = catalog.factories(name='XyzHandler')
    assert len(xyzhandlers) == 1
    xyzhandler = catalog.factory(name='XyzHandler')
    assert xyzhandler == xyzhandlers[0]


    interface_name = 'IXyzReader'
    names = [factory.name for factory in catalog.factories(interfaces=interface_name)]

    assert interface_name not in names

    xyzreader = catalog.factory(interfaces='IXyzReader')
    xyzwriter = catalog.factory(interfaces='IXyzWriter')
    
    assert xyzreader.name == xyzwriter.name == 'XyzHandler'

def test_interface_ids():
    interface_name = 'IXyzReader'
    interface = catalog.interface(name=interface_name)

    from openalea.vpltk.sample.__plugin__ import IXyzReader as factory_IXyzReader
    from openalea.vpltk.sample.interfaces import IXyzReader as interface_IXyzReader
    from openalea.vpltk.sample.implementations import XyzHandler

    assert catalog.interface_id(interface_name) == interface_name
    assert catalog.interface_id(interface) == interface_name

    # Cannot assert objects are identical ... why ?
    assert interface.name == factory_IXyzReader.name

    assert interface == interface_IXyzReader

    factory_name = 'XyzHandler'
    assert isinstance(catalog.factory(name=factory_name).instantiate(), XyzHandler)
    assert isinstance(catalog.factory(interfaces=interface).instantiate(), XyzHandler)
    assert isinstance(catalog.factory(interfaces=interface_name).instantiate(), XyzHandler)

