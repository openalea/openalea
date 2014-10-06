
from openalea.core.service.interface import interface_name, interface_class, guess_interface, new_interface
from openalea.core.interface import IInterface


def test_guess_method():
    assert 'IInt' in guess_interface(1)

    class NotRegisteredClass(object):
        pass

    assert guess_interface(NotRegisteredClass()) == []

def test_new_and_get_class():
    iclass1 = interface_class('IInt')
    assert interface_class(iclass1) == iclass1
    assert issubclass(iclass1, IInterface)


    iname0 = 'IInt'
    iname1 = interface_name(iname0)
    iname2 = interface_name(iclass1)
    iname3 = interface_name(iclass1())
    iname4 = interface_name(int)
    iname5 = interface_name('int')

    assert iname1 == iname0
    assert iname2 == iname0
    assert iname3 == iname0
    assert iname4 == iname0
    assert iname5 == iname0

    interface1 = new_interface(iname1, min=1, max=1)
    interface2 = new_interface(iclass1, min=1, max=2)
    interface3 = new_interface(interface2, min=1, max=3)
    interface4 = new_interface(iname1, 1, min=1, max=4)
    interface5 = new_interface(value=1, min=1, max=5)

    assert isinstance(interface1, iclass1)
    assert isinstance(interface2, iclass1)
    assert isinstance(interface3, iclass1)
    assert isinstance(interface4, iclass1)
    assert isinstance(interface5, iclass1)

    # Warning, normal behaviour is to keep interface unchanged if interface is yet an instance
    assert(interface3.max == 2)

    assert(interface1.max == 1)
    assert(interface2.max == 2)
    assert(interface4.max == 4)
    assert(interface5.max == 5)
