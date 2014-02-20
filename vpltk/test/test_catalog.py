from openalea.vpltk.catalog import Catalog

catalog = Catalog()

def test_services():

    service1 = catalog.get_service(identifier='openalea-test:XyzHandler')
    service2 = catalog.get_service(identifier='openalea-test:XyzHandler')

    assert service1 is service2
    assert hasattr(service1, 'read')
    assert hasattr(service1, 'write')

def test_get_factories():

    interfaces = catalog.get_interfaces()
    assert 'openalea-test:IXyzReader' in interfaces
    assert 'openalea-test:IXyzWriter' in interfaces

    factories = catalog.get_factories(tags=['plugin'])
    names = [factory.name for factory in factories]
    assert 'openalea-test:XyzHandler' in names

    xyzhandlers = catalog.get_factories(identifier='openalea-test:XyzHandler')
    assert len(xyzhandlers) == 1
    xyzhandler = catalog.get_factory(identifier='openalea-test:XyzHandler')
    assert xyzhandler == xyzhandlers[0]


    interface_name = 'openalea-test:IXyzReader'
    names = [factory.name for factory in catalog.get_factories(interfaces=interface_name)]

    assert interface_name not in names

    xyzreader = catalog.get_factory(interfaces='openalea-test:IXyzReader')
    xyzwriter = catalog.get_factory(interfaces='openalea-test:IXyzWriter')
    
    assert xyzreader.name == xyzwriter.name == 'openalea-test:XyzHandler'

def test_interface_ids():
    interface_name = 'openalea-test:IXyzReader'
    interface_factory = catalog.get_factory(identifier=interface_name)
    interface = interface_factory.instantiate()

    from openalea.vpltk.sample.__plugin__ import IXyzReader as factory_IXyzReader
    from openalea.vpltk.sample.interfaces import IXyzReader as interface_IXyzReader
    from openalea.vpltk.sample.implementations import XyzHandler

    assert catalog.get_interface_id(interface_name) == interface_name
    assert catalog.get_interface_id(interface_factory) == interface_name
    assert catalog.get_interface_id(interface) == interface_name

    # Cannot assert objects are identical ... why ?
    assert interface_factory.name == factory_IXyzReader.name

    assert interface == interface_IXyzReader

    factory_name = 'openalea-test:XyzHandler'
    assert isinstance(catalog.get_factory(identifier=factory_name).instantiate(), XyzHandler)
    assert isinstance(catalog.get_factory(interfaces=interface).instantiate(), XyzHandler)
    assert isinstance(catalog.get_factory(interfaces=interface_name).instantiate(), XyzHandler)
    assert isinstance(catalog.get_factory(interfaces=interface_factory).instantiate(), XyzHandler)

