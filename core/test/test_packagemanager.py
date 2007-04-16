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
Test the Package Manager
"""


from openalea.core.pkgmanager import PackageManager
import os
import openalea

# Test package manager configuration



def test_wraleapath():

    pkgman = PackageManager()
    assert openalea.__path__[0] in  pkgman.wraleapath
    pkgman.add_wraleapath("/usr/bin")

    assert "/usr/bin" in pkgman.wraleapath
                      


def test_load_pm():
    pkgman = PackageManager()
    pkgman.init()

    simpleop = pkgman["Library"]
    assert simpleop

    addfactory = simpleop.get_factory('int')
    assert addfactory != None
    assert addfactory.instantiate()

    valfactory = simpleop.get_factory('float')
    assert valfactory != None

   

def test_category():
    pkgman = PackageManager()

    pkgman.init()
    pkgman.find_and_register_packages()

    # test if factory are dedoubled
    for cat in pkgman.category.values():
        s = set()
        for factory in  cat:
            assert not factory.get_id() in s
            s.add(factory.get_id())


def test_search():
    pkgman = PackageManager()
    pkgman.add_wralea("test_wralea.py")

    assert pkgman.has_key('Test')

    res = pkgman.search_node("sum")
    assert len(res) == 1
    assert "sum" in res[0].name




                
            

