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
    assert len ( pkgman.wraleapath ) == 3
    pkgman.add_wraleapath("/usr/bin")

    assert "/usr/bin" in pkgman.wraleapath
                      


def test_load_pm():
    pkgman = PackageManager()
    pkgman.init()

    simpleop = pkgman["arithmetics"]
    assert simpleop

    addfactory = simpleop.get_nodefactory('add')
    assert addfactory != None
    assert addfactory.instantiate()

    valfactory = simpleop.get_nodefactory('val')
    assert valfactory != None

   

# def test_find_wralea():
#      pkgman=PackageManager()
#      pkgman.init()

#      assert len(pkgman) == 2
#      pkgman.save_config("test.xml")


# def test_config():

#     #Empty Config
#     pkgman = PackageManager()
#     pkgman.save_config("test.xml")

#     assert(os.path.exists("test.xml"))
#     os.remove("test.xml")


