# Tests for wralea.py



#from openalea.softbus.core import Package, NodeFactory

from aleacore.core import Package, NodeFactory
from aleacore.subgraph import SubGraphFactory
from simpleop import Add, Value

#register packages


def register_packages(pkgmanager):
    """ Initialisation function
    Return a list of package to include in the package manager.
    This function is called by the package manager when it is updated
    """

    # Meta information associated to the package

    pkg_metainfo={ 'version' : '0.0.1',
                   'license' : 'CECILL-C',
                   'authors' : 'SDK, CP',
                   'institutes' : 'INRIA/CIRAD',
                   'description' : 'Simple operations.',
                   }


    oppackage=Package("simpleop", pkg_metainfo)




        
    nf1=NodeFactory( name= "add", # name
                    desc= "Addition", # description
                    doc= Add.__doc__, # documentation string
                    cat = "Operations", # category
                    module = "simpleop",
                    nodeclass = "Add", # Node
                    widgetclass = None, # Widget
                    )

    nf2=NodeFactory(name = "val", # name
                    desc = "Value", # description
                    doc = Value.__doc__, # documentation string
                    cat  = "Operations", # category
                    module = "simpleop",
                    nodeclass = "Value", # Node
                    widgetclass = None, # Widget
                    )

                      
    oppackage.add_nodefactory( nf1 )
    oppackage.add_nodefactory( nf2 )




    # SUBGRAPH

    # Meta information associated to the package

    pkg_metainfo={ 'version' : '0.0.1',
                   'license' : 'CECILL-C',
                   'authors' : 'SDK, CP',
                   'institutes' : 'INRIA/CIRAD',
                   'description' : 'Subgraphs.',
                   }

    subgraphpackage=Package("subgraph", pkg_metainfo)

    #We build a subgraph

    sgfactory = SubGraphFactory(pkgmanager, name="sg1",
                                desc= "Subgraph Exemple",
                                cat = "Subgraphs",
                                )

    # build the subgraph factory

    addid = sgfactory.add_nodefactory ("simpleop", "add")
    val1id = sgfactory.add_nodefactory ("simpleop", "val")
    val2id = sgfactory.add_nodefactory ("simpleop", "val")
    val3id = sgfactory.add_nodefactory ("simpleop", "val")

    sgfactory.connect (val1id, 0, addid, 0)
    sgfactory.connect (val2id, 0, addid, 1)
    sgfactory.connect (addid, 0, val3id, 0)

    subgraphpackage.add_nodefactory(sgfactory)


    pkgmanager.add_package(oppackage)
    pkgmanager.add_package(subgraphpackage)

    return (oppackage, subgraphpackage)

        



    
