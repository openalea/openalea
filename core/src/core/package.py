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


__doc__=""" This module defines Package classes.

A Package is a deplyment unit and contains a factories (Node generator)
and meta informations (authors, license, doc...)
"""

__license__= "Cecill-C"
__revision__=" $Id$ "


import inspect
import os, sys
import string
import imp
import time
import shutil

from openalea.core.nocasedict import NoCaseDict
from openalea.core.path import path as _path
from openalea.core.vlab import vlab_object

# Exceptions

class UnknownNodeError (Exception):
    def __init__(self, name):
        Exception.__init__(self)
        self.message = "Cannot find node : %s"%(name)

    def __str__(self):
        return self.message

class FactoryExistsError(Exception):
    pass

###############################################################################


class Package(NoCaseDict):
    """
    A Package is a dictionnary of node factory.
    Each node factory is able to generate node and their widgets.

    Meta informations are associated with a package.
    """

    mimetype = "openalea/package"


    def __init__(self, name, metainfo, path=None) :
        """
        Create a Package

        @param name : a unique string used as a unique identifier for the package
        @param metainfo : a dictionnary for metainformation. Attended keys are :
            license : a string ex GPL, LGPL, Cecill, Cecill-C
            version : a string
            authors : a string
            institutes : a string
            url : a string
            description : a string for the package description
            publication : optional string for publications

        @param path : path where the package lies (a directory or a full wralea path)
        """

        dict.__init__(self)
        
        self.name = name
        self.metainfo = metainfo

        # package directory

        if(not path):
            # package directory
            import inspect
            # get the path of the file which call this function
            call_path = os.path.abspath(inspect.stack()[1][1])
            self.path = os.path.dirname(call_path)
            self.wralea_path = call_path

        # wralea.py path is specified
        else:
            if(not os.path.exists(path)):
                os.mkdir(path)
            if(not os.path.isdir(path)):
                self.path = os.path.dirname(path)
                self.wralea_path = path

            else:
                self.path = path
                self.wralea_path = os.path.join(self.path, "__wralea__.py")

            #wralea_name = name.replace('.', '_')
        

    def is_directory(self):
        """ Return if the package is embeded in a directory """
        return self.wralea_path.endswith("__wralea__.py")


    def is_editable(self):
        return False


    def get_pkg_files(self):
        """ Return the list of python filename of the package.
        The filename are relative to self.path
        """
        
        #assert self.is_directory()

        ret = []
        for file in os.listdir(self.path):
            src = os.path.join(self.path, file)
            if(not os.path.isfile(src) or
               file.endswith(".pyc") or
               file.startswith(".") 
               ): 
                continue
            ret.append(file)

        return ret


    def remove_files(self):
        """ Remove pkg files """
        assert False


    def reload(self):
        """ Reload all python file of the package """
        
        sources = self.get_pkg_files()

        s = set() # set of full path name
        for f in sources:
            if(f.endswith('.py')): f += 'c'

            s.add(os.path.abspath(os.path.join(self.path, f)))

        for module in sys.modules.values():
            if(not module): continue
            try:
                modulefile = os.path.abspath(module.__file__)
                if(modulefile in s):
                    reload(module)
                    print "Reloaded ", module.__name__
            except:
                pass
            

    def get_wralea_path(self):
        """ Return the full path of the wralea.py (if set) """
        return self.wralea_path

        
    def get_id(self):
        """ Return the package id """
        return self.name


    def get_tip(self):
        """ Return the package description """

        str= "Package : %s\n"%(self.name,)
        try: str += "Description : %s\n"%(self.metainfo['description'],)
        except : pass
        try: str += "Institutes : %s\n"%(self.metainfo['institutes'],)
        except : pass 

        try: str += "URL : %s\n"%(self.metainfo['url'],)
        except : pass 

        return str


    def get_metainfo(self, key):
        """
        Return a meta information.
        See the standard key in the __init__ function documentation.
        """
        try:
            return self.metainfo[key]
        except:
            return ""



    def add_factory(self, factory):
        """ Add to the package a factory ( node or subgraph ) """

        if(self.has_key(factory.name)):
            print "Factory %s already defined. Ignored !"%(factory.name,)
            return


        self[factory.name] = factory
        factory.package = self
        
        try:
            factory.is_valid()

        except Exception, e:
            factory.package = None
            del(self[factory.name])
            raise e
        

    def update_factory(self, old_name, factory):
        """ Update factory (change its name) """

        del(self[old_name])
        self.add_factory(factory)


    def get_names(self):
        """ Return all the factory names in a list """

        return self.keys()
    

    def get_factory(self, id):
        """ Return the factory associated with id """

        try:
            factory = self[id]
        except KeyError:
            raise UnknownNodeError("%s.%s"%(self.name,id) )

        return factory


