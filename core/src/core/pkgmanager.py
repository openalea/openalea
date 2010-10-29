# -*- python -*-
#
#       OpenAlea.Core
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA
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
"""This module defines the package manager.

It is able to find installed package and their wralea.py
It stores the packages and nodes informations
"""

__license__ = "Cecill-C"
__revision__ = " $Id$ "

import openalea

import sys
import os
import tempfile
import glob
from path import path
from fnmatch import fnmatch
from pkg_resources import iter_entry_points

from openalea.core.singleton import Singleton
from openalea.core.package import Package, UserPackage, PyPackageReader
from openalea.core.package import PyPackageReaderWralea, PyPackageReaderVlab
from openalea.core.settings import get_userpkg_dir, Settings
from openalea.core.pkgdict import PackageDict, is_protected, protected
from openalea.core.category import PackageManagerCategory

# Exceptions
import time
DEBUG = True
DEBUG = False

class UnknowFileType(Exception):
    pass

class UnknownPackageError (Exception):
    def __init__(self, name):
        Exception.__init__(self)
        self.message = "Cannot find package : %s"%(name)

    def __str__(self):
        return self.message


# Logging
class Logger(object):
    """ OpenAlea logging class """

    def __init__(self):
        self.log_index = 0
        self.log_file = os.path.join(tempfile.gettempdir(), "openalea.log")

        f = open(self.log_file, 'w')
        f.write("OpenAlea Log\n\n")
        f.close()


    def add(self, msg):
        """ Write to log file """

        f = open(self.log_file, 'a')
        f.write("%i %s\n"%(self.log_index, msg))
        f.close()
        self.log_index +=1


    def print_log(self):
        """ Print log file """

        f = open(self.log_file)
        print f.read()
        f.close()




###############################################################################

class PackageManager(object):
    """
    The PackageManager is a Dictionary of Packages
    It can locate OpenAlea packages on the system (with wralea).
    """

    __metaclass__ = Singleton

    def __init__ (self, verbose=True):
        """ Constructor """
        self.log = Logger()
        self.verbose = verbose
        # remove namespace option
        #self.include_namespace = self.get_include_namespace()

        # save system path
        self.old_syspath = sys.path[:]

        # dictionnary of packages
        self.pkgs = PackageDict()

        # dictionnary of category
        self.category = PseudoGroup("")

        # dictionary of standard categories
        self.user_category = PackageManagerCategory()

        # list of path to search wralea file related to the system
        self.user_wralea_path = set()
        self.sys_wralea_path = set()


        self.set_user_wralea_path()
        self.set_sys_wralea_path()






#    def get_include_namespace(self):
#        """ Read user config and return include namespace status """
#
#        config = Settings()
#
#        # include namespace
#        try:
#            s = config.get("pkgmanager", "include_namespace")
#            self.include_namespace = bool(eval(s))
#
#        except:
#            self.include_namespace = False
#
#        return self.include_namespace
#
    def get_wralea_path(self):
        """ return the list of wralea path (union of user and system)"""

        return list(self.sys_wralea_path.union(self.user_wralea_path))


    def set_user_wralea_path(self):
        """ Read user config """

        if self.user_wralea_path:
            return

        self.user_wralea_path = set()
        config = Settings()

        # wralea path
        try:
            s = config.get("pkgmanager", "path")
            l = eval(s)

            for p in l:
                self.add_wralea_path(os.path.abspath(p), self.user_wralea_path)

        except Exception, e:
            self.log.add(str(e))


    def write_config(self):
        """ Write user config """

        config = Settings()
        config.set("pkgmanager", "path", repr(list(self.user_wralea_path)))
#        config.set("pkgmanager", "include_namespace", repr(self.include_namespace))
        config.write_to_disk()


    def set_sys_wralea_path(self):
        """
        Define the default wralea search path
        For that, we look for "wralea" entry points
        and deprecated_wralea entry point
        if a package is declared as deprecated_wralea,
        the module is not load
        """


        if self.sys_wralea_path:
            return

        self.sys_wralea_path = set()
        self.deprecated_pkg = set()

        # Use setuptools entry_point
        for epoint in iter_entry_points("wralea"):

            # Get Deprecated packages
            if self.verbose:
                print epoint.name, epoint.module_name
            if(epoint.module_name == "deprecated"):
                self.deprecated_pkg.add(epoint.name.lower())
                continue

            #base = epoint.dist.location
            #m = epoint.module_name.split('.')
            #p = os.path.join(base, *m)

            # Be carfull, this lines will import __init__.py and all its predecessor
            # to find the path.
            try:
                m = __import__(epoint.module_name, fromlist=epoint.module_name)
            except ImportError, e:
                self.log.add("Cannot load %s : %s"%(epoint.module_name, e))
                continue

            l = list(m.__path__)
            for p in l :
                p = os.path.abspath(p)
                self.log.add("Wralea entry point: %s (%s) "%(epoint.module_name, p))
                self.add_wralea_path(p, self.sys_wralea_path)

        # Search the path based on the old method (by hand).
        # Search in openalea namespace
