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

#import openalea.library as library

from pkgreader import OpenAleaWriter


# Exceptions 


class UnknowFileType(Exception):
    pass


###############################################################################

class PackageManager(object):
    """
    The PackageManager registers, and provide packages in a dictionnary
    The package manager is a singleton
    """

    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    
    def __init__ (self):

        # list of path to search wralea file
        self.wraleapath = [ '.' ] + openalea.__path__ #+ library.__path__
        
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

        
    def get_config_file (self):
        """ Return the system config file """

        envhome = ''
        if 'HOME' in os.environ:
            envhome = os.environ['HOME']
        elif 'HOMEDRIVE' in os.environ and 'HOMEPATH' in os.environ:
            envhome = os.path.join(os.environ['HOMEDRIVE'], os.environ['HOMEPATH'])

        if envhome:
            return os.path.join(envhome, '.openalea.xml')

        else :
            return None


    def clear(self):
        """ Remove all packages """
        self.pkgs = {}
    

    # Sys Path Functions
    def add_wraleapath(self, new_path):

        if(not new_path in self.wraleapath):
            self.wraleapath.append(new_path)
        
#         if(not new_path in sys.path):
#             sys.path.append(new_path)


#     def update_syspath (self):

#         self.recover_syspath()
        
#         for p in self.wraleapath:
#             if(not p in sys.path):
#                 sys.path.append(p)


    def recover_syspath (self):
        sys.path=self.old_syspath

    # Accessors

    def add_package(self, package):
        """ Add a package to the pkg manager """

        self[ package.get_id() ] = package
        self.update_category(package)


    # Category management

    def update_category(self, package):
        """ Update the category dictionnay with package contents """
        
        for nf in package.values():

            if(not nf.category) : nf.category = "Unclassified"

            try:
                self.category[nf.category].append( FactoryDesc(package, nf) )
            except KeyError:
                newcategory = Category()
                self.category[nf.category] = newcategory
                newcategory.append( FactoryDesc(package, nf) )


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
        return reader.register_packages(self)
        
    
    def find_wralea_files (self):
        """
        Find on the system all wralea.py, wralea.xml files
        Return a list of pkg readers
        """

        from tools.path import path

        readers = {}

        for wp in self.wraleapath:

            if(not os.path.isdir(wp)): continue
            
            filelist = []
            p = path(wp)

            # search for wralea.py
            map(filelist.append, p.walkfiles("wralea.py"))
            map(filelist.append, p.walkfiles("wralea.xml"))

            for f in filelist:

                # avoid doublons
                if(not readers.has_key(f)):
                    print "find %s" % (f,)
                    reader = self.get_pkgreader(f)
                    readers[f] = reader

        return readers.values()


    def get_pkgreader(self, filename):
        """ Return the pkg reader corresponding to the filename """

        from pkgreader import XmlPackageReader, PyPackageReader

        reader = None
        if(filename.endswith('.py')):
            reader = PyPackageReader(filename)
        elif(filename.endswith('.xml')):
            reader = XmlPackageReader(filename)

        else : raise UnknowFileType()

        return reader


    def find_and_register_packages (self):
        """ Find all wralea on the system and register them """
        
        readerlist=self.find_wralea_files()

        for pkgreader in readerlist:
            pkgreader.register_packages(self)


    def save_config (self, filename=None):
        """ Save configuration (package index and wralea paths)
        if filename is None, use default config file
        """

        if(filename == None):
            filename = self.get_config_file()

        writer = OpenAleaWriter(self)
        writer.write_config(filename)


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



class Category(list):
    """ Annex class to sort NodeFactory by category """
    pass


class FactoryDesc:
    """ Factory description """

    def __init__(self, package, factory):

        self.package = package
        self.factory = factory
