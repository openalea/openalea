# -*- python -*-
#
#       OpenAlea.SoftBus: OpenAlea Software Bus
#
#       Copyright or (C) or Copr. 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Christophe Pradal <christophe.prada@cirad.fr>
#                       Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#



__doc__= """
Test the subgraph module
"""


from openalea.core.pkgmanager import PackageManager
from openalea.core.compositenode import CompositeNodeFactory
from openalea.core.node import Factory
import os

libraryname = "Library"


def test_compositenodewriter():

    pm = PackageManager ()
    pm.init()

    sgfactory = CompositeNodeFactory(pm, "addition")

    sgfactory.set_nb_input(3)
    sgfactory.set_nb_input(4)
    
    # build the compositenode factory
    addid = sgfactory.add_nodefactory ((libraryname, "+"))
    val1id = sgfactory.add_nodefactory ((libraryname, "float")) 
    val2id = sgfactory.add_nodefactory ((libraryname, "float"))
    val3id = sgfactory.add_nodefactory ((libraryname, "float"))

    sgfactory.add_connection (val1id, 0, addid, 0)
    sgfactory.add_connection (val2id, 0, addid, 1)
    sgfactory.add_connection (addid, 0, val3id, 0)


    # Package
    metainfo={ 'version' : '0.0.1',
               'license' : 'CECILL-C',
               'authors' : 'OpenAlea Consortium',
               'institutes' : 'INRIA/CIRAD',
               'description' : 'Base library.',
               'url' : 'http://openalea.gforge.inria.fr'
               }


    package1 = pm.create_user_package("MyPackage", metainfo, os.path.curdir)
    package1.add_factory(sgfactory)

    print "package 1", package1
    package1.write()
    
    pm.init()

    newsg = pm.get_node('MyPackage', 'addition')

    sg = sgfactory.instantiate()

    sg.get_node_by_id(val1id).set_input(0, 2.)
    sg.get_node_by_id(val2id).set_input(0, 3.)

        # evaluation
    sg()

    assert sg.get_node_by_id(val3id).get_input(0) == 5.


def test_nodewriter():

    pm = PackageManager ()
    pm.init()


    # Package
    metainfo = { 'version' : '0.0.1',
               'license' : 'CECILL-C',
               'authors' : 'OpenAlea Consortium',
               'institutes' : 'INRIA/CIRAD',
               'description' : 'Base library.',
               'url' : 'http://openalea.gforge.inria.fr'
               }

    package1 = pm.create_user_package("MyPackage", metainfo, os.path.curdir)

    assert package1 != None

    nf = package1.create_user_factory(name="mynode",
                                      category='test',
                                      description="descr",
                                      nbin=0, nbout=0
                                      )

    
    package1.write()
    
    pm.init()

    newsg = pm.get_node('MyPackage', 'mynode')

    os.remove("MyPackage_wralea.py")
    os.remove("MyPackage_wralea.pyc")
    os.remove("mynode.py")
    os.remove("mynode.pyc")

    




