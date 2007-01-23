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
###############################################################################

__doc__="""
This module defines the session classes
"""

__license__= "Cecill-C"
__revision__=" $Id$ "

from openalea.core.core import Package
from openalea.core.subgraph import SubGraphFactory

from pkgreader import SessionWriter, XmlPackageReader


class Session:
    """
    A session is composed by different workspaces, and a user package
    A session is persistant
    """

    USR_PKG_NAME = "MyObjects"

    def __init__(self, pkgmanager):

        self.session_filename = None
        
        # map between (pkg_id, node_id) : node_instance
        self.workspaces = {}
        
        self.pkgmanager = pkgmanager
        # init pkgmanager
        pkgmanager.clear()
        pkgmanager.find_and_register_packages()


        # Create user package
        pkg_metainfo = {}
        pkg = Package(self.USR_PKG_NAME, pkg_metainfo)
        self.user_pkg = pkg

        rootfactory = SubGraphFactory(pkgmanager, name="Workspace",
                                      description= "",
                                      category = "",
                                      )
        
        pkg.add_factory(rootfactory)
        pkgmanager.add_package(pkg)

        


    def add_workspace(self, factory):
        """
        Instanciate a new node
        Return node_instance
        """

        # We open only one workspace by factory
        # To avoid synchronisation between them
        if(self.workspaces.has_key(factory)):
            return self.workspaces[factory]
        
        node = factory.instantiate()
        self.workspaces[factory] = node

        return node


    def close_workspace(self, factory):
        try:
            del(self.workspaces[factory])
        except:
            pass


    def clear(self):
        """ Reinit Session """

        self.__init__(self.pkgmanager)
        

    def load(self, filename):
        """ load session data from filename """

        self.clear()
        
        reader = XmlPackageReader(filename)
        reader.register_packages(self.pkgmanager)
        #reader.register_session(self)

        self.user_pkg = self.pkgmanager[self.USR_PKG_NAME]

        self.add_workspace(self.user_pkg['Workspace'])
        
        self.session_filename = filename
                

    def save(self, filename = None):
        """
        Save session in filename
        user_pkg  and workspaces data are saved
        """

        if(filename == None):
            filename = self.session_filename

        writer = SessionWriter(self)
        writer.write_config(filename)

        self.session_filename = filename
            
