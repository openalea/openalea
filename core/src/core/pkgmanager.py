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
This module defines the package manager.
It is able to find installed package and their wralea.py
It stores the packages and nodes informations
"""

__license__= "Cecill-C"
__revision__=" $Id$ "


import sys
import os
import openalea


# Exceptions 

class UnknowFileType(Exception):
    pass

###############################################################################

class PackageManager(object):
    """
    The PackageManager is a Dictionary of Packages
    It can locate OpenAlea packages on the system (with wralea)
    """

    def __init__ (self):

        # list of path to search wralea file
        self.wraleapath = list(openalea.__path__)
        
        # save system path
        self.old_syspath = sys.path[:]
        #self.update_syspath()

        # dictionnay of packages
        self.pkgs = {}

        # dictionnay of category
        self.category = {}


    def init(self, filename=None):
        """ Initialize package
        If filename is None, find wralea files on the system
        else load filename
        """

        if (not filename):
            self.find_and_register_packages()
        else :
            self.add_wralea(filename)

        
    def clear(self):
        """ Remove all packages """
        self.pkgs = {}
        self.recover_syspath()
        self.category = {}

        self.wraleapath = openalea.__path__ 

    # Path Functions
    def add_wraleapath(self, new_path):
        """
        Add a search path for wralea files
        @param new_path : a path string
        """
        if(not new_path in self.wraleapath):
            self.wraleapath.append(new_path)
        

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

            if(not nf.category) : nf.category = "Unclassified"

            try:
                if(not (nf in self.category[nf.category])):
                    self.category[nf.category].add( nf )
                
            except KeyError:
                newcategory = Category(nf.category)
                self.category[nf.category] = newcategory
                newcategory.add( nf )


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

        if(not os.path.exists(filename)):
            print "Wralea : %s does not exists."%(filename,)
            return
        
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
            wralea_files.update( p.walkfiles("wralea.py") )
            wralea_files.update( p.walkfiles("wralea.xml") )

        for f in wralea_files:
            print "Package Manager : found %s" % f
            
        return map( self.get_pkgreader, wralea_files)


    def get_pkgreader(self, filename):
        """ Return the pkg reader corresponding to the filename """

        from pkgreader import XmlPackageReader, PyPackageReader

        reader = None
        if(filename.endswith('.py')):
            reader = PyPackageReader(filename)
        elif(filename.endswith('.xml')):
            reader = XmlPackageReader(filename)
        else :
            raise UnknowFileType()

        return reader


    def find_and_register_packages (self):
        """ Find all wralea on the system and register them """
        
        readerlist=self.find_wralea_files()

        [x.register_packages(self) for x in readerlist]

        self.rebuild_category()


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

    # Convenience functions
    def get_node(self, pkg_id, factory_id):
        """ Return a node instance giving a pkg_id and a factory_id """
        pkg = self[pkg_id]
        factory = pkg[factory_id]
        return factory.instantiate()

    def search_node(self, search_str):
        """ Return a list of Factory corresponding to search_str """

        ret = []

        ret = [ factory \
                for pkg in self.values() \
                for factory  in pkg.values() \
                if(search_str in factory.name)]
            
        return ret



class Category(set):
    """ Annex class to sort NodeFactory by category """

    def __init__(self, category_name):
        self.category = category_name

    def get_id(self):
        return self.category

    def get_tip(self):
        return ""