#        if(self.include_namespace):
#            l = list(openalea.__path__)
#            for p in l :
#                self.add_wralea_path(p, self.sys_wralea_path)

        self.add_wralea_path(os.path.dirname(__file__), self.sys_wralea_path)
        self.add_wralea_path(get_userpkg_dir(), self.sys_wralea_path)


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

        self.user_wralea_path = set()
        self.sys_wralea_path = set()

        self.pkgs = PackageDict()
        self.recover_syspath()
        self.category = PseudoGroup('Root')


    # Path Functions
    def add_wralea_path(self, path, container):
        """
        Add a search path for wralea files

        :param path: a path string
        :param container: set containing the path
        """

        if(not os.path.isdir(path)): return


        # Ensure to add a non existing path
        for p in container:
            common = os.path.commonprefix((p, path))
            # the path is already in wraleapth
            if( common == p and
                os.path.join(common, path[len(common):]) == path ):
                return
            # the new path is more generic, we keep it
            if(common == path and
               os.path.join(common, p[len(common):]) == p):
                container.remove(p)
                container.add(path)
                return
        # the path is absent
        container.add(path)


    def recover_syspath(self):
        """ Restore the initial sys path """
        sys.path = self.old_syspath[:]


    # Accessors
    def add_package(self, package):
        """ Add a package to the pkg manager """

        # Test if the package is deprecated
        if(package.name.lower() in self.deprecated_pkg):
            self.log.add("Deprecated : Ignoring %s"%(package.name))
            del(package)
            return

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
        """ Return a pseudo category structure """
        return self.category


    # Category management
    def update_category(self, package):
        """ Update the category dictionary with package contents """

        for nf in package.itervalues():
            # skip the deprecated name (starting with #)
            if is_protected(nf.name):
                continue

            # empty category
            if not nf.category:
                nf.category = "Unclassified"

            # parse the category
            for c in nf.category.split(","):
                # we work in lower case by convention
                c = c.strip().lower()

                # search for the sub category (split by .)
                try:
                    c_root, c_others = c.split('.',1)
                except: #if there is no '.', c_others is empty
                    c_root = c
                    c_others = ''

                if c_root in self.user_category.keywords:
                    # reconstruct the name of the category
                    c_temp = self.user_category.keywords[c_root]+'.'+c_others.title()
                    self.category.add_name(c_temp, nf)
                else:
                    self.category.add_name(c.title(), nf)


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
            self.log.add("Package directory : %s does not exists."%(dirname,))
            return None

        self.add_wralea_path(dirname, self.user_wralea_path)

        # find wralea
        readers = self.find_wralea_dir(dirname)
        if not readers:
            self.log.add("Search Vlab objects.")
            readers = self.find_vlab_dir(dirname)
        ret = None
        for r in readers:
            if r:
                ret = r.register_packages(self)
            else:
                self.log.add("Unable to load package %s."%(dirname, ))
                ret = None

        if(readers):
#            self.save_cache()
            self.rebuild_category()

        return ret


    def find_vlab_dir(self, directory, recursive=True):
        """
        Find in a directory vlab specification file.

        Search recursivly is recursive is True

        :return: a list of pkgreader instances
        """

        from path import path

        spec_files = set()
        if(not os.path.isdir(directory)):
            self.log.add("Not a directory", directory, repr(directory))
            return []

        p = path(directory).abspath()
        spec_name = '*specifications'
        # search for wralea.py
        if(recursive):
            spec_files.update( p.walkfiles(spec_name) )
        else:
            spec_files.update( p.glob(spec_name) )

        for f in spec_files:
            self.log.add("Package Manager : found  VLAB %s" % p)

        return map(self.get_pkgreader, spec_files)


    def find_wralea_dir(self, directory, recursive=True):
        """
        Find in a directory wralea files,
        Search recursivly is recursive is True

        :return : a list of pkgreader instances
        """

        if DEBUG:
            t0 = time.clock()

        wralea_files = set()
        if(not os.path.isdir(directory)):
            self.log.add("%s Not a directory"%repr(directory))
            return []

        p = path(directory).abspath()


        # search for wralea.py
        if(recursive):
            for f in p.walkfiles("*wralea*.py"):
                wralea_files.add(str(f))
        else:
            wralea_files.update( p.glob("*wralea*.py") )

        for f in wralea_files:
            self.log.add("Package Manager : found %s" % f)

        if DEBUG:
            t1 = time.clock()
            dt = t1 - t0
            print 'search wralea files takes %f sec'%dt

        readers = map(self.get_pkgreader, wralea_files)

        if DEBUG:
            t2 = time.clock()
            dt1 = t2 - t1
            print 'readers takes %f sec: %f'% (dt1, (dt1/(dt+dt1))*100)

        return readers



    def find_wralea_files (self):
        """
        Find on the system all wralea.py files

        :return : a list of pkgreader instances
        """

        readers = []

