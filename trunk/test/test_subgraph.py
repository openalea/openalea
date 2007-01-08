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


from core.pkgmanager import PackageManager
from core.subgraph import SubGraphFactory
from core.core import Package , RecursionError 

def test_subgraph():

    pm = PackageManager ()

    pkg = pm.add_wralea ("wralea.py")

    sgfactory = SubGraphFactory(pm, "addition")

    # build the subgraph factory
    addid = sgfactory.add_nodefactory ("simpleop", "add")
    val1id = sgfactory.add_nodefactory ("simpleop", "val")
    val2id = sgfactory.add_nodefactory ("simpleop", "val")
    val3id = sgfactory.add_nodefactory ("simpleop", "val")

    sgfactory.connect (val1id, 0, addid, 0)
    sgfactory.connect (val2id, 0, addid, 1)
    sgfactory.connect (addid, 0, val3id, 0)


    # allocate the subgraph

    sg = sgfactory.instantiate()

    sg.get_node_by_id(val1id).value = 2.
    sg.get_node_by_id(val2id).value = 3.

    
    # evaluation
    sg()

    assert sg.get_node_by_id(val3id).value == 5.


def test_recursion():


    pm = PackageManager ()
    pkg = Package("subgraph", {})

    sgfactory1 = SubGraphFactory(pm, "graph1")
    sgfactory2 = SubGraphFactory(pm,  "graph2")

    map (pkg.add_nodefactory, (sgfactory1, sgfactory2))

    assert len(pkg.get_node_names()) == 2

    pm.add_package(pkg)
    
    # build the subgraph factory

    sgfactory1.add_nodefactory ("subgraph", "graph2")
    sgfactory2.add_nodefactory ("subgraph", "graph1")

    try:
        sg = sgfactory1.instantiate ()
        assert False
    except RecursionError:
        assert True
        

def test_subgraphio():

    pm = PackageManager ()

    pkg = pm.add_wralea ("wralea.py")

    pkg = Package("subgraph", {})

    # create a subgraph with 2 in and 1 out
    # the subgraph does an addition
    sgfactory = SubGraphFactory(pm, "additionsg")
    sgfactory.set_numinput(2)
    sgfactory.set_numoutput(1)
        
    addid = sgfactory.add_nodefactory ("simpleop", "add")
    
    sgfactory.connect ('in', 0, addid, 0)
    sgfactory.connect ('in', 1, addid, 1)
    sgfactory.connect (addid, 0, 'out', 0)

    pkg.add_nodefactory(sgfactory)
    pm.add_package(pkg)


    sgfactory2 = SubGraphFactory(pm, "testio")
    addid = sgfactory2.add_nodefactory ("subgraph", "additionsg")
    val1id = sgfactory2.add_nodefactory ("simpleop", "val")
    val2id = sgfactory2.add_nodefactory ("simpleop", "val")
    val3id = sgfactory2.add_nodefactory ("simpleop", "val")

    sgfactory2.connect (val1id, 0, addid, 0)
    sgfactory2.connect (val2id, 0, addid, 1)
    sgfactory2.connect (addid, 0, val3id, 0)

    # allocate the subgraph
        
    sg = sgfactory2.instantiate()

    sg.get_node_by_id(val1id).value = 2.
    sg.get_node_by_id(val2id).value = 3.

    
    # evaluation
    sg()

    assert sg.get_node_by_id(val3id).value == 5.

