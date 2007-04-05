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

    USR_PKG_NAME = "My Packages"

    def __init__(self):

        Observed.__init__(self)

        # Instantiate a Package Manager
        self.pkgmanager = PackageManager()

        # Create user package if needed
        if(not self.pkgmanager.has_key(self.USR_PKG_NAME)):
            pkg_metainfo = {}
            pkg = Package(self.USR_PKG_NAME, pkg_metainfo)
            self.pkgmanager.add_package(pkg)


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


        self.user_pkg = self.pkgmanager[self.USR_PKG_NAME]

        if(create_workspace and not self.user_pkg.has_key('Workspace')):
            rootfactory = SubGraphFactory(self.pkgmanager, name="Workspace",
                                          description= "",
                                          category = "",
                                          )
        
            self.user_pkg.add_factory(rootfactory)

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


    

from openalea.core.singleton import Singleton

# Decorator to add notification to function
def notify_decorator(f):
    
    def wrapped(self, *args, **kargs):
        ret = f(self, *args, **kargs)
        self.notify_listeners(('pool_modified',))
        return ret
    wrapped.__doc__ = f.__doc__

    return wrapped


class DataPool(Observed, dict):
    """ Dictionnary of session data """

    __metaclass__ = Singleton


    def __init__(self):

        Observed.__init__(self)
        dict.__init__(self)
        
        DataPool.__setitem__ = notify_decorator(dict.__setitem__)
        DataPool.__delitem__ = notify_decorator(dict.__delitem__)
        DataPool.clear = notify_decorator(dict.clear)

        
        
    def add_data(self, key, instance):
        """ Add an instance referenced by key to the data pool """

        self[key] = instance
        self.notify_listeners(('pool_modified',))

    def remove_data(self, key):
        """ Remove the instance identified by key """

        try:
            del(self[key])
            self.notify_listeners(('pool_modified',))
        except:
            pass

