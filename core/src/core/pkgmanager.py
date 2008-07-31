# -*- python -*-
#
#       OpenAlea.Core
#
#       Copyright 2006-2008 INRIA - CIRAD - INRA  
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
import tempfile
import glob

from pkg_resources import iter_entry_points

from openalea.core.singleton import Singleton
from openalea.core.package import UserPackage, PyPackageReader
from openalea.core.package import PyPackageReaderWralea, PyPackageReaderVlab
from openalea.core.settings import get_userpkg_dir, Settings
from openalea.core.pkgdict import PackageDict, is_protected, protected

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
        self.pkgs = PackageDict()

        # dictionnary of category
        self.category = PseudoGroup("")

        # list of path to search wralea file
        self.set_default_wraleapath()


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
            #base = epoint.dist.location
            #m = epoint.module_name.split('.')
            #p = os.path.join(base, *m)
            try:
                m = __import__(epoint.module_name, fromlist=epoint.module_name)
            except ImportError, e:
                print "Cannot load %s : %s"%(epoint.module_name, e)
                continue

            l = list(m.__path__)
            for p in l :
                p = os.path.abspath(p)
                print "Wralea entry point: %s (%s) "%(epoint.module_name, p)
                self.add_wraleapath(p)

        # Search in openalea namespace
        if(self.include_namespace):
            l = list(openalea.__path__)
            for p in l :
                self.add_wraleapath(p)

        self.add_wraleapath(os.path.dirname(__file__))
        self.add_wraleapath(get_userpkg_dir())


    def init(self, dirname=None, verbose=True):
        """ Initialize package manager
        If dirname is None, find wralea files on the system
        else load directory
        If verbose is False, don't print any output
        """

        # output redirection
        if(not verbose):
            sysout = sys.stdout
            sys.stdout = open(os.devnull, 'w')

        try:

            if (not dirname):
                self.find_and_register_packages()
            else :
                self.load_directory(dirname) 

        finally:

            if(not verbose):
                sys.stdout.close()
                sys.stdout = sysout


    def reload(self, pkg=None):
        """ Reload all packages if pkg is None
        else reload only pkg"""

        if(not pkg):
            self.clear()
            self.find_and_register_packages(no_cache=True)
            for p in self.pkgs.values():
                p.reload()
        else:
            pkg.reload()
            self.load_directory(pkg.path)
        
        
    def clear(self):
        """ Remove all packages """

        self.pkgs = PackageDict()
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
            if( common == p and
                os.path.join(common, path[len(common):]) == path ): 
                return
            # the new path is more generic, we keep it
            if(common == path and
               os.path.join(common, p[len(common):]) == p):
                self.wraleapath.remove(p)
                self.wraleapath.add(path)
                return
        # the path is absent
        self.wraleapath.add(path)
        
        

    def recover_syspath(self):
        """ Restore the initial sys path """
        sys.path = self.old_syspath[:]


    # Accessors
    def add_package(self, package):
        """ Add a package to the pkg manager """

        #if( not self.pkgs.has_key(package.get_id())):
        self[package.get_id()] = package
        self.update_category(package)


    def get_pseudo_pkg(self):
        """ Return a pseudopackage structure """

        pt = PseudoPackage('Root')

        # Build the name tree (on uniq objects)
        s = set()
        for k, v in self.pkgs.iteritems():
            if(not is_protected(k)):
                pt.add_name(k, v)

        return pt

    
    def get_pseudo_cat(self):
        """ Return a pseudocategory structure """
        return self.category 


    # Category management
    def update_category(self, package):
        """ Update the category dictionary with package contents """
        
        for nf in package.itervalues():
            if not nf.category: 
                nf.category = "Unclassified"
            
            for c in nf.category.split(","):
                c = c.strip()
                self.category.add_name(c, nf)


    def rebuild_category(self):
        """ Rebuild all the category """

        self.category = PseudoGroup('Root') 
        for p in self.pkgs.itervalues():
            self.update_category(p)

       

    # Wralea functions
    def load_directory(self, dirname):
        """ Load a directory containing wraleas"""
        
        dirname = os.path.abspath(dirname)

        if(not os.path.exists(dirname) or
           not os.path.isdir(dirname)):
            print "Package directory : %s does not exists."%(dirname,)
            return None

        self.add_wraleapath(dirname)

        # find wralea
        readers = self.find_wralea_dir(dirname)
        if not readers:
            print "Search Vlab objects."
            readers = self.find_vlab_dir(dirname)
        ret = None
        for r in readers:
            if r: 
                ret = r.register_packages(self)
            else:
                print "Unable to load package %s."%(filename,)
                ret = None
        
        if(readers): 
            self.save_cache()
            self.rebuild_category()

        return ret


    def find_vlab_dir(self, directory, recursive=True):
        """
        Find in a directory vlab specification file.
        Search recursivly is recursive is True
        @return : a list of pkgreader instances
        """

        from path import path

        spec_files = set()
        if(not os.path.isdir(directory)):
            print "notdir", directory, repr(directory)
            return []
            
        p = path(directory).abspath()

        # search for wralea.py
        if(recursive):
            spec_files.update( p.walkfiles("specifications") )
        else:
            spec_files.update( p.glob("specifications") )

        for f in spec_files:
            print "Package Manager : found  VLAB %s" % p
            
        return map(self.get_pkgreader, spec_files)


    def find_wralea_dir(self, directory, recursive=True):
        """
        Find in a directory wralea files,
        Search recursivly is recursive is True
        @return : a list of pkgreader instances
        """

        from path import path

        wralea_files = set()
        if(not os.path.isdir(directory)):
            print "notdir", directory, repr(directory)
            return []
            
        p = path(directory).abspath()


        # search for wralea.py
        if(recursive):
            for f in p.walkfiles("*wralea*.py"):
                wralea_files.add(str(f))
        else:
            wralea_files.update( p.glob("*wralea*.py") )
        
        for f in wralea_files:
            print "Package Manager : found %s" % f
            
        return map(self.get_pkgreader, wralea_files)


    
    def find_wralea_files (self):
        """
        Find on the system all wralea.py files
        @return : a list of pkgreader instances
        """
        
        readers = []

        try:
            # Try to load cache file
            directories = set(self.get_cache())
            assert(len(directories))
            recursive = False

        except Exception, e:
            # No cache : search recursively on the disk
            
            self.read_wralea_path()

            directories = self.wraleapath
            recursive = True

        for wp in directories:
            ret = self.find_wralea_dir(wp, recursive)
            if(ret):
                readers += ret 
            
        return readers



    def get_pkgreader(self, filename):
        """ Return the pkg reader corresponding to the filename """

        reader = None
        if(filename.endswith("__wralea__.py")):
            reader = PyPackageReaderWralea(filename)
        elif(filename.endswith('wralea.py')):
            reader = PyPackageReader(filename)
        elif(filename.endswith('specifications')):
            reader = PyPackageReaderVlab(filename)

        else :
            raise UnknowFileType(filename)

        return reader


    def find_and_register_packages (self, no_cache=False):
        """ 
        Find all wralea on the system and register them 
        If no_cache is True, ignore cache file
        """

        if(no_cache):
            self.delete_cache()

        readerlist = self.find_wralea_files()
        for x in readerlist:
            x.register_packages(self)

        self.save_cache()
        self.rebuild_category()


    # Cache functions
    def get_cache_filename(self):
        """ Return the cache filename """

        return os.path.join(tempfile.gettempdir(), ".alea_pkg_cache")


    def save_cache(self):
        """ Save in cache current package manager state """
        
        f = open(self.get_cache_filename(),'w')
        s = set([pkg.path + "\n" for pkg in self.pkgs.itervalues()])
        f.writelines(list(s))
        f.close()


    def delete_cache(self):
        """ Remove cache """
        
        n = self.get_cache_filename()

        if(os.path.exists(n)):
            os.remove(n)


    def get_cache(self):
        """ Return cache contents """
        
        f = open(self.get_cache_filename(), "r")
        
        for d in f:
            d = d.strip()
            yield d
        
        f.close()
        
        
    # Package creation

    def create_user_package(self, name, metainfo, path=None):
        """
        Create a new package in the user space and register it
        Return the created package
        @param path : the directory where to create the package
        """

        if(self.pkgs.has_key(name)):
            return self.pkgs[name]

        # Create directory
        if(not path):
            path = get_userpkg_dir()
        path = os.path.join(path, name)
        
        if(not os.path.isdir(path)):
            os.mkdir(path)

        if(not os.path.exists(os.path.join(path, "__wralea__.py"))):
            # Create new Package and its wralea
            p = UserPackage(name, metainfo, path)
            p.write()

        # Register package
        self.load_directory(path)
        self.write_config()

        p = self.pkgs[name]
        return p


    def get_user_packages(self):
        """ Return the list of user packages """

        return [x for x in self.pkgs.values() if isinstance(x, UserPackage)]


    def rename_package(self, old_name, new_name):
        """ Rename package 'old_name' to 'new_name' """
        
        self.pkgs[protected(old_name)] = self.pkgs[old_name]
        self.pkgs[new_name] = self.pkgs[old_name]
        self.pkgs[old_name].name = new_name

        if(self.pkgs[old_name].metainfo.has_key('alias')):
               self.pkgs[old_name].metainfo['alias'].append(old_name)

        self.pkgs[old_name].write()
        del(self.pkgs[old_name])
       

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

    def iterkeys(self):
        return self.pkgs.iterkeys()

    def iteritems(self):
        return self.pkgs.iteritems()

    def itervalues(self):
        return self.pkgs.itervalues()

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

        best = None
        match = [] 
        for pkg in self.values():
            for factory  in pkg.values():
                
                if(not best and (search_str == factory.name.upper())):
                    best = factory
                    continue

                if(search_str in pkg.name.upper() or
                   search_str in factory.name.upper() or
                   search_str in factory.description.upper() or
                   search_str in factory.category.upper() or
                   search_str in "%s:%s"%(pkg.name.upper(), factory.name.upper())):

                    match.append(factory)
                       

        if(nb_inputs>=0):
            match = filter(lambda x: x and x.inputs and len(x.inputs) == nb_inputs, match)
        if(nb_outputs>=0):
            match = filter(lambda x: x and x.outputs and len(x.outputs) == nb_outputs, match)
            
        match.sort(cmp=cmp_name)
        if(best) : match.insert(0, best)
        return match


def cmp_name(x, y):
    """ Comparison function """
    return cmp(x.name.lower(), y.name.lower())



class PseudoGroup(PackageDict):
    """ Data structure used to separate dotted naming (packages, category) """

    sep = '.' # Separator
    mimetype = "openalea/package"

    def __init__(self, name):
        """ Name is the pseudo package name """

        PackageDict.__init__(self)
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
                self[str(id(value))] = value
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


