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
    
    asession = Session()
    datapool = asession.datapool

    datapool['i'] = [1,2,3]

    add_user_class(datapool)
    asession.save('test.pic')

    asession.datapool.clear()
    asession.load('test.pic')
    
    assert asession.datapool['i'] == [1,2,3]
    os.remove('test.pic')



def test_save_workspace():
    
    asession = Session()

    import sys
    
    sgfactory = CompositeNodeFactory(name="SubGraphExample",
                                description= "Examples",
                                category = "Examples",
                                )
    # build the subgraph factory

    addid = sgfactory.add_nodefactory (("Catalog.Data", "int"))
    instance = sgfactory.instantiate()

    instance.node_id[addid].set_input(0,3)
    asession.add_workspace(instance)

    asession.save('test.pic')

    asession.workspaces = []
    asession.load('test.pic')
    os.remove('test.pic')

    i = asession.workspaces[0]
    assert type(i) == type(instance)
    #assert i.node_id[addid].get_input(0) == 3

#test_save_workspace()



