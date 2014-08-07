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
"""Test the composite node module"""

__license__ = "Cecill-C"
__revision__ = " $Id$ "

from openalea.core.pkgmanager import PackageManager
from openalea.core.compositenode import CompositeNodeFactory, CompositeNode
from openalea.core.node import gen_port_list, RecursionError
from openalea.core import Package
from openalea.core.path import path


class TestClass:
    def setUp(self):
        d= {}
        execfile('catalog.py', globals(), d)
        self.pkg = d['pkg']
        self.plus_node= self.pkg['plus'].instantiate()
        self.float_node= self.pkg['float'].instantiate()
        self.int_node= self.pkg['int'].instantiate()
        self.string_node= self.pkg['string'].instantiate()
        self.pm = PackageManager()
        self.pm.add_package(self.pkg)

    def test_instantiate_compositenode(self):
        """test instantiation"""
        #pm = PackageManager()
        #pm.init()

        sg = CompositeNode()

        # build the compositenode factory
        addid = sg.add_node(self.plus_node)
        val1id = sg.add_node(self.float_node)
        val2id = sg.add_node(self.float_node)
        val3id = sg.add_node(self.float_node)

        sg.connect(val1id, 0, addid, 0)
        sg.connect(val2id, 0, addid, 1)
        sg.connect(addid, 0, val3id, 0)

        sgfactory = CompositeNodeFactory("addition")
        sg.to_factory(sgfactory)

        # allocate the compositenode
        sg = sgfactory.instantiate()
        sg.node(val1id).set_input(0, 2.)
        sg.node(val2id).set_input(0, 3.)

        # evaluation
        sg()

        assert sg.node(val3id).get_output(0) == 5.


    def test_compositenode_creation_without_edges(self):
        """test compositenode creation without edges"""

        sg = CompositeNode()

        # build the compositenode factory
        addid = sg.add_node(self.plus_node)
        val1id = sg.add_node(self.float_node)
        val2id = sg.add_node(self.float_node)
        val3id = sg.add_node(self.float_node)

        sgfactory = CompositeNodeFactory("addition")
        sg.to_factory(sgfactory)
        # allocate the compositenode
        sg = sgfactory.instantiate()

        assert len(sg) == 4+2


    def test_to_factory(self):
        """ Create a compositenode, generate its factory and reintantiate it """

        sg = CompositeNode()

        n1 = self.float_node
        n2 = self.float_node
        e1 = sg.add_node(n1)
        e2 = sg.add_node(n2)
        sg.connect(e1, 0, e2, 0)

        n1.set_input(0, 34.)
        sg()
        assert n2.get_output(0)==34.
    
        sgfactory = CompositeNodeFactory("factorytest")
        sg.to_factory(sgfactory)

        sg2 = sgfactory.instantiate()

        assert len(list(sg2.vertices()))==2+2 # two nodes + in/ou
        assert len(list(sg2.edges()))==1

        sg2.node(e1).set_input(0, 3.)
        sg2()
        assert sg2.node(e2).get_output(0)==3.

        return sg, sgfactory


    def test_to_factory2(self):
        """ test factory """
        sg, sgfactory= self.test_to_factory()
        sg.to_factory(sgfactory)
        sg2= sgfactory.instantiate()
        assert len(sg)==len(sg2)


    # need to be checked. Order has changed


    def test_recursion_factory(self):
        """ Test Recursion detection"""

        pm = self.pm
        #pm.init()
        pkg = Package("compositenode", {})

        sgfactory1 = CompositeNodeFactory("graph1")
        sgfactory2 = CompositeNodeFactory("graph2")

        map(pkg.add_factory, (sgfactory1, sgfactory2))

        assert len(pkg.get_names()) == 2

        pm.add_package(pkg)
    
        n1 = sgfactory1.instantiate()
        n2 = sgfactory1.instantiate()
        # build the compositenode factory
        n1.add_node(n2)
        n2.add_node(n1)

        n1.to_factory(sgfactory1)
        n2.to_factory(sgfactory2)

        #sgfactory1.add_nodefactory ( ("compositenode", "graph2"))
        #sgfactory2.add_nodefactory ( ("compositenode", "graph1"))

        try:
            sg = sgfactory1.instantiate()
            assert False
        except RecursionError:
            assert True


    def test_compositenodeio(self):
        """ Test IO"""
        pm = self.pm
        #pm.init()

        pkg = Package("compositenode", {})

        # create a compositenode with 2 in and 1 out
        # the compositenode does an addition
        sg = CompositeNode(inputs=(dict(name="in1", interface=None, value=None),
                                  dict(name="in2", interface=None, value=None)),
                          outputs=(dict(name="out", interface=None), ), )
        addid = sg.add_node(self.plus_node)

        sg.connect(sg.id_in, 0, addid, 0)
        sg.connect(sg.id_in, 1, addid, 1)
        sg.connect(addid, 0, sg.id_out, 0)

        sgfactory = CompositeNodeFactory("additionsg")
        sg.to_factory(sgfactory)

        sg1= sgfactory.instantiate()
        sg1.set_input(0, 2.)
        sg1.set_input(1, 3.)
        sg1()

        assert sg1.get_output(0)==5.

        pkg.add_factory(sgfactory)
        pm.add_package(pkg)

        sg = CompositeNode()
        addid = sg.add_node(pm.get_node("compositenode", "additionsg"))
        val1id = sg.add_node(self.float_node)
        val2id = sg.add_node(self.float_node)
        val3id = sg.add_node(self.float_node)

        sg.connect(val1id, 0, addid, 0)
        sg.connect(val2id, 0, addid, 1)
        sg.connect(addid, 0, val3id, 0)

        sgfactory2 = CompositeNodeFactory("testio")
        sg.to_factory(sgfactory2)
        # allocate the compositenode

        sg = sgfactory2.instantiate()
        sg.node(val1id).set_input(0, 2.)
        sg.node(val2id).set_input(0, 3.)

        # evaluation
        sg()
        assert sg.node(val3id).get_output(0)==5.


    def test_addnode(self):
        """Test  node addition"""

        sg = CompositeNode()

        # build the compositenode factory
        val1id = sg.add_node(self.float_node)
        val2id = sg.add_node(self.float_node)

        sg.connect(val1id, 0, val2id, 0)

        sgfactory = CompositeNodeFactory("testaddnode")
        sg.to_factory(sgfactory)
        # allocate the compositenode

        sg = sgfactory.instantiate()

        sg.node(val1id).set_input(0, 2.)
        sg()
        assert sg.node(val2id).get_output(0)==2.


        # Add a new node
        addid = sg.add_node(self.plus_node)
        sg.connect(val1id, 0, addid, 0)
        sg.connect(val2id, 0, addid, 1)

        sg.to_factory(sgfactory)
        sg = sgfactory.instantiate()
        sg.node(val1id).set_input(0, 3.)
        sg()
        assert sg.node(addid).get_output(0)==6.


    def test_multi_out_eval(self):
        """ Test multiple out connection"""

        sg = CompositeNode()

        # build the compositenode factory
        val1id = sg.add_node(self.string_node)
        val2id = sg.add_node(self.string_node)
        val3id = sg.add_node(self.string_node)

        sg.connect(val1id, 0, val2id, 0)
        sg.connect(val1id, 0, val3id, 0)

        sgfactory = CompositeNodeFactory("testlazyeval")
        sg.to_factory(sgfactory)
        # allocate the compositenode
        sg = sgfactory.instantiate()

        sg.node(val1id).set_input(0, "teststring")
        sg()
        assert sg.node(val2id).get_output(0) == "teststring"
        assert sg.node(val3id).get_output(0) == "teststring"

        #partial evaluation
        sg.node(val1id).set_input(0, "teststring2")
        sg.eval_as_expression(val2id)
        assert sg.node(val2id).get_output(0) == "teststring2"

        sg.eval_as_expression(val3id)
        assert sg.node(val3id).get_output(0) == "teststring2"


    def test_multi_in_eval(self):
        """ Test multiple out connection"""
        sg = CompositeNode()

        # build the compositenode factory
        val1id = sg.add_node(self.string_node)
        val2id = sg.add_node(self.string_node)
        val3id = sg.add_node(self.string_node)

        sg.connect(val1id, 0, val3id, 0)
        sg.connect(val2id, 0, val3id, 0)


        sgfactory = CompositeNodeFactory("testlazyeval")
        sg.to_factory(sgfactory)
        # allocate the compositenode
        sg = sgfactory.instantiate()

        sg.node(val1id).set_input(0, "teststring1")
        sg.node(val2id).set_input(0, "teststring2")
        sg()
        assert (sg.node(val3id).get_output(0) == "['teststring1', 'teststring2']")\
            or \
            (sg.node(val3id).get_output(0) == "['teststring2', 'teststring1']")


    def test_change_io(self):
        """ Test set_io"""

        ins = [dict(name="in1"), dict(name="in2")]
        outs = [dict(name="out1"), dict(name="out2")]
        sg = CompositeNode(ins, outs)
        assert sg.get_nb_input() == 2
        assert sg.get_nb_output() == 2

        ins = [dict(name="in1")]
        outs = [dict(name="out1"), dict(name="out2"), dict(name="out3")]

        sg.set_io(ins, outs)
        assert sg.get_nb_input() == 1
        assert sg.get_nb_output() == 3


    def test_auto_io(self):
        """ Test auto io"""
        sg = CompositeNode()

        # build the compositenode factory
        val1id = sg.add_node(self.string_node)
        val2id = sg.add_node(self.string_node)
        val3id = sg.add_node(self.string_node)


        sg.connect(val1id, 0, val3id, 0)
        sg.connect(val2id, 0, val3id, 0)

        sgfactory = CompositeNodeFactory("testlautoio")
        sg.to_factory(sgfactory, listid=[val1id, val2id, val3id], auto_io=True)

        # allocate the compositenode
        sg = sgfactory.instantiate()
        assert sg.get_nb_input() == 2
        assert sg.get_nb_output() == 1
        sg.set_input(0, "to")
        sg.set_input(1, "to")

        sg()
        res = sg.get_output(0)
        assert ''.join(eval(res)) == "toto"


