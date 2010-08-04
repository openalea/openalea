# -*- python -*-
#
#       OpenAlea.SoftBus: OpenAlea Software Bus
#
#       Copyright 2006 INRIA - CIRAD - INRA
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
"""Test the subgraph module"""

__license__ = "Cecill-C"
__revision__ = " $Id$ "


from openalea.core.pkgmanager import PackageManager
from openalea.core.compositenode import CompositeNodeFactory, CompositeNode
from openalea.core.node import Factory, gen_port_list
import os
import shutil


def setup_module():
    try:
        path = os.path.join(os.path.curdir, "MyTestPackage")
        shutil.rmtree(path)

    except:
        pass


def test_compositenodewriter():

    setup_module()

    pm = PackageManager()
    pm.init()

    sg = CompositeNode(inputs=[dict(name="%d" % i) for i in xrange(3)],
                       outputs=[dict(name="%d" % i) for i in xrange(4)],
                      )

    # build the compositenode factory
    addid = sg.add_node(pm.get_node("pkg_test", "+"))
    val1id = sg.add_node(pm.get_node("pkg_test", "float"))
    val2id = sg.add_node(pm.get_node("pkg_test", "float"))
    val3id = sg.add_node(pm.get_node("pkg_test", "float"))

    sg.connect(val1id, 0, addid, 0)
    sg.connect(val2id, 0, addid, 1)
    sg.connect(addid, 0, val3id, 0)
    sg.connect(val3id, 0, sg.id_out, 0)
    sgfactory = CompositeNodeFactory("addition")
    sg.to_factory(sgfactory)
    # Package
    metainfo = {'version': '0.0.1',
               'license': 'CECILL-C',
               'authors': 'OpenAlea Consortium',
               'institutes': 'INRIA/CIRAD',
               'description': 'Base library.',
               'url': 'http://openalea.gforge.inria.fr'}

    package1 = pm.create_user_package("MyTestPackage", 
                                      metainfo, os.path.curdir)
    package1.add_factory(sgfactory)
    print package1.keys()
    assert 'addition' in package1
    package1.write()

    sg = sgfactory.instantiate()

    sg.node(val1id).set_input(0, 2.)
    sg.node(val2id).set_input(0, 3.)

    # evaluation
    sg()
    print sg.node(val3id).get_output(0)
    assert sg.node(val3id).get_output(0) == 5.

    print "nb vertices", len(sg)
    assert len(sg) == 6

    pm.init()
    newsg = pm.get_node('MyTestPackage', 'addition')
    print "nb vertices", len(newsg)
    assert len(newsg) == 6


def test_nodewriter():
    """test node writer"""
    setup_module()

    pm = PackageManager()
    pm.clear()
    pm.init()

    # Package
    metainfo = {'version': '0.0.1',
               'license': 'CECILL-C',
               'authors': 'OpenAlea Consortium',
               'institutes': 'INRIA/CIRAD',
               'description': 'Base library.',
               'url': 'http://openalea.gforge.inria.fr'}

    package1 = pm.create_user_package("MyTestPackage", \
        metainfo, os.path.curdir)
    assert package1 != None

    nf = package1.create_user_node(name="mynode",
                                      category='test',
                                      description="descr",
                                      inputs=(),
                                      outputs=(),
                                      )
    package1.write()
    pm.init()
    newsg = pm.get_node('MyTestPackage', 'mynode')
    package1.remove_files()

