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
    The PackageManager registers, and provide packages in a dictionnary
    """

#     # The package manager is a singleton

#     __instance = None

#     def __new__(cls):
#         if cls.__instance is None:
#             cls.__instance = object.__new__(cls)
#         return cls.__instance

    
    def __init__ (self):

        # list of path to search wralea file
        self.wraleapath = [ '.' ] + openalea.__path__
        
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

        
#     def get_configfile (self):
#         """ Return the system config file """

#         envhome = ''
#         if 'HOME' in os.environ:
#             envhome = os.environ['HOME']
#         elif 'HOMEDRIVE' in os.environ and 'HOMEPATH' in os.environ:
#             envhome = os.path.join(os.environ['HOMEDRIVE'], os.environ['HOMEPATH'])

#         if envhome:
#             return os.path.join(envhome, '.openalea.xml')

#         else :
#             return None


    def clear(self):
        """ Remove all packages """
        self.pkgs = {}
        self.recover_syspath()
        self.category = {}

        self.wraleapath = [ '.' ] + openalea.__path__ 
    

    # Path Functions
    def add_wraleapath(self, new_path):

        if(not new_path in self.wraleapath):
            self.wraleapath.append(new_path)
        

    def recover_syspath (self):
        sys.path=self.old_syspath

    # Accessors

    def add_package(self, package):
        """ Add a package to the pkg manager """

        #if( not self.pkgs.has_key(package.get_id())):
        self[ package.get_id() ] = package
        self.update_category(package)


    # Category management

    def update_category(self, package):
        """ Update the category dictionnay with package contents """
        
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
            print "%s does not exists."%(filename,)
            return
        
        reader = self.get_pkgreader(filename)
        if reader: 
            return reader.register_packages(self)
        else:
            print "Unable to load pakahe %s."%(filename,)
            return None
        
    
    def find_wralea_files (self):
        """
        Find on the system all wralea.py, wralea.xml files
        Return a list of pkg readers
        """

        from tools.path import path

        wralea_files= set()
        for wp in self.wraleapath:

            if(not os.path.isdir(wp)):
                continue
            
            p= path(wp).abspath()

            # search for wralea.py
            wralea_files.update( p.walkfiles("wralea.py") )
            wralea_files.update( p.walkfiles("wralea.xml") )

        for f in wralea_files:
            print "find %s" % f
            
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

        for pkgreader in readerlist:
            pkgreader.register_packages(self)


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



class Category(set):
    """ Annex class to sort NodeFactory by category """

    def __init__(self, category_name):
        self.category = category_name

    def get_id(self):
        return self.category

    def get_tip(self):
        return ""


