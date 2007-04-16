# -*- python -*-
#
#       OpenAlea.Core: OpenAlea Core
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
Test the session
"""


from openalea.core.session import Session
from openalea.core.pkgmanager import PackageManager
from openalea.core.compositenode import CompositeNodeFactory, CompositeNode

import os
import openalea


def add_user_class(datapool):
    """ Add an user class to datapool """
    
    import moduletest
    datapool['j'] = moduletest.test_data()

    
def test_save_datapool():
    
    session = Session()
    datapool = session.datapool

    datapool['i'] = [1,2,3]

    add_user_class(datapool)
    session.save('test.pic')

    session.datapool.clear()
    session.load('test.pic')
    
    assert session.datapool['i'] == [1,2,3]
    os.remove('test.pic')


def test_save_workspace():
    
    session = Session()

    sgfactory = CompositeNodeFactory(session.pkgmanager, name="SubGraphExample",
                                description= "Examples",
                                category = "Examples",
                                )

    # build the subgraph factory

    addid = sgfactory.add_nodefactory ('i', ("Library", "int"))
    instance = sgfactory.instantiate()
    instance.node_id['i'].set_input(0,3)

    session.add_workspace(instance)

    session.save('test.pic')

    session.workspaces = []
    session.load('test.pic')

    i = session.workspaces[0]
    assert isinstance(i, CompositeNode)
    assert i.node_id['i'].get_input(0) == 3
    os.remove('test.pic')


test_save_workspace()



