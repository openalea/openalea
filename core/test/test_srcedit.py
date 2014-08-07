#
#       OpenAlea.Core: OpenAlea Core
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
"""Test the node src edition"""

__license__ = "Cecill-C"
__revision__ = " $Id$ "

import os
import openalea
from openalea.core.pkgmanager import PackageManager
from openalea.core.node import RecursionError
from openalea.core import Package


def setup_func():
    """ Create test_module  and wralea """

    modsrc = \
           """
from openalea.core import *

class MyNode:

    def __init__(self):
        pass


    def __call__(self, inputs):
        return inputs
"""

    file = open("mymodule.py", 'w')
    file.write(modsrc)
    file.close()


    wraleasrc = \
    """
from openalea.core import *


def register_packages(pkgmanager):
    metainfo={ }
    package1 = Package("TestPackage", metainfo)

    f = Factory( name= "test",
                 category = "",
                 description = "",
                 nodemodule = "mymodule",
                 nodeclass = "MyNode",

                 )

    package1.add_factory(f)

    pkgmanager.add_package(package1)
"""

    file = open("my_wralea.py", 'w')
    file.write(wraleasrc)
    file.close()


def teardown_func():
    """ Delete created files """
    try:
        os.remove("my_wralea.py")
    except:
        pass
    try:
        os.remove("mymodule.py")
    except:
        pass

from nose import with_setup


@with_setup(setup_func, teardown_func)
def test_srcedit():
    """ Test src edition """

    # Change src
    pm = PackageManager()
    pm.wraleapath = '.'

    pm.init()
    factory = pm['TestPackage']['test']

    node1 = factory.instantiate()
    assert node1.func((1, 2, 3)) == (1, 2, 3)

    src = factory.get_node_src()
    assert src

    newsrc = src.replace("return inputs", "return sum(inputs)")
    assert newsrc

    factory.apply_new_src(newsrc)
    node2 = factory.instantiate()
    assert node2.func((1, 2, 3)) == 6

    factory.save_new_src(newsrc)

    src = factory.get_node_src()
    print src

    return

    # Reinit src
    pm = PackageManager()
    pm.wraleapath = '.'

    pm.init()

    factory = pm['TestPackage']['test']

    node = factory.instantiate()

    assert node(((1, 2, 3), )) == 6
