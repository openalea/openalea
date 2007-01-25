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
        self.clear()

       
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

        self.session_filename = None

        # map between (pkg_id, node_id) : node_instance
        self.workspaces = {}


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
        
        pkg.add_factory(rootfactory)
        self.pkgmanager.add_package(pkg)

        

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
            


class workspace(object):
    """
    A workspace contain a node
    and has threaded execution capabilities
    """


    def __init__(self, node):

        self.node = node
        self.is_running = False

    def single_run(self):
        """
        Run the node one time
        start_id, is the subnode id to execute (if any)
        """

        if(not self.is_running):
            self.node.eval()

    def start_continuous_execution(self):
        """ Continuous execution """

        if(not self.is_running):
            # Start the thread
            
            self.is_running = True

    def stop_continuous_execution(self):

        if(self.is_running):
            # Stop the thread
            
            self.is_running = False
        
        