################################################################################

class UserPackage(Package):
    """ Package user editable and persistent """

    def __init__(self, name, metainfo, path=None):
        """ @param path : directory where to store wralea and module files """

        if(not path):
            import inspect
            # get the path of the file which call this function
            path = os.path.abspath(inspect.stack()[1][1])

        Package.__init__(self, name, metainfo, path)
    
    
    def is_editable(self):
        return True

    
    def remove_files(self):
        """ Remove pkg files """
        assert self.is_directory()
        
        self.clear()
        shutil.rmtree(self.path, ignore_errors=True)


    def clone_from_package(self, pkg):
        """ Copy the contents of pkg in self"""
        
        assert self.is_directory()

        # Copy icon
        if(not self.metainfo['icon']):
            self.metainfo['icon'] = pkg.metainfo['icon']
        
        # Copy files
        sources =  pkg.get_pkg_files()

        for file in sources:
            src = os.path.join(pkg.path, file)
            dst = os.path.join(self.path, file)
            shutil.copyfile(src, dst)

        # Copy deeply all the factory
        for k,v in pkg.iteritems():
            self[k] = v.copy(replace_pkg = (pkg, self),
                             path = self.path
                             )
            
            #self.update(copy.deepcopy(pkg))

        self.write()

        
    def write(self):
        """ Return the writer class """

        writer = PyPackageWriter(self)
        if(not os.path.isdir(self.path)):
            os.mkdir(self.path)
            
        print "Writing", self.wralea_path

        writer.write_wralea(self.wralea_path)

        # create a __init__.py if necessary
        init_path = os.path.join(self.path, '__init__.py')

        if(not os.path.exists(init_path)):
            f = open(init_path, 'w')
            f.close()



    # Convenience function
    def create_user_node(self, name, category, description,
                            inputs, outputs):
        """
        Return a new user node factory
        This function create a new python module in the package directory
        The factory is added to the package
        and the package is saved """

        if(self.has_key(name)):
            raise FactoryExistsError()

        localdir = self.path
        classname = name.replace(' ', '_')
	
	
        # build function parameters
        ins = []
	for input in inputs:
            in_name = input['name'].replace(' ', '_').lower()
            in_value = input['value']
            if in_value is not None:
                arg = '%s=%s'%(in_name,in_value)
            else:
                arg = '%s'%(in_name,)
            ins.append(arg)
	in_args = ', '.join(ins)

        
        # build output
	out_values = ""
        return_values = []
	for output in outputs:
            arg = output['name'].replace(' ', '_').lower()
            out_values += '%s = None; '%(arg,)
            return_values.append('%s, '%(arg,))


        # Create the module file
	my_template = \
