# -*- python -*-
#
#       OpenAlea.Core: OpenAlea Core
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
###############################################################################

__doc__="""
Session regroups all the data which can be stored between different executions
of the system.
"""

__license__= "Cecill-C"
__revision__=" $Id$ "


import os, sys

from compositenode import CompositeNodeFactory,CompositeNode
from pkgmanager import PackageManager
from package import Package, UserPackage
from observer import Observed
from datapool import DataPool

import shelve



class Session(Observed):
    """
    A session is composed by different workspaces, and an user package.
    A workspace is an open node
    A session can be saved on disk.
    """

    USR_PKG_NAME = "My Package"

    def __init__(self):

        Observed.__init__(self)
        
        self.workspaces = []
        self.datapool = DataPool()

        self.pkgmanager = PackageManager()

        self.empty_cnode_factory = CompositeNodeFactory("Workspace")

        self.clear()

       
    def add_workspace(self, compositenode=None, notify=True):
        """
        Open a new workspace in the session
        if compositenode = None, create a new empty compositenode
        """
        
        if(not compositenode):
            compositenode = self.empty_cnode_factory.instantiate()
            compositenode.set_caption("")
            self.workspaces.append(compositenode)

        elif(compositenode not in self.workspaces):
            self.workspaces.append(compositenode)

        if(notify): self.notify_listeners()
            
        return compositenode
    

    def close_workspace(self, index, notify=True):
        """ Close workspace at index """

        del(self.workspaces[index])
        if(notify) : self.notify_listeners()
        

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

        if(create_workspace):
            self.add_workspace()
            
        self.notify_listeners()

        
    def save(self, filename = None):
        """
        Save session in filename
        user_pkg and workspaces data are saved
        """

        if(filename):
            self.session_filename = filename

        d = shelve.open(self.session_filename)

        # modules
        modules_path = []
        for k in sys.modules.keys():
            m = sys.modules[k]
            if hasattr(m, '__file__'):
                modules_path.append((m.__name__, os.path.abspath(m.__file__)))
                
        d['__modules__'] = modules_path

        # datapool
        d['datapool'] = self.datapool

        # workspaces
        d['workspaces'] = self.workspaces

        d.close()


    def load(self, filename):
        """ Load session data from filename """

        self.clear(False)
        
        self.session_filename = filename

        d = shelve.open(self.session_filename)

        # modules
        modules = d['__modules__']

        for name, path in modules:
            self.load_module(name, path)

        # datapool
        self.datapool.update(d['datapool'])

        # workspaces
        workspaces = d['workspaces']
        for n in  workspaces:
            self.workspaces.append(n)

        self.notify_listeners()
        

    def load_module(self, name, path):

        import imp
        if(name in sys.modules.keys()) : return
        lastname = name.rsplit('.', 1)[-1]
        if(not os.path.isdir(path)):
            path = os.path.dirname(path)

        try:
            (file, filename, desc) = imp.find_module(lastname, [path])
            imp.load_module(name, file, filename, desc)
        except Exception, e:
            pass

        


    

