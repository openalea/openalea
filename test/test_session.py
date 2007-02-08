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
from openalea.core.subgraph import SubGraphFactory

import os
import openalea


def test_session():

    session = Session()
    pkgman = session.pkgmanager

    # user package is created
    assert pkgman.pkgs.has_key(Session.USR_PKG_NAME)
    
    # file is created
    session.save('savesession.xml')
    assert os.path.exists("savesession.xml")

    pkgman.clear()
    assert not pkgman.pkgs.has_key(Session.USR_PKG_NAME)
    assert len(pkgman.pkgs.keys())==0

    session.load('savesession.xml')
    assert pkgman.pkgs.has_key(Session.USR_PKG_NAME)
    assert session.user_pkg.has_key('Workspace')

    


def test_save():
    
    session = Session()
    
    sgfactory = SubGraphFactory(session.pkgmanager, name="SubGraphExample",
                                description= "Examples",
                                category = "Examples",
                                )

    # build the subgraph factory

    addid = sgfactory.add_nodefactory ('add1', ("Library", "add"))
    session.user_pkg.add_factory(sgfactory)

    session.save('testsave2.xml')

    session.clear()
    session.load('testsave2.xml')
    
    assert len(session.user_pkg.keys())==2



