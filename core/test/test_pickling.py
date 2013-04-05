# -*- python -*-
#
#       OpenAlea.Core: OpenAlea Core
#
#       Copyright 2012 INRIA - CIRAD - INRA
#
#       File author(s): Christophe Pradal <christophe.prada@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
"""Test pickling of openalea components"""

__license__ = "Cecill-C"
__revision__ = " $Id$ "

from pickle import dumps

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
        self.pm.init()
        self.pm.add_package(self.pkg)

        self.X = [f for f in self.pm.search_node('X') if f.name=='X'][0].instantiate()
        self.pmap = [f for f in self.pm.search_node('pmap') if f.name=='pmap'][0].instantiate()

    def test_pkgmgr(self):
        """test pickling of the PackageManager"""

        s = dumps(self.pm)

        assert s

    def test_compositenode(self):
        sg = CompositeNode()

        # build the compositenode factory
        addid = sg.add_node(self.plus_node)
        val1id = sg.add_node(self.int_node)
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

        s = dumps(sg)
        
        assert s

    def test_lambda(self):
        sg = CompositeNode()

        # build the compositenode factory
        addid = sg.add_node(self.plus_node)
        val1id = sg.add_node(self.X)
        val2id = sg.add_node(self.float_node)
        val3id = sg.add_node(self.float_node)

        sg.connect(val1id, 0, addid, 0)
        sg.connect(val2id, 0, addid, 1)
        sg.connect(addid, 0, val3id, 0)

        sgfactory = CompositeNodeFactory("addition")
        sg.to_factory(sgfactory)

        # allocate the compositenode
        sg = sgfactory.instantiate()
        sg.node(val2id).set_input(0, 3.)

        # evaluation
        sg()

        s = dumps(sg)
        assert s

        # check if the subdataflow can be serialized
        subdf = sg.node(addid).output(0)
        s = dumps(subdf)
        assert s



    def test_pmap(self):
        sg = CompositeNode()

        # build the compositenode factory
        addid = sg.add_node(self.plus_node)
        val1id = sg.add_node(self.X)
        val2id = sg.add_node(self.float_node)
        val3id = sg.add_node(self.pmap)

        sg.connect(val1id, 0, addid, 0)
        sg.connect(val2id, 0, addid, 1)
        sg.connect(addid, 0, val3id, 0)

        sgfactory = CompositeNodeFactory("addition")
        sg.to_factory(sgfactory)

        # allocate the compositenode
        sg = sgfactory.instantiate()
        sg.node(val2id).set_input(0, 3.)
        sg.node(val3id).set_input(1, range(100))
        sg.node(val3id).set_input(2, 2)

        # evaluation
        sg()
        res = sg.node(val3id).output(0)
        print res



