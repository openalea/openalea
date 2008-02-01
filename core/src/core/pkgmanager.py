# -*- python -*-
#
#       OpenAlea.Core
#
#       Copyright 2006-2007 INRIA - CIRAD - INRA  
#
#       File author(s): Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#                       Christophe Pradal <christophe.prada@cirad.fr>
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
from package import UserPackage, PyPackageReader, PyPackageReaderWralea
from settings import get_userpkg_dir, Settings
from pkg_resources import iter_entry_points
from nocasedict import NoCaseDict

# Exceptions 

class UnknowFileType(Exception):
    pass

class UnknownPackageError (Exception):
    def __init__(self, name):
        Exception.__init__(self)
        self.message = "Cannot find package : %s"%(name)

    def __str__(self):
        return self.message



###############################################################################

class PackageManager(object):
    """
    The PackageManager is a Dictionary of Packages
    It can locate OpenAlea packages on the system (with wralea).
    """

    __metaclass__ = Singleton

    def __init__ (self):
        """ Constructor """
        
        self.include_namespace = self.get_include_namespace()

        # save system path
        self.old_syspath = sys.path[:]

        # dictionnary of packages
        self.pkgs = NoCaseDict()

        # dictionnary of category
        self.category = PseudoGroup("")
        
        # list of path to search wralea file
        self.set_default_wraleapath()
        self.read_wralea_path()


    def get_include_namespace(self):
        """ Read user config and return include namespace status """

        config = Settings()

        # include namespace
        try:
            str = config.get("pkgmanager", "include_namespace")
            self.include_namespace = bool(eval(str))
            
        except:
            self.include_namespace = False

        return self.include_namespace


    def read_wralea_path(self):
        """ Read user config """

        config = Settings()

        # wralea path
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
        config.set("pkgmanager", "include_namespace", repr(self.include_namespace))
        config.write_to_disk()


    def set_default_wraleapath(self):
        """ Define the default wralea search path """
        
        self.wraleapath = set()

        # Use setuptools entry_point
        for epoint in iter_entry_points("wralea"):
            base = epoint.dist.location
            m = epoint.module_name.split('.')
            p = os.path.join(base, *m)
            print "Wralea entry point: ", p
            self.add_wraleapath(p)

        # Search in openalea namespace
        if(self.include_namespace):
            l = list(openalea.__path__)
            for p in l :
                self.add_wraleapath(p)

        self.add_wraleapath(os.path.dirname(__file__))
        self.add_wraleapath(get_userpkg_dir())
        

    def init(self, dirname=None):
        """ Initialize package
        If dirname is None, find wralea files on the system
        else load directory
        """

        if (not dirname):
            self.find_and_register_packages()
        else :
            self.load_directory(dirname)    


    def reload(self):
        """ Reload all packages """

        self.clear()
        self.find_and_register_packages()
        for p in self.pkgs.values():
            p.reload()
        
        
    def clear(self):
        """ Remove all packages """

        self.pkgs = NoCaseDict()
        self.recover_syspath()
        self.category = PseudoGroup('Root')
        

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


    def get_pseudo_pkg(self):
        """ Return a pseudopackage structure """

        pt = PseudoPackage('Root')
        for k, v in self.pkgs.iteritems():
            pt.add_name(k, v)

        return pt

    
    def get_pseudo_cat(self):
        """ Return a pseudocategory structure """
        return self.category 


    # Category management
    def update_category(self, package):
        """ Update the category dictionary with package contents """
        
        for nf in package.values():
            if not nf.category: 
                nf.category = "Unclassified"
            
            for c in nf.category.split(","):
                c = c.strip()
                self.category.add_name(c, nf)


    def rebuild_category(self):
        """ Rebuild all the category """

        self.category = PseudoGroup('Root') 
        for p in self.values():
            self.update_category(p)

       

    # Wralea functions
    def load_directory(self, dirname):
        """ Load a directory containing wraleas"""
        
        dirname = os.path.abspath(dirname)

        if(not os.path.exists(dirname) or
           not os.path.isdir(dirname)):
            print "Package directory : %s does not exists."%(dirname,)
            return

        self.add_wraleapath(dirname)

        # find wralea
        readers = self.find_wralea_dir(dirname)
        for r in readers:
            if r: 
                return r.register_packages(self)
            else:
                print "Unable to load package %s."%(filename,)
                return None



    def find_wralea_dir(self, directory):
        """
        Find in a directory wralea files,
        @return : a list of pkgreader instances
        """

        from path import path

        wralea_files = set()
        if(not os.path.isdir(directory)):
            return
            
        p = path(directory).abspath()

        # search for wralea.py
        wralea_files.update( p.walkfiles("*wralea.py") )
        wralea_files.update( p.walkfiles("__wralea__.py") )

        for f in wralea_files:
            print "Package Manager : found %s" % f
            
        return map(self.get_pkgreader, wralea_files)


    
    def find_wralea_files (self):
        """
        Find on the system all wralea.py, wralea.xml files
        @return : a list of pkgreader instances
        """
        
        readers = []
        for wp in self.wraleapath:
            readers += self.find_wralea_dir(wp)
            
        return readers



    def get_pkgreader(self, filename):
        """ Return the pkg reader corresponding to the filename """

        reader = None
        if(filename.endswith("__wralea__.py")):
            reader = PyPackageReaderWralea(filename)
        elif(filename.endswith('wralea.py')):
            reader = PyPackageReader(filename)
        else :
            raise UnknowFileType(filename)

        return reader


    def find_and_register_packages (self):
        """ Find all wralea on the system and register them """
        
        readerlist = self.find_wralea_files()
        for x in readerlist:
            x.register_packages(self)
            
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
        self.load_directory(path)
        self.write_config()
        return p


    def get_user_packages(self):
        """ Return the list of user packages """

        return [x for x in self.pkgs.values() if isinstance(x, UserPackage)]
       

    # Dictionnary behaviour
      
    def __getitem__(self, key):
        try:
            return self.pkgs[key]
        except KeyError:
            raise UnknownPackageError(key)

    def __setitem__(self, key, val):
        self.pkgs[key] = val

    def __len__(self):
        return len(self.pkgs)

    def __delitem__(self, item):
        r = self.pkgs.__delitem__(item)
        self.rebuild_category()
        return r
    
    def keys(self):
        return self.pkgs.keys()

    def items(self):
        return self.pkgs.items()

    def values(self):
        return self.pkgs.values()

    def has_key(self, *args):
        return self.pkgs.has_key(*args)
    
    def get(self, *args):
        return self.pkgs.get(*args)


    # Convenience functions
    def get_node(self, pkg_id, factory_id):
        """ Return a node instance giving a pkg_id and a factory_id """
        pkg = self[pkg_id]
        factory = pkg[factory_id]
        return factory.instantiate()


    def search_node(self, search_str, nb_inputs=-1, nb_outputs=-1):
        """ Return a list of Factory corresponding to search_str """

        search_str = search_str.upper()

        ret = [ factory \
                for pkg in self.values() \
                    for factory  in pkg.values() \
                    if(search_str in pkg.name.upper() or
                       search_str in factory.name.upper() or
                       search_str in factory.description.upper() or
                       search_str in factory.category.upper()) ]

        if(nb_inputs>=0):
            ret = filter(lambda x: x and x.inputs and len(x.inputs) == nb_inputs, ret)
        if(nb_outputs>=0):
            ret = filter(lambda x: x and x.outputs and len(x.outputs) == nb_outputs, ret)
            
        ret.sort(cmp=cmp_name)
        return ret


