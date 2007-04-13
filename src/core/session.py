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
Session regroups all the data which can be stored between different executions
of the system.
"""

__license__= "Cecill-C"
__revision__=" $Id$ "


from compositenode import CompositeNodeFactory
from pkgmanager import PackageManager
from package import Package, UserPackage
from observer import Observed
from datapool import DataPool



class Session(Observed):
    """
    A session is composed by different workspaces, and an user package.
    A workspace is an open node
    A session can be saved on disk.
    """

    USR_PKG_NAME = "My Package"

    def __init__(self):

        Observed.__init__(self)

        # Instantiate a Package Manager
        self.pkgmanager = PackageManager()

        self.workspaces = []
        self.datapool = DataPool()
        self.clear()

       
    def add_workspace(self, compositenode, notify=True):
        """ Open a new workspace in the session"""

        if(compositenode not in self.workspaces):
            self.workspaces.append(compositenode)
            if(notify): self.notify_listeners()
        return compositenode
    

    def close_workspace(self, index, notify=True):
        """ Close workspace at index """
        try:
            del(self.workspaces[index])
            if(notify) : self.notify_listeners()
        except:
            pass


    def clear(self, create_workspace = True):
        """ Reinit Session """

        self.session_filename = None

        self.workspaces = []
        
        self.datapool.clear()

        # init pkgmanager
        self.pkgmanager.clear()
        self.pkgmanager.find_and_register_packages()
        
        # Create user package if needed
        if(not self.pkgmanager.has_key(self.USR_PKG_NAME)):
            self.pkgmanager.create_user_package(self.USR_PKG_NAME, {})

        self.user_pkg = self.pkgmanager[self.USR_PKG_NAME]

        if(create_workspace and not self.user_pkg.has_key('Workspace')):
            rootfactory = CompositeNodeFactory(self.pkgmanager, name="Workspace",
                                          description= "",
                                          category = "",
                                          )
        
            self.user_pkg.add_factory(rootfactory)

        self.notify_listeners()

        

    def load(self, filename):
        """ Load session data from filename """

        self.clear(False)
        
        self.session_filename = filename
        self.notify_listeners()
                

    def save(self, filename = None):
        """
        Save session in filename
        user_pkg and workspaces data are saved
        """

        if(filename == None):
            filename = self.session_filename


        self.session_filename = filename


    

