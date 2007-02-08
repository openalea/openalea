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

    addfactory = simpleop.get_factory('add')
    assert addfactory != None
    assert addfactory.instantiate()

    valfactory = simpleop.get_factory('float')
    assert valfactory != None

   

def test_category():
    pass