"""\
def %s(%s):
    '''\
    %s
    '''
    %s
    # write the node code here.

    # return outputs
    return %s
"""%(classname, in_args, description, out_values, return_values)

        module_path = os.path.join(localdir, "%s.py"%(classname))
        
        file = open(module_path, 'w')
        file.write(my_template)
        file.close()

        from openalea.core.node import NodeFactory

        factory = NodeFactory(name=name,
                              category=category,
                              description=description,
                              inputs=inputs,
                              outputs=outputs,
                              nodemodule=classname,
                              nodeclass=classname,
                              search_path = [localdir]
                              )

        self.add_factory(factory)
        self.write()
        
        return factory


    # Convenience function
    def create_user_compositenode(self, name, category, description,
                                   inputs, outputs):
        """
        Return a new user composite node factory
        and save the package
        """

        from compositenode import CompositeNodeFactory

        newfactory = CompositeNodeFactory(name=name,
                                          description= description,
                                          category = category,
                                          inputs=inputs,
                                          outputs=outputs,
                                          )
        self.add_factory(newfactory)
        self.write()
        
        return newfactory


    def add_data_file(self, filename, description=''):
        """ 
        Add a file in a package
        (copy it in the directory)
        """
        from openalea.core.data import DataFactory

        bname = os.path.basename(filename)
        src = os.path.abspath(filename)
        dst = os.path.join(self.path, bname)

        try:
            if(src != dst):
                shutil.copyfile(src, dst)
        except shutil.Error:
            f = open(dst, 'w')
            f.close()
            
        newfactory = DataFactory(bname, description)

        self.add_factory(newfactory)
        self.write()
        
        return newfactory


    def set_icon(self, filename):
        """ 
        Set package icon 
        Copy filename in the package dir
        """

        bname = os.path.basename(filename)
        src = os.path.abspath(filename)
        dst = os.path.join(self.path, bname)
        
        try:
            if(src != dst):
                shutil.copyfile(src, dst)
            self.metainfo['icon'] = bname
            self.write()
        except IOError:
            pass


    def add_factory(self, factory):
        """ Write change on disk """

        Package.add_factory(self, factory)
        

    def __delitem__(self, key):
        """ Write change on disk """
        
        Package.__delitem__(self, key)
        #self.write()



################################################################################
    
class AbstractPackageReader(object):
    """
    Abstract class to add a package in the package manager.
    """
    def __init__(self, filename):
        """ 
        Build a package from a specification file.
        filename may be a __wralea__.py file for instance.
        """
        self.filename = filename

    def register_packages(self, pkgmanager):
        """ Create and add a package in the package manager. """
        raise NotImplementedError()



class PyPackageReader(AbstractPackageReader):
    """ 
    Build packages from wralea file
    Use 'register_package' function
    """

    def filename_to_module (self, filename):
        """ Transform the filename ending with .py to the module name """
        start_index = 0
        end_index = len(filename)

        # delete the .py at the end
        if(filename.endswith('.py')):
            end_index = -3
        # Windows case (e.g. C:/...)
        if(filename[1] == ':'):
            start_index = 2

        modulename = filename[start_index:end_index]

        l = modulename.split(os.path.sep)
        modulename = '.'.join(l)

        return modulename


    def get_pkg_name(self):
        """ Return the OpenAlea (uniq) full package name """
        m = self.filename_to_module(self.filename)
        m = m.replace(".", "_")
        return m
        


    def register_packages(self, pkgmanager):
        """ Execute Wralea.py """

        retlist = []
        pkg = None

        basename = os.path.basename(self.filename)
        basedir = os.path.abspath( os.path.dirname( self.filename ))

        modulename = self.get_pkg_name()
        base_modulename = self.filename_to_module(basename)
        
        # Adapt sys.path
        sys.path.append(basedir)

        if(sys.modules.has_key(modulename)):
            del sys.modules[modulename]

        (file, pathname, desc) = imp.find_module(base_modulename, [basedir])
        try:
            wraleamodule = imp.load_module(modulename, file, pathname, desc)
            pkg = self.build_package(wraleamodule, pkgmanager)

        except Exception, e:
            print '%s is invalid :'%(self.filename,), e

        except: # Treat all exception
            print '%s is invalid :'%(self.filename,)

        if(file) :
            file.close()

        # Recover sys.path
        sys.path.pop()

        return pkg


    def build_package(self, wraleamodule, pkgmanager):
        """ Build package and update pkgmanager """

        try:
            wraleamodule.register_packages(pkgmanager) 
            
        except AttributeError:
            # compatibility issue between two types of reader
            reader = PyPackageReaderWralea(self.filename)
            reader.build_package(wraleamodule, pkgmanager)