#        try:
#            # Try to load cache file
#            directories = set(self.get_cache())
#            assert(len(directories))
#            recursive = False

#        except Exception, e:
            # No cache : search recursively on the disk

        if DEBUG:
            t1 = time.clock()

        directories = self.get_wralea_path()
        if DEBUG:
            #print '      ~~~~~~~~~~'
            t2 = time.clock()
            #print '      get_wralea_path %f sec'%(t2-t1)
            #print '\n'.join(directories)

        recursive = True

        for wp in directories:
            if DEBUG: t0 = time.clock()
            ret = self.find_wralea_dir(wp, recursive)
            if(ret):
                readers += ret
            if DEBUG:
                #print '      ~~~~~~~~~~'
                t1 = time.clock()
                #print '      find_wralea %s %f sec'%(wp, t1-t0)

        if DEBUG:
            #print '      ~~~~~~~~~~'
            t3 = time.clock()
            #print '      find_wralea_dir %f sec'%(t3-t2)

        return readers



    def get_pkgreader(self, filename):
        """ Return the pkg reader corresponding to the filename """

        reader = None
        if filename.endswith("__wralea__.py"):
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

#        if(no_cache):
#            self.delete_cache()
        self.set_sys_wralea_path()
        self.set_user_wralea_path()
        if DEBUG:
            t1 = time.clock()
        readerlist = self.find_wralea_files()

        if DEBUG:
            t2 = time.clock()
            print '-------------------'
            print 'find_wralea_files takes %f seconds'%(t2-t1)

        for x in readerlist:
            x.register_packages(self)
        if DEBUG:
            t3 = time.clock()
            print '-------------------'
            print 'register_packages takes %f seconds'%(t3-t2)
#        self.save_cache()

        self.rebuild_category()


    # Cache functions
#    def get_cache_filename(self):
#        """ Return the cache filename """
#
#        return os.path.join(tempfile.gettempdir(), ".alea_pkg_cache")