def cmp_name(x, y):
    """ Comparison function """
    return cmp(x.name.lower(), y.name.lower())


class PseudoGroup(dict):
    """ Data structure used to separate dotted naming (packages, category) """

    sep = '.' # Separator
    mimetype = "openalea/package"

    def __init__(self, name):
        """ Name is the pseudo package name """
        self.name = name
        self.item = None

    def new(self, name):
        return PseudoGroup(name)

    def get_id(self):
        return self.name

    def get_tip(self):
        return self.name


    def add_name(self, name, value):
        """ Add a value in the structure with the key name_tuple """

        if(not name) : 
            # if value is a dict we include sub nodes
            self.item = value
            try:
                for k, v in value.iteritems():
                    self[k] = v
            except:
                self[id(value)] = value
            return
        
        splitted = name.split(self.sep, 1)
        key = splitted[0]

        # Create sub dict if necessary
        if(not self.has_key(key)):
            self[key] = self.new(key)

        if(len(splitted)>1):
            remain = splitted[1]
        else:
            remain = None

        self[key].add_name(remain, value)
            

class PseudoPackage(PseudoGroup):
    """ Package structure used to separate dotted naming (packages, category) """

    def new(self, name):
        return PseudoPackage(name) 

    def is_real_package(self):
        return self.item != None


    def get_tip(self):
        if(self.item) : return self.item.get_tip()

        return "Sub Package : %s"%(self.name,)
   
    
    def get_metainfo(self, key):
        if(self.item):
            return self.item.get_metainfo(key)
        return "" 