class PyPackageReaderWralea(PyPackageReader):
    """ 
    Build a package from  a __wralea__.py 
    Use module variable
    """

    def build_package(self, wraleamodule, pkgmanager):
        """ Build package and update pkgmanager """

        name = wraleamodule.__dict__.get('__name__', None)
        edit = wraleamodule.__dict__.get('__editable__', False)

        # Build Metainfo
        metainfo = dict(
            version = '',
            license = '',
            authors = '',
            institutes = '',
            description = '',
            url = '',
            icon = '',
            )

        for k,v in wraleamodule.__dict__.iteritems():
            
            if(not k.startswith('__')): continue
            k = k[2:-2]
            if(not metainfo.has_key(k)): continue
            metainfo[k] = v

        
        # Build Package
        path = wraleamodule.__file__
        if(path.endswith('.pyc')) :
            path = path.replace('.pyc', '.py')

        if(not edit):
            p = Package(name, metainfo, path)
        else:
            p = UserPackage(name, metainfo, path)

        # Add factories
        factories = wraleamodule.__dict__.get('__all__', [])
        for fname in factories:
            f = wraleamodule.__dict__.get(fname, None)
            try:
                if(f): p.add_factory(f)
            except Exception, e:
                print e

        pkgmanager.add_package(p)
        

######################
# Vlab package reader
######################

class PyPackageReaderVlab(AbstractPackageReader):
    """ 
    Build a package from  a vlab specification file. 
    """

    def register_packages(self, pkgmanager):
        """ Create and add a package in the package manager. """
        fn = _path(self.filename).abspath()
        pkg_path = fn.dirname()

        spec_file = fn.basename()
        assert spec_file == 'specifications'

        vlab_package = vlab_object(pkg_path, pkgmanager)
        pkg = vlab_package.get_package()
        pkgmanager.add_package(pkg)


############################## Writers #########################################

class PyPackageWriter(object):
    """ Write a wralea python file """

    wralea_template =\
"""
# This file has been generated at $TIME

from openalea.core import *

$PKG_DECLARATION

"""

    pkg_template = \
"""
$PKGNAME

$METAINFO 

$ALL

$FACTORY_DECLARATION
"""


    def __init__(self, package):
        """ Package to write """

        self.package = package
        

    def get_factories_str(self):
        """ Return a dict of (name:repr) of all factory"""

        # generate code for each factory
        result_str = {}
        for f in self.package.values():
            writer = f.get_writer()
            if(writer):
                name = f.get_python_name()
                result_str[name] = str(writer)

        return result_str

    
    def __repr__(self):
        """ Return a string with the package declaration """

        fdict = self.get_factories_str()

        all = fdict.keys()

        fstr = '\n'.join(fdict.values())

        pstr = string.Template(self.pkg_template)
        
        editable = isinstance(self.package, UserPackage)

        metainfo = '__editable__ = %s\n'%(repr(editable))

        for (k, v) in self.package.metainfo.iteritems():
            key = "__%s__"%(k)
            val = repr(v)
            metainfo += "%s = %s\n"%(key, val)

        result = pstr.safe_substitute(PKGNAME="__name__ = %s"%(repr(self.package.name)),
                                      METAINFO=metainfo,
                                      ALL="__all__ = %s"%(repr(all),),
                                      FACTORY_DECLARATION=fstr,
                                      )

        return result
    

    def get_str(self):
        """ Return string to write """

        pstr = repr(self)
        wtpl = string.Template(self.wralea_template)

        result = wtpl.safe_substitute(
            TIME=time.ctime(),
            PKG_DECLARATION=pstr)

        return result
        

    def write_wralea(self, fullfilename):
        """ Write the wralea.py in the specified filename """

        try:
            result = self.get_str()
        except Exception,e:
            print e
            print "FILE HAS NOT BEEN SAVED !!"
            return
            
        handler = open(fullfilename, 'w')
        handler.write(result)
        handler.close()

        # Recompile
        import py_compile
        py_compile.compile(fullfilename)

        


