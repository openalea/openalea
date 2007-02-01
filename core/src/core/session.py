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
from openalea.core.pkgmanager import PackageManager

from pkgreader import SessionWriter, XmlPackageReader


class Session:
    """
    A session is composed by different workspaces, and a user package
    A session is persistant
    """

    USR_PKG_NAME = "MyObjects"

    def __init__(self):

        self.pkgmanager = PackageManager()

        self.workspaces = []
        self.clear()

       
    def add_workspace(self, node):

        self.workspaces.append(node)

        return node


    def close_workspace(self, index):
        try:
            del(self.workspaces[index])
        except:
            pass


    def clear(self):
        """ Reinit Session """

        self.session_filename = None

        self.workspaces = []

        # init pkgmanager
        self.pkgmanager.clear()
        self.pkgmanager.find_and_register_packages()


        # Create user package
        pkg_metainfo = {}
        pkg = Package(self.USR_PKG_NAME, pkg_metainfo)
        self.user_pkg = pkg

        rootfactory = SubGraphFactory(self.pkgmanager, name="Workspace",
                                      description= "",
                                      category = "",
                                      )
        
        self.user_pkg.add_factory(rootfactory)

        self.pkgmanager.add_package(pkg)


        

    def load(self, filename):
        """ load session data from filename """

        self.clear()
        
        reader = XmlPackageReader(filename)
        reader.register_packages(self.pkgmanager)
        reader.register_session(self)

        self.user_pkg = self.pkgmanager[self.USR_PKG_NAME]
        
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


    def new_network(self, name, nin, nout, category, description):
        """ Create a new graph in the user package """
        pass
    
                    
            


class workspace(object):
    """
    Abstraction to represent a couple node/factory
    The user manipulates workspace without knowing if he
    interacts with the node (data) or the factory (description)
    or with a subgraph

    Workspaces provide the same functions for subgraph and for
    simple node. If graph operation occurs on simple node, an exception
    will be raised
    """

    def __init__(self, factory, node):

        self.factory = factory
        self.node = node

    # Subgraph Operations
    def add_node(self, **kargs):
        """
        @param pkg : package name
        @param category : category name
        @param name : factory id
        @param factory : factory instance

        @return : element id
        """
        pass

    def connect(src_id, src_port, dst_id, dst_port):
        pass

    # Node Operations
    def set_input(self, index, obj):
        pass

    def run(self, elt_id = None):
        pass
        
    
