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
This module defines the session and datapool classes
"""

__license__= "Cecill-C"
__revision__=" $Id$ "

from openalea.core.core import Package
from openalea.core.subgraph import SubGraphFactory
from openalea.core.pkgmanager import PackageManager

from pkgreader import SessionWriter, XmlPackageReader

from openalea.core.observer import Observed

class Session(Observed):
    """
    A session is composed by different workspaces, and an user package.
    A session can be saved on disk.
    """

    USR_PKG_NAME = "MyObjects"

    def __init__(self):

        Observed.__init__(self)

        # Instantiate a Package Manager
        self.pkgmanager = PackageManager()

        self.workspaces = []
        self.datapool = DataPool()
        self.clear()

       
    def add_workspace(self, node):
        """ Open a new workspace to the session containing a node """

        self.workspaces.append(node)
        self.notify_listeners()
        return node


    def close_workspace(self, index):
        """ Close workspace at index """
        try:
            del(self.workspaces[index])
            self.notify_listeners()
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


        # Create user package
        pkg_metainfo = {}
        pkg = Package(self.USR_PKG_NAME, pkg_metainfo)
        self.user_pkg = pkg


        if(create_workspace):
            rootfactory = SubGraphFactory(self.pkgmanager, name="Workspace",
                                          description= "",
                                          category = "",
                                          )
        
            self.user_pkg.add_factory(rootfactory)

        self.pkgmanager.add_package(pkg)
        self.notify_listeners()

        

    def load(self, filename):
        """ Load session data from filename """

        self.clear(False)
        
        reader = XmlPackageReader(filename)
        reader.register_packages(self.pkgmanager)
        reader.register_session(self)

        self.user_pkg = self.pkgmanager[self.USR_PKG_NAME]
        
        self.session_filename = filename
        self.notify_listeners()
                

    def save(self, filename = None):
        """
        Save session in filename
        user_pkg and workspaces data are saved
        """

        if(filename == None):
            filename = self.session_filename

        writer = SessionWriter(self)
        writer.write_config(filename)

        self.session_filename = filename


#     def new_network(self, name, nin, nout, category, description):
#         """ Create a new graph in the user package """
#         pass
    

from openalea.core.singleton import Singleton

class DataPool(Observed):
    """ Dictionnary of session data """

    __metaclass__ = Singleton

    def __init__(self):

        Observed.__init__(self)
        self.data = {}

        
    def add_data(self, key, instance):
        """ Add an instance referenced by key to the data pool """

        self.data[key] = instance
        self.notify_listeners(('pool_modified',))

    def remove_data(self, key):
        """ Remove the instance identified by key """

        try:
            del(self.data[key])
            self.notify_listeners(('pool_modified',))
        except:
            pass

    def clear(self):
        ret = self.data.clear()
        self.notify_listeners(('pool_modified',))
        return ret

    def __getitem__(self, key):
        return self.data[key]
    
    def __setitem__(self, key, val):
        self.data[key] = val
        self.notify_listeners(('pool_modified',))

    def __len__(self):
        return len(self.data)

    def keys(self):
        return self.data.keys()

    def items(self):
        return self.data.items()

    def values(self):
        return self.data.values()
