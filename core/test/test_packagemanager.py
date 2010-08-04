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
#
"""Test the Package Manager"""
from openalea.core.pkgmanager import PackageManager
import os
import openalea
from openalea.core.settings import Settings


def test_wraleapath():
    """test wraleapath"""
    pkgman = PackageManager()

# this option (include_namespace has been removed)
#    assert bool(openalea.__path__[0] in  \
#      pkgman.get_wralea_path()) == pkgman.include_namespace

    if(os.name == 'posix'):
        pkgman.add_wralea_path("/usr/bin", \
            pkgman.user_wralea_path)
        assert "/usr/bin" in pkgman.get_wralea_path()
    else:
        pkgman.add_wralea_path("C:\\Windows", \
            pkgman.user_wralea_path)
        assert "C:\\Windows" in pkgman.get_wralea_path()


def test_load_pm():
    pkgman = PackageManager()
    pkgman.init()

    simpleop = pkgman["openalea.flow control"]
    assert simpleop

    addfactory = simpleop.get_factory('command')
    assert addfactory != None
    assert addfactory.instantiate()

    valfactory = simpleop.get_factory('rendez vous')
    assert valfactory != None


def test_category():

    pkgman = PackageManager()

    pkgman.init()
    pkgman.find_and_register_packages()

    # test if factory are dedoubled
    for cat in pkgman.category.values():
        s = set()
        for factory in cat:
            assert not factory in s
            s.add(factory)


def test_search():

    pkgman = PackageManager()
    pkgman.load_directory("./")

    assert 'Test' in pkgman

    res = pkgman.search_node("sum")
    print res
    assert "sum" in res[0].name


    # comment these 3 lines because system.command is not part
    # of any nodes anymore.
    #res = pkgman.search_node("system.command")
    #print res
    #assert "command" in res[0].name


def test_write_config():

    pkgman = PackageManager()
    pkgman.load_directory("./")
    pkgman.write_config()
    p = pkgman.user_wralea_path

    s = Settings()
    path = s.get("pkgmanager", "path")
    paths = list(eval(path)) # path is a string

    assert set(paths) == set(p)