#    def save_cache(self):
#        """ Save in cache current package manager state """
#
#        f = open(self.get_cache_filename(),'w')
#        s = set([pkg.path + "\n" for pkg in self.pkgs.itervalues()])
#        f.writelines(list(s))
#        f.close()
#
#
#    def delete_cache(self):
#        """ Remove cache """
#
#        n = self.get_cache_filename()
#
#        if(os.path.exists(n)):
#            os.remove(n)
#
#
#    def get_cache(self):
#        """ Return cache contents """
#
#        f = open(self.get_cache_filename(), "r")
#
#        for d in f:
#            d = d.strip()
#            yield d
#
#        f.close()


    # Package creation

    def create_user_package(self, name, metainfo, path=None):
        """
        Create a new package in the user space and register it
        Return the created package
        :param path : the directory where to create the package
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

        p = self.pkgs.get(name)
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

    def __contains__(self, key):
        return self.has_key(key)

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
        """
        Return a list of Factory corresponding to search_str
        If nb_inputs or nb_outputs is specified,
        return only node with the same number of (in/out) ports
        """

        search_str = search_str.upper()

        best = None
        match = []
        # Search for each package and for each factory
        for name, pkg in self.iteritems():
            if(is_protected(name)): continue # alias

            for fname, factory in pkg.iteritems():
                if(is_protected(fname)): continue # alias

                if(not best and (search_str == factory.name.upper())):
                    best = factory
                    continue

                if(search_str in pkg.name.upper() or
                   search_str in factory.name.upper() or
                   search_str in factory.description.upper() or
                   search_str in factory.category.upper() or
                   search_str in "%s:%s"%(pkg.name.upper(), factory.name.upper())):

                    match.append(factory)

        # Filter ports
        if(nb_inputs>=0):
            match = filter(lambda x: x and x.inputs and len(x.inputs) == nb_inputs, match)
        if(nb_outputs>=0):
            match = filter(lambda x: x and x.outputs and len(x.outputs) == nb_outputs, match)

        match.sort(cmp=cmp_name)
        if(best) : match.insert(0, best)
        return match


    ####################################################################################
    # Methods to introspect globally the PkgManager
    ####################################################################################

    def get_packages(self, pkg_name=None):
        """
        Return all public packages.
        """
        if pkg_name and is_protected(pkg_name):
            pkg_name = None
        if pkg_name and pkg_name in self:
            pkgs = [pkg_name]
        else:
            pkgs = set(pk.name for pk in self.itervalues() if not is_protected(pk.name))
        return [self[p] for p in pkgs]


    def get_data(self, pattern='*.*',pkg_name=None):
        """ Return all data that match the pattern. """
        pkgs = self.get_packages(pkg_name)
        datafiles = [f for p in pkgs for f in p.itervalues() if not is_protected(f.name) and f.is_data() and fnmatch(f.name,pattern)]
        return datafiles

    def get_composite_nodes(self, pkg_name=None):
        pkgs = self.get_packages(pkg_name)
        cn = [f for p in pkgs for f in p.itervalues() if f.is_composite_node() ]
        return cn

    def get_nodes(self, pkg_name=None):
        pkgs = self.get_packages(pkg_name)
        nf = [f for p in pkgs for f in p.itervalues() if f.is_node() ]
        return nf

    def _dependencies(self, factory):
        f = factory
        if not f.is_composite_node():
            return

        for p,n in f.elt_factory.values():
            if is_protected(p) or is_protected(n):
                continue
            try:
                fact = self[p][n]
            except:
                #print p, n
                continue
            yield fact

            for df in self._dependencies(fact):
                yield df

    def _missing_dependencies(self, factory, l=[]):

        f = factory
        if not f.is_composite_node():
            return

        for p,n in f.elt_factory.values():
            if is_protected(p) or is_protected(n):
                continue
            try:
                fact = self[p][n]
            except:
                l.append((p, n))
                continue
            yield fact

            for df in self._missing_dependencies(fact,l):
                yield df

    def _missing(self, factory, l=[]):
        list(self._missing_dependencies(factory,l))
        return l

    def missing_dependencies(self,package_or_factory=None):
        """ Return all the dependencies of a package or a factory. """
        f = package_or_factory
        if f is None:
            return self._all_missing_dependencies()
        if isinstance(f, Package):
            return self._missing_pkg_dependencies(f)
        else:
            return self._missing_cn_dependencies(f)

    def dependencies(self, package_or_factory=None):
        """ Return all the dependencies of a package or a factory. """
        f = package_or_factory
        if f is None:
            return self._all_dependencies()
        if isinstance(f, Package):
            return self._pkg_dependencies(f)
        else:
            return self._cn_dependencies(f)

    def _all_dependencies(self):

        d = {}
        for pkg in self.get_packages():
            m = self._pkg_dependencies(pkg)
            if m:
                d[pkg.name] = m
        return d


    def _pkg_dependencies(self, package):
        cns = [f for f in package.itervalues() if f.is_composite_node() ]
        factories = set((f.package.name, f.name) for cn_factory in cns for f in self._dependencies(cn_factory) if f.package.name != package.name)
        return sorted(factories)

    def _cn_dependencies(self, factory):
        factories = set((f.package.name, f.name) for f in self._dependencies(factory))
        return sorted(factories)

    def _all_missing_dependencies(self):
        d = {}
        for pkg in self.get_packages():
            m = self._missing_pkg_dependencies(pkg)
            if m:
                d[pkg.name] = m
        return d
    def _missing_pkg_dependencies(self, package):
        cns = [f for f in package.itervalues() if f.is_composite_node() ]
        l=[]
        for cn in cns:
           self._missing(cn,l)
        factories = set(l)
        if factories:
            return sorted(factories)
        return None

    def _missing_cn_dependencies(self, factory):
        l=[]
        factories = set(self._missing(factory,l))
        if factories:
            return sorted(factories)
        return None


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
        """todo"""
        return PseudoGroup(name)

    def get_id(self):
        """todo"""
        return self.name

    def get_tip(self):
        """todo"""
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
                try:
                    self[str(id(value))] = value
                except Exception, e:
                    print e
                    pass
            return

        splitted = name.split(self.sep, 1)
        key = splitted[0]

        if(len(splitted)>1):
            remain = splitted[1]
        else:
            remain = None

        # Create sub dict if necessary
        if not dict.has_key(self, key.lower()):
            self[key] = self.new(key)

        try:
            self[key].add_name(remain, value)
        except Exception, e:
            print 'Package %s[%s]'%(self.name, name)
            print e
            try:
                self[str(id(key))].add_name(remain, value)
            except Exception, e:
                print 'Unable to found the nodes: %s'%value
                print e
                pass



class PseudoPackage(PseudoGroup):
    """ Package structure used to separate dotted naming (packages, category) """

    def new(self, name):
        """todo"""
        return PseudoPackage(name)

    def is_real_package(self):
        """todo"""
        return self.item != None


    def get_tip(self):
        """todo"""
        if(self.item) : return self.item.get_tip()

        return "Sub Package : %s" % (self.name, )

    def get_metainfo(self, key):
        """todo"""
        if(self.item):
            return self.item.get_metainfo(key)
        return ""


