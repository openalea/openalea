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

It is able to find installed package and their plugin.py
It stores the packages and nodes informations
"""

__license__ = "Cecill-C"
__revision__ = " $Id: pkgmanager.py 3772 2013-04-05 13:46:39Z pradal $ "

import sys
import os
from os.path import join as pj
from os.path import isdir

import urlparse
from openalea.core.path import path
from fnmatch import fnmatch
from pkg_resources import iter_entry_points

from openalea.core.singleton import Singleton
from openalea.core.observer import Observed
from openalea.core.settings import get_userpkg_dir, Settings
from openalea.core.pkgdict import PackageDict, is_protected, protected
from openalea.core import logger
from openalea.core.package import (Package, UserPackage, PyPackageReader,
PyPackageReaderWralea)
from openalea.core.category import PackageManagerCategory

from ConfigParser import NoSectionError, NoOptionError

# Exceptions
import time
DEBUG = False
SEARCH_OUTSIDE_ENTRY_POINTS = True


from openalea.core.pkgmanager import (Logger, pmanLogger, logger, 
                                      UnknownPackageError, IllFormedUrlError)

class PluginManager(Observed):
    """
    The PluginManager is a Dictionary of Packages
    It can locate OpenAlea packages on the system (with plugin).
    """

    def __init__ (self, plugin_type='plugin', verbose=True):
        """ Constructor """
        Observed.__init__(self)
        self.log = Logger()

        self.plugin_type = plugin_type

        #make urlparse correctly handle the glorious "oa" protocol :)
        urlparse.uses_query.append("oa")

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

        # list of path to search plugin file related to the system
        self.user_plugin_path = set()
        self.sys_plugin_path = set()
        # for packages that we don't want to save in the config file
        self.temporary_plugin_paths = set()


        self.set_user_plugin_path()
        self.set_sys_plugin_path()



    def emit_update(self):
        self.notify_listeners("update")


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
    def get_plugin_path(self):
        """ return the list of plugin path (union of user and system)"""

        dirs = list(self.temporary_plugin_paths.union(self.sys_plugin_path.union(self.user_plugin_path)))
        dirs = filter(isdir, dirs)
        return dirs


    def set_user_plugin_path(self):
        """ Read user config """

        if self.user_plugin_path:
            return
        if not SEARCH_OUTSIDE_ENTRY_POINTS:
            return

        self.user_plugin_path = set()
        config = Settings()
        l = []
        # plugin path
        try:
            s = config.get("pkgmanager", "path")
            l = eval(s)
        except NoSectionError, e:
            config.add_section("pkgmanager")
            config.add_option("pkgmanager", "path", str([]))
        except NoOptionError, e:
            config.add_option("pkgmanager", "path", str([]))
        for p in l:
            self.add_plugin_path(os.path.abspath(p), self.user_plugin_path)


    def write_config(self):
        """ Write user config """

        config = Settings()
        config.set("pkgmanager", "path", repr(list(self.user_plugin_path)))
#        config.set("pkgmanager", "include_namespace", repr(self.include_namespace))
        config.write()


    def set_sys_plugin_path(self):
        """
        Define the default plugin search path
        For that, we look for "plugin" entry points
        and deprecated_plugin entry point
        if a package is declared as deprecated_plugin,
        the module is not load
        """


        if self.sys_plugin_path:
            return

        self.sys_plugin_path = set()
        self.deprecated_pkg = set()

        # Use setuptools entry_point
        for epoint in iter_entry_points(self.plugin_type):

            # Get Deprecated packages
            if self.verbose:
                pmanLogger.debug(epoint.name +" "+ epoint.module_name)
            if(epoint.module_name == "deprecated"):
                self.deprecated_pkg.add(epoint.name.lower())
                continue

            #base = epoint.dist.location
            #m = epoint.module_name.split('.')
            #p = os.path.join(base, *m)

            # Be careful, this lines will import __init__.py and all its predecessor
            # to find the path.
            try:
                m = __import__(epoint.module_name, fromlist=epoint.module_name)
            except ImportError, e:
                logger.error("Cannot load %s : %s"%(epoint.module_name, e))
                #self.log.add("Cannot load %s : %s"%(epoint.module_name, e))
                continue

            l = list(m.__path__)
            for p in l :
                p = os.path.abspath(p)
                logger.info("plugin entry point: %s (%s) "%(epoint.module_name, p))
                #self.log.add("plugin entry point: %s (%s) "%(epoint.module_name, p))
                self.add_plugin_path(p, self.sys_plugin_path)

        # Search the path based on the old method (by hand).
        # Search in openalea namespace
#        if(self.include_namespace):
#            l = list(openalea.__path__)
#            for p in l :
#                self.add_plugin_path(p, self.sys_plugin_path)

        if SEARCH_OUTSIDE_ENTRY_POINTS:
            self.add_plugin_path(os.path.dirname(__file__), self.sys_plugin_path)
            self.add_plugin_path(get_userpkg_dir(), self.sys_plugin_path)


    def init(self, dirname=None, verbose=True):
        """ Initialize package manager

        If dirname is None, find plugin files on the system
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
        self.notify_listeners("update")


    def clear(self):
        """ Remove all packages """

        self.user_plugin_path = set()
        self.sys_plugin_path = set()

        self.pkgs = PackageDict()
        self.recover_syspath()
        self.category = PseudoGroup('Root')


    # Path Functions
    def add_plugin_path(self, path, container):
        """
        Add a search path for plugin files

        :param path: a path string
        :param container: set containing the path
        """

        if(not os.path.isdir(path)): return

        # Ensure to add a non existing path
        for p in container:
            common = os.path.commonprefix((p, path))
            # the path is already in pluginpth
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
            logger.warning("Deprecated : Ignoring %s"%(package.name))
            #self.log.add("Deprecated : Ignoring %s"%(package.name))
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



    # plugin functions
    def load_directory(self, dirname):
        """ Load a directory containing plugins"""

        dirname = os.path.abspath(dirname)

        if(not os.path.exists(dirname) or
           not os.path.isdir(dirname)):
            logger.error("Package directory : %s does not exists."%(dirname,))
            #self.log.add("Package directory : %s does not exists."%(dirname,))
            return None

        self.add_plugin_path(dirname, self.user_plugin_path)

        # find plugin
        readers = self.find_plugin_dir(dirname)
        if not readers:
            logger.info("Search Vlab objects.")
            #self.log.add("Search Vlab objects.")
            readers = self.find_vlab_dir(dirname)
        ret = None
        for r in readers:
            if r:
                ret = r.register_packages(self)
            else:
                logger.error("Unable to load package %s."%(dirname, ))
                #self.log.add("Unable to load package %s."%(dirname, ))
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

        from openalea.core.path import path

        spec_files = set()
        if(not os.path.isdir(directory)):
            logger.error("Not a directory", directory, repr(directory))
            #self.log.add("Not a directory", directory, repr(directory))
            return []

        p = path(directory).abspath()
        spec_name = '*specifications'
        # search for plugin.py
        if(recursive and SEARCH_OUTSIDE_ENTRY_POINTS):
            spec_files.update( p.walkfiles(spec_name) )
        else:
            spec_files.update( p.glob(spec_name) )

        for f in spec_files:
            logger.info("Package Manager : found  VLAB %s" % p)
            #self.log.add("Package Manager : found  VLAB %s" % p)

        return map(self.get_pkgreader, spec_files)


    def find_plugin_dir(self, directory, recursive=True):
        """
        Find in a directory plugin files,
        Search recursivly is recursive is True

        :return : a list of pkgreader instances
        """

        if DEBUG:
            t0 = time.clock()

        plugin_files = set()
        if(not os.path.isdir(directory)):
            logger.warning("%s Not a directory"%repr(directory))
            #self.log.add("%s Not a directory"%repr(directory))
            return []

        p = path(directory).abspath()


        # search for plugin.py
        if(recursive and SEARCH_OUTSIDE_ENTRY_POINTS):
            for f in p.walkfiles("*%s*.py" % self.plugin_type):
                plugin_files.add(str(f))
        else:
            plugin_files.update( p.glob("*%s*.py" % self.plugin_type) )

        for f in plugin_files:
            logger.info("Package Manager : found %s" % f)
            #self.log.add("Package Manager : found %s" % f)

        if DEBUG:
            t1 = time.clock()
            dt = t1 - t0
            print 'search plugin files takes %f sec'%dt

        readers = map(self.get_pkgreader, plugin_files)

        if DEBUG:
            t2 = time.clock()
            dt1 = t2 - t1
            print 'readers takes %f sec: '% (dt1,)

        return readers



    def find_plugin_files (self):
        """
        Find on the system all plugin.py files

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

        directories = self.get_plugin_path()
        if DEBUG:
            #print '      ~~~~~~~~~~'
            t2 = time.clock()
            #print '      get_plugin_path %f sec'%(t2-t1)
            #print '\n'.join(directories)

        recursive = True

        for wp in directories:
            if DEBUG: t0 = time.clock()
            ret = self.find_plugin_dir(wp, recursive)
            if(ret):
                readers += ret
            if DEBUG:
                #print '      ~~~~~~~~~~'
                t1 = time.clock()
                #print '      find_plugin %s %f sec'%(wp, t1-t0)

        if DEBUG:
            #print '      ~~~~~~~~~~'
            t3 = time.clock()
            #print '      find_plugin_dir %f sec'%(t3-t2)

        return readers

    def find_all_plugin(self):
        """
        Find on the system all plugin.py files

        :return : a list of file paths
        """

        files = set()
        directories = self.get_plugin_path()
        recursive = True
        if not SEARCH_OUTSIDE_ENTRY_POINTS:
            recursive = False 
        if recursive:
            files = set( f.abspath() for p in directories for f in path(p).walkfiles('*%s*.py' % self.plugin_type))
        else:
            files = set( f.abspath() for p in directories for f in path(p).glob('*%s*.py' % self.plugin_type))
        return files

    def create_readers(self, plugin_files):
        return  filter(None,(self.get_pkgreader(f) for f in plugin_files))


    def get_pkgreader(self, filename):
        """ Return the pkg reader corresponding to the filename """

        reader = None
        if filename.endswith("__%s__.py" % self.plugin_type):
            reader = PyPackageReaderWralea(filename)
        else :
            return None

        return reader


    def find_and_register_packages (self, no_cache=False):
        """
        Find all plugin on the system and register them
        If no_cache is True, ignore cache file
        """

#        if(no_cache):
#            self.delete_cache()
        self.set_sys_plugin_path()
        self.set_user_plugin_path()
        if DEBUG:
            t1 = time.clock()

        plugin_files = self.find_all_plugin()
        readerlist = self.create_readers(plugin_files)

        #readerlist = self.find_plugin_files()

        if DEBUG:
            t2 = time.clock()
            print '-------------------'
            print 'find_plugin_files takes %f seconds'%(t2-t1)

        for x in readerlist:
            if DEBUG:
                tn = time.clock()
            x.register_packages(self)
            if DEBUG:
                print 'register package ', x.get_pkg_name(), 'in ', time.clock() -tn
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

        if(not isdir(path)):
            os.mkdir(path)

        if(not os.path.exists(os.path.join(path, "__%s__.py" % self.plugin_type))):
            # Create new Package and its plugin
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
        self.notify_listeners("update")


    # Dictionnary behaviour

    def __getitem__(self, key):
        try:
            return self.pkgs[key]
        except KeyError:
            raise UnknownPackageError(key)

    def __setitem__(self, key, val):
        self.pkgs[key] = val
        self.notify_listeners("update")

    def __len__(self):
        return len(self.pkgs)

    def __delitem__(self, item):
        r = self.pkgs.__delitem__(item)
        self.rebuild_category()
        self.notify_listeners("update")
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
    def get_node_from_url(self, url):
        fac = self.get_factory_from_url(url)
        return fac.instantiate()

    def get_factory_from_url(self, url):
        """Returns a node instance from the given url.

        :Parameters:
        - url - is either a string or a urlparse.ParseResult instance.
        It is encoded this way: oa://*domain*/*packageName*?fac=*factoryName*&ft=*factoryType* .
        "oa" means that it is meant to be used by openalea.
        "domain" MUST BE "local" for now.
        "packageName" is the name of the package
        "factoryName" is the of factory
        "factoryType" is one of {"CompositeNodeFactory", "NodeFactory", "DataFactory"}
        """
        pkg, queries = self.get_package_from_url(url)#url.path.strip("/") #the path is preceded by one "/"
        if "fac" not in queries:
            raise IllFormedUrlError(url.geturl())
        factory_id = queries["fac"][0]
        factory = pkg[factory_id.strip("/")]
        return factory

    def get_package_from_url(self, url):
        if isinstance(url, str):
            url = urlparse.urlparse(url)
        assert isinstance(url, urlparse.ParseResult)
        queries  = urlparse.parse_qs(url.query)
        pkg_id = url.path.strip("/") #the path is preceded by one "/"
        pkg = self[pkg_id]
        return pkg, queries


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

        The results are sorted in the following way:
          1 - Highest Priority : presence of search_str in factory name
                           and position in the name (closer to the
                           begining = higher score)
          2 - Then : Number of occurences of search_str in the factory
              description.
          3 - Then : Number of occurences of search_str in the category name
          4 - Finally : presence of search_str in package name and position
              in the name (close to the begining = higher score)
        """

        search_str = search_str.upper()

        best = None
        match = []
        scored = []
        # Search for each package and for each factory
        for name, pkg in self.iteritems():
            if(is_protected(name)): continue # alias

            for fname, factory in pkg.iteritems():
                if(is_protected(fname)): continue # alias

                # -- The scores for each string that is explored.
                # They are long ints because we make a 96 bits bitshift
                # to compute the final score --
                facNameScore = 0L
                facDescScore = 0L
                facCateScore = 0L
                pkgNameScore = 0L

                fname = factory.name.upper()
                if search_str in fname:
                    l = float(len(fname))
                    facNameScore = long(100*(1-fname.index(search_str)/l))

                facDescScore = long(factory.description.upper().count(search_str))
                facCateScore = long(factory.category.upper().count(search_str))

                pname = pkg.name.upper()
                if search_str in pname:
                    l = float(len(pname))
                    pkgNameScore = long(100*(1-pname.index(search_str)/l))

                score = facNameScore << (32*3) | facDescScore << (32*2) | \
                        facCateScore << (32*1) | pkgNameScore << (32)
                if score > 0:
                    match.append((score, factory))

        # Filter ports
        if(nb_inputs>=0):
            match = filter(lambda (sc, x): x and x.inputs and len(x.inputs) == nb_inputs, match)
        if(nb_outputs>=0):
            match = filter(lambda (sc, x): x and x.outputs and len(x.outputs) == nb_outputs, match)

        if not len(match):
            return match

        match.sort(reverse=True)
        match = zip(*match)[1]

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


    def get_data(self, pattern='*.*',pkg_name=None, as_paths=False):
        """ Return all data that match the pattern. """
        pkgs = self.get_packages(pkg_name)
        datafiles = [(pj(p.path,f.name) if as_paths else f) for p in pkgs \
                         for f in p.itervalues() if not is_protected(f.name) and f.is_data() and fnmatch(f.name,pattern)]
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

    def who_use(self, factory_name):
        """ Search who use a package or a factory

        return a list of factory.
        """
        res = []
        for pkg in self.get_packages():
            cns = [f for f in pkg.itervalues() if f.is_composite_node()]
            res.extend((pkg.name, cn.name) for cn in cns for pname, name in self._cn_dependencies(cn) if name == factory_name)
        return res

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
                print 'Unable to find these nodes: %s'%value
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


