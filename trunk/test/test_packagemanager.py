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

import os
pj=os.path.join
import sys
sys.path.append(pj("..","src"))

from pkgmanager import PackageManager


import openalea

# Test package manager configuration

def test_config():

    #Empty Config
    pkgman = PackageManager()
    pkgman.save_config("test.xml")

    assert(os.path.exists("test.xml"))

    os.remove("test.xml")

def test_wraleapath():

    pkgman = PackageManager()
    assert len ( pkgman.wraleapath ) == 2
    pkgman.add_wraleapath("/usr/bin")
    pkgman.save_config("test.xml")

    pkgman=PackageManager()
    import openalea
    assert openalea.__path__[0] in pkgman.wraleapath
    assert "." in pkgman.wraleapath
    pkgman.add_wralea("test.xml")
                      
    assert "/usr/bin" in pkgman.wraleapath
                      
    os.remove("test.xml")


def test_add_py():
    pkgman = PackageManager()
    pkgman.add_wralea("wralea.py")


    assert len(pkgman) == 2

    simpleop = pkgman["simpleop"]
    assert simpleop

    subgraph = pkgman["subgraph"]
    assert subgraph

    from simpleop import Add, Value
    addfactory = simpleop.get_nodefactory('add')
    assert addfactory != None
    assert addfactory.doc == Add.__doc__
    assert addfactory.instantiate()

    valfactory = simpleop.get_nodefactory('val')
    assert valfactory != None

   
    pkgman.save_config("test.xml")

    

def test_add_xml():

    pkgman = PackageManager()
    pkgman.add_wralea("wralea.xml")

    assert len(pkgman) == 2

    simpleop = pkgman["simpleop"]
    
    subgraph = pkgman["subgraph"]
    assert subgraph

    pkgman.save_config("test.xml")

def test_find_wralea():
     pkgman=PackageManager()
     pkgman.init()

     assert len(pkgman) == 2
     pkgman.save_config("test.xml")



