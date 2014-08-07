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
"""Test evaluation alogrithm"""

__license__ = "Cecill-C"
__revision__ = " $Id$ "

def test_diamond_after_map():
    """ Tests that a diamond after a map evaluates only onces the map node.

          Map
         /   \
        N1   N2
         \   /
           +    #evaluation of + should only trigger one evaluation of Map.
    """

    from openalea.core import pkgmanager
    from os.path import join
    from os import getcwd

    pm = pkgmanager.PackageManager()
    pm.add_wralea_path(join(getcwd(), "pkg"), pm.user_wralea_path)
    pm.init()


    # -- get our factories--
    rangeFac = pm["pkg_test"]["range"]
    listFac  = pm["pkg_test"]["list"]
    mapFac   = pm["pkg_test"]["map"]
    addFac   = pm["pkg_test"]["+"]
    xFac     = pm["openalea.flow control"]["X"]

    # -- build our df --
    from openalea.core import compositenode

    df       = compositenode.CompositeNode()
    range_   = rangeFac.instantiate()
    map_     = mapFac.instantiate()
    loopAdd  = addFac.instantiate()
    finalAdd = addFac.instantiate()
    x        = xFac.instantiate()
    listleft = listFac.instantiate()
    listrght = listFac.instantiate()


    rId = df.add_node(range_)
    mId = df.add_node(map_)
    laId = df.add_node(loopAdd)
    faId = df.add_node(finalAdd)
    xId = df.add_node(x)
    llId = df.add_node(listleft)
    lrId = df.add_node(listrght)

    range_.set_input(1,10)
    df.connect(rId, 0, mId, 1)
    df.connect(xId, 0, laId, 0)
    df.connect(xId, 0, laId, 1)
    df.connect(laId, 0, mId, 0)
    df.connect(mId, 0, llId, 0)
    df.connect(mId, 0, lrId, 0)
    df.connect(llId, 0, faId, 0)
    df.connect(lrId, 0, faId, 1)

    df.eval_as_expression(faId)


#see test_compositenode.py
