

from openalea.core.package import *
from openalea.core.node import gen_port_list
import os

def test_package():


    metainfo={ 'version' : '0.0.1',
               'license' : 'CECILL-C',
               'authors' : 'OpenAlea Consortium',
               'institutes' : 'INRIA/CIRAD',
               'description' : 'Base library.',
               'url' : 'http://openalea.gforge.inria.fr'
               }
    

    package = Package("Test", metainfo)

    assert package != None



def test_userpackage():


    metainfo={ 'version' : '0.0.1',
               'license' : 'CECILL-C',
               'authors' : 'OpenAlea Consortium',
               'institutes' : 'INRIA/CIRAD',
               'description' : 'Base library.',
               'url' : 'http://openalea.gforge.inria.fr'
               }
    

    package = UserPackage("DummyPkg", metainfo, os.path.curdir)



    factory = package.create_user_factory("TestFact", "", "",
                                          gen_port_list(3),
                                          gen_port_list(2))
    
    assert os.path.curdir in factory.search_path
    assert len(factory.inputs)==3
    assert len(factory.outputs)==2

    assert os.path.exists("TestFact.py")
    execfile("TestFact.py")

    package.write()
    assert os.path.exists("DummyPkg_wralea.py")
    execfile("DummyPkg_wralea.py")


    os.remove("DummyPkg_wralea.py")
    os.remove("DummyPkg_wralea.pyc")
    os.remove("TestFact.py")
    

    

