# -*- python -*-
#
#       OpenAlea.Core
#
#       Copyright 2006-2007 INRIA - CIRAD - INRA  
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
This module defines the package manager.
It is able to find installed package and their wralea.py
It stores the packages and nodes informations
"""

__license__= "Cecill-C"
__revision__=" $Id$ "

import openalea
import sys
import os
from singleton import Singleton
from package import UserPackage, PyPackageReader
from settings import get_userpkg_dir, Settings


# Exceptions 

class UnknowFileType(Exception):
    pass

###############################################################################

class PackageManager(object):
    """
    The PackageManager is a Dictionary of Packages
    It can locate OpenAlea packages on the system (with wralea).
    """

    __metaclass__ = Singleton

    def __init__ (self):
        

        # list of path to search wralea file
        self.set_default_wraleapath()

        # save system path
        self.old_syspath = sys.path[:]
        #self.update_syspath()

        # dictionnay of packages
        self.pkgs = {}

        # dictionnay of category
        self.category = {}

        self.read_config()


    def read_config(self):
        """ Read user config """

        config = Settings()
        
        try:
            str = config.get("pkgmanager", "path")
            l = eval(str)
            
            for p in l:
                self.add_wraleapath(os.path.abspath(p))
                
        except Exception, e:
            print e


    def write_config(self):
        """ Write user config """
        
        config = Settings()
        config.set("pkgmanager", "path", repr(list(self.wraleapath)))
        config.write_to_disk()


    def set_default_wraleapath(self):
        """ Return a list wralea path """

        self.wraleapath = set()
        l = list(openalea.__path__)
        for p in l :
            self.add_wraleapath(p)
        self.add_wraleapath(get_userpkg_dir())
        

    def init(self, filename=None):
        """ Initialize package
        If filename is None, find wralea files on the system
        else load filename
        """

        if (not filename):
            self.find_and_register_packages()
        else :
            self.add_wralea(filename)


    def unload_module(self):
        """ Remove all wralea module and invalidate others"""

        for name in sys.modules.keys():
            m = sys.modules[name]
            if(m) : m.oa_invalidate = True
        

        
    def clear(self):
        """ Remove all packages """

        self.pkgs = {}
        self.recover_syspath()
        self.category = {}
        

    # Path Functions
    def add_wraleapath(self, path):
        """
        Add a search path for wralea files
        @param path : a path string
        """

        if(not os.path.isdir(path)): return

        # Ensure to add a non existing path
        for p in self.wraleapath:
            common = os.path.commonprefix((p, path))
            # the path is already in wraleapth
            if(common == p): return
            # the new path is more generic, we keep it
            if(common == path):
                self.wraleapath.remove(p)
                self.wraleapath.add(path)
                return
        # the path is absent
        self.wraleapath.add(path)
        
        

    def recover_syspath(self):
        """ Restore the initial sys path """
        sys.path = self.old_syspath

    # Accessors

    def add_package(self, package):
        """ Add a package to the pkg manager """

        #if( not self.pkgs.has_key(package.get_id())):
        self[package.get_id()] = package
        self.update_category(package)


    # Category management
    def update_category(self, package):
        """ Update the category dictionary with package contents """
        
        for nf in package.values():
            if not nf.category: 
                nf.category = "Unclassified"

            self.category.setdefault(nf.category, 
                                     Category(nf.category)).add(nf)


    def rebuild_category(self):
        """ Rebuild all the category """

        self.category = {}
        for p in self.values():
            self.update_category(p)
        

    # Wralea functions
    def add_wralea(self, filename):
        """ Execute a wralea file 
        Return the registered packages
        """

        filename = os.path.abspath(filename)
        
        if(not os.path.exists(filename) or
           not os.path.isfile(filename)):
            print "Wralea : %s does not exists."%(filename,)
            return

        # Update wralea path if necessary
        path = os.path.dirname(filename)
        self.add_wraleapath(path)
        
        reader = self.get_pkgreader(filename)
        if reader: 
            return reader.register_packages(self)
        else:
            print "Unable to load package %s."%(filename,)
            return None
        
    
    def find_wralea_files (self):
        """
        Find on the system all wralea.py, wralea.xml files
        @return : a list of pkgreader instances
        """

        from path import path

        wralea_files= set()
        for wp in self.wraleapath:
            if(not os.path.isdir(wp)):
                continue
            
            p= path(wp).abspath()

            # search for wralea.py
            wralea_files.update( p.walkfiles("*wralea.py") )
            #wralea_files.update( p.walkfiles("*wralea.xml") )

        for f in wralea_files:
            print "Package Manager : found %s" % f
            
        return map( self.get_pkgreader, wralea_files)


    def get_pkgreader(self, filename):
        """ Return the pkg reader corresponding to the filename """

        reader = None
        if(filename.endswith('.py')):
            reader = PyPackageReader(filename)
        else :
            raise UnknowFileType()

        return reader


    def find_and_register_packages (self):
        """ Find all wralea on the system and register them """
        
        readerlist = self.find_wralea_files()

        [x.register_packages(self) for x in readerlist]

        self.rebuild_category()


    def create_user_package(self, name, metainfo, path=None):
        """
        Create a new package in the user space and register it
        Return the created package
        """

        if(self.pkgs.has_key(name)):
            return self.pkgs[name]

        # Create directory
        if(not path):
            path = get_userpkg_dir()
            path = os.path.join(path, name)
        
        if(not os.path.isdir(path)):
            os.mkdir(path)


        # Create new Package and its wralea
        p = UserPackage(name, metainfo, path)
        p.write()

        # Register package
        self.add_wralea(p.get_wralea_path())
        self.write_config()
        return p


    def get_user_packages(self):
        """ Return the list of user packages """

        return [x for x in self.pkgs.values() if isinstance(x, UserPackage)]
       

    # Dictionnary behaviour
      
    def __getitem__(self, key):
        return self.pkgs[key]

    def __setitem__(self, key, val):
        self.pkgs[key] = val

    def __len__(self):
        return len(self.pkgs)

    def keys(self):
        return self.pkgs.keys()

    def items(self):
        return self.pkgs.items()

    def values(self):
        return self.pkgs.values()

    def has_key(self, *args):
        return self.pkgs.has_key(*args)


    # Convenience functions
    def get_node(self, pkg_id, factory_id):
        """ Return a node instance giving a pkg_id and a factory_id """
        pkg = self[pkg_id]
        factory = pkg[factory_id]
        return factory.instantiate()


    def search_node(self, search_str):
        """ Return a list of Factory corresponding to search_str """

        search_str = search_str.upper()
        ret = [ factory \
                for pkg in self.values() \
                for factory  in pkg.values() \
                if(search_str in pkg.name.upper() or
                   search_str in factory.name.upper() or
                   search_str in factory.description.upper() or
                   search_str in factory.category.upper()) ]
            
        return ret



class Category(set):
    """ Annex class to sort NodeFactory by category """

    def __init__(self, category_name):
        self.category = category_name

    def get_id(self):
        return self.category

    def get_tip(self):
        return ""


