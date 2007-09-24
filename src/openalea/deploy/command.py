# -*- python -*-
#
#       OpenAlea.Deploy: OpenAlea setuptools extension
#
#       Copyright 2006-2007 INRIA - CIRAD - INRA  
#
#       File author(s): Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#

__doc__="""
Setuptools commands
"""

__license__= "Cecill-C"
__revision__=" $Id$ "




import os, sys
import shutil
from distutils.errors import *

from os.path import join as pj
from setuptools import Command
from setuptools.dist import assert_string_list, assert_bool
from setuptools.command.build_py import build_py as old_build_py
from setuptools.command.build_ext import build_ext as old_build_ext
from setuptools.command.install import install as old_install
from setuptools.command.easy_install import easy_install
from setuptools.command.develop import develop

import setuptools.command.build_py
import setuptools.command.build_ext
import setuptools.command.install

from distutils.dist import Distribution

import pkg_resources
from distutils.errors import DistutilsSetupError
from distutils.util import convert_path
from distutils.dir_util import mkpath

import re
import new

from openalea.deploy import get_all_lib_dirs, get_all_bin_dirs
from openalea.deploy import get_base_dir, OPENALEA_PI
from openalea.deploy.environ_var import set_lsb_env, set_win_env



# Utility
def copy_data_tree (src, dst, exclude_pattern=['(RCS|CVS|\.svn)', '.*\~']):
    """
    Copy an entire directory tree 'src' to a new location 'dst'.
    @param exclude_pattern: a list of pattern to exclude.
    """
   
    names = os.listdir(src)
    mkpath(dst)
    outfiles = []

    for p in exclude_pattern:
        names = filter( lambda x: not(re.match(p, x)) , names)
            
    for n in names:
        src_name = os.path.join(src, n)
        dst_name = os.path.join(dst, n)
                
        if os.path.isdir(src_name):
            ret = copy_data_tree(src_name, dst_name, exclude_pattern)
            outfiles += ret

        else:
            shutil.copy2(src_name, dst_name)
            outfiles.append(dst_name)
            
    return outfiles

    

# Command overloading

def has_ext_modules(dist):
    """ Replacement function for has_ext_module """
    try:
        return Distribution.has_ext_modules(dist) or \
               (dist.scons_scripts or
                dist.lib_dirs or dist.inc_dirs or
                dist.bin_dirs or dist.share_dirs)
    except:
        return dist.has_ext_modules()


def set_has_ext_modules(dist):
    """ Set new function handler to dist object """
    m = new.instancemethod(has_ext_modules, dist, Distribution)
    dist.has_ext_modules = m


class build_py(old_build_py):
    """
    Enhanced 'build_py'
    Create namespace
    """

    def initialize_options (self):
        old_build_py.initialize_options(self)
	self.scons_ext_param = ""  # None value are not accepted
	self.scons_path = None     # Scons path


    def run(self):
        # Run others commands
        self.run_command("create_namespaces")
        return old_build_py.run(self)


class build_ext(old_build_ext):
    """
    Enhanced 'build_ext'
    Add lib_dirs and inc_dirs parameters to package parameter
    """

    # User options
    user_options = []
    user_options.extend( old_build_ext.user_options )
    user_options.append( ( 'scons-ext-param=' ,
                           None,
                           'External parameters to pass to scons.' ) )
    user_options.append( ( 'scons-path=',
                           None,
                           'Optional scons executable path.'
                           'eg : C:\Python25\scons.bat for windows.' ) )


    def initialize_options (self):
        old_build_ext.initialize_options(self)
	self.scons_ext_param = ""  # None value are not accepted
	self.scons_path = None     # Scons path


    def run(self):
        # Run others commands
        self.run_command("scons")

        # Add lib_dirs and include_dirs in packages
        for d in (self.distribution.lib_dirs,
                  self.distribution.inc_dirs,
                  self.distribution.bin_dirs,
                  self.distribution.share_dirs,
                  ):
            if(d):
                
                if(not os.path.exists(self.build_lib)):
                    self.mkpath(self.build_lib)

                for (name, dir) in d.items():
                    copy_data_tree(dir, pj(self.build_lib, name))

        return old_build_ext.run(self)


# Validation functions

def validate_create_namespaces(dist, attr, value):
    """ Validation for create_namespaces keyword """
    assert_bool(dist, attr, value)

    if(value and dist.namespace_packages):
        setuptools.command.build_py.build_py = build_py

def validate_scons_scripts(dist, attr, value):
    """ Validation for scons_scripts keyword """
    assert_string_list(dist, attr, value)
    if(value): 
        setuptools.command.build_ext.build_ext = build_ext
        set_has_ext_modules(dist)


def validate_shared_dirs(dist, attr, value):
    """ Validation for shared directories keywords"""
    try:
        assert_string_list(dist, attr, list(value.keys()))
        assert_string_list(dist, attr, list(value.values()))

        if(value):
            # Change commands
            setuptools.command.build_ext.build_ext = build_ext
            setuptools.command.install.install = install
            set_has_ext_modules(dist)

    except (TypeError,ValueError,AttributeError,AssertionError):
        raise DistutilsSetupError(
            "%r must be a dict of strings (got %r)" % (attr,value)
        )
    

def validate_postinstall_scripts(dist, attr, value):
    """ Validation for postinstall_scripts keyword"""
    try:
        assert_string_list(dist, attr, value)

        if(value):
            # Change commands
            setuptools.command.install.install = install

    except (TypeError,ValueError,AttributeError,AssertionError):
        raise DistutilsSetupError(
            "%r must be a list of strings (got %r)" % (attr,value)
        )


def write_keys_arg(cmd, basename, filename, force=False):
    """ Egg-info writer """
    argname = os.path.splitext(basename)[0]
    value = getattr(cmd.distribution, argname, None)
    if value is not None:
        value = '\n'.join(value.keys())+'\n'
    cmd.write_or_delete_file(argname, filename, value, force)
    


# SCons Management
        

class SconsError(Exception):
   """Scons subprocess Exception"""

   def __str__(self):
	return "Scons subprocess has failed."


class scons(Command):
    """
    Call SCons in an external process.
    """

    description = "Run SCons"
    
    user_options =[( 'scons-ext-param=',
                    None,
                    'External parameters to pass to scons.' ),
		  ( 'scons-path=',
                    None,
                    'Optional scons executable path. eg : C:\Python24\scons.bat for windows.' )]


    def initialize_options (self):
        self.outfiles = None
        self.scons_scripts = []   #scons directory
        self.scons_parameters = [] #scons parameters
	self.build_dir = None        #build directory
	self.scons_ext_param = None  #scons external parameters
	self.scons_path = None


    def finalize_options (self):

        # Set default values
        try:
            self.scons_scripts = self.distribution.scons_scripts
            self.scons_parameters = self.distribution.scons_parameters
        except:
            pass

        if(not self.scons_parameters):
            self.scons_parameters = ""

        self.set_undefined_options('build_ext',
                                   ('build_lib', 'build_dir'),
                                   ('scons_ext_param', 'scons_ext_param'),
                                   ('scons_path', 'scons_path'))


    def get_source_files(self):
        return []
        

    def run (self):
        """
        Run scons command with subprocess module if available.
        """
        if(not self.scons_scripts):
            return

        # try to import subprocess package
        try:
            import subprocess
            subprocess_enabled = True
        except ImportError:
            subprocess_enabled = False
            
        # run each scons script from setup.py
        for s in self.scons_scripts:
            try:
                # Join all the SCons parameters.
                file_param = '-f %s' % (s,)
                
		# Join all parameters strings from setup.py scons_parameters list
                param = ' '.join(self.scons_parameters)
                
		# Integrated Build parameter
                build_param = 'python_build_dir=%s ' % ( self.build_dir,)
                build_param += 'py_pkg_name=%s ' % ( self.distribution.metadata.get_name(),)
                
		# External parameters (from the command line)
		externp = self.scons_ext_param
	
		if(self.scons_path):
		    command = self.scons_path
		else:
		    command = 'scons'

                command_param = file_param + ' ' + build_param + ' ' + param + ' ' + externp
		commandstr = command + ' ' + command_param
                
                print commandstr

                # Run SCons
                if( subprocess_enabled ):
                    retval = subprocess.call(commandstr, shell=True)
                else:
                    retval =os.system(commandstr)
		    
                # Test if command success with return value
		if( retval != 0 ) :
                   raise SconsError()

            except SconsError, i:
		print i, " Failure..."
		sys.exit(1)  

            except Exception, i:
                print "!! Error : Cannot execute scons command:", i,
                print " Failure..."
		sys.exit(1)


# Namespace Creation

class create_namespaces(Command):
    """
    Create namespace packages
    """

    description = "Create namespace packages"

    namespace_header = \
"""
try:
    import pkg_resources
    pkg_resources.declare_namespace(__name__)
except ImportError:
    import pkgutil
    __path__ = pkgutil.extend_path(__path__, __name__)

# Local setup for openalea subversion
try:
    from __init_path__ import set_path
    set_path()
except:
    pass

"""

    user_options = []


    def initialize_options (self):
	self.namespaces = []
        self.build_dir = None

    def finalize_options (self):
        # Set default values
        self.set_undefined_options('build',
                                   ('build_lib', 'build_dir'))
        try:
            self.namespaces = self.distribution.namespace_packages
            if(self.namespaces is None) : self.namespaces = []
#             # Add namespace to packages
#             for ns in self.namespaces:
#                 if(ns not in self.distribution.packages):
#                     self.distribution.packages.append(ns)


        except:
            pass


    def create_empty_namespace(self, name):
        """ Create a directory with a __init__.py """

        nsdir = pj(self.build_dir, name)
        
        if(not os.path.exists(nsdir)):
            self.mkpath(nsdir)

        initfilename = pj(nsdir, '__init__.py')
        
        if(not os.path.exists(initfilename)):
            f = open(initfilename, 'w')
            f.write(self.namespace_header)
            f.close()


    def run (self):
        """ Run command """
        
        for namespace in self.namespaces:
            print "creating %s namespace"%(namespace)
            self.create_empty_namespace(namespace)
        

        
# Installation


class install(old_install):
    """
    Overload install command
    Use alea_install instead of easy_install
    """
    def do_egg_install(self):
 
        alea_install = self.distribution.get_command_class('alea_install')

        cmd = alea_install(
            self.distribution, args="x", root=self.root, record=self.record,
        )
        cmd.ensure_finalized()  # finalize before bdist_egg munges install cmd

        self.run_command('bdist_egg')
        args = [self.distribution.get_command_obj('bdist_egg').egg_output]

        if setuptools.bootstrap_install_from:
            # Bootstrap self-installation of setuptools
            args.insert(0, setuptools.bootstrap_install_from)

        cmd.args = args
        cmd.run()
        setuptools.bootstrap_install_from = None




class alea_install(easy_install):
    """
    Overload easy_install to add
    - Environment variable
    - Postinstall Scripts
    """

    def finalize_options(self):

        # Add openalea package link
        if(not self.find_links) : self.find_links = ""
        self.find_links += " " + OPENALEA_PI
        self.dist = None

        easy_install.finalize_options(self)


    def run(self):

        self.set_system()
        easy_install.run(self)
        # Call postinstall
        self.postinstall(self.dist)

        # Set environment
        set_env()


    def set_system(self):
        """ Set environment """

        if("win" in sys.platform):
            # install pywin32
            try:
                pkg_resources.require("pywin32")

            except pkg_resources.DistributionNotFound:

                # install pywin32
                from setuptools.command.easy_install import main
                main(['-f', OPENALEA_PI, "pywin32"])
                
            try:
                pkg_resources.require("pywin32")
                bdir = get_base_dir("pywin32")
                pywin32lib = pj(bdir, "pywin32_system32")
                set_win_env(['PATH=%s'%(pywin32lib,),])
            except:
                pass
        


    def process_distribution(self, requirement, dist, deps=True, *info):
        ret = easy_install.process_distribution(self, requirement, dist, deps, *info)
        # save distribution
        self.dist = dist
 
        return ret


    def postinstall(self, dist):
        """ Call postinstall scripts """

        print "Post installation"
        if(dist):
            pkg_resources.require(dist.project_name)
            sys.path.append(dist.location)
                
        try:
            lstr = dist.get_metadata("postinstall_scripts.txt")
        except:
            lstr = []

        # Add pywin32 path
        if('win' in sys.platform):
            win32dir = pj(get_base_dir('pywin32'), 'pywin32_system32')

            if(win32dir not in os.environ['PATH']):
                os.environ['PATH'] += ";" + win32dir

        # process postinstall
        for s in pkg_resources.yield_lines(lstr):
            print "Executing %s"%(s)
            
            try:
                module  = __import__(s, globals(), locals(), s.split('.'))
                module.install()
                
            except Exception, e:
                print "Warning : Cannot execute %s"%(s,)
                print e




def set_env():
    """ Set environment variables """

    print "Setting environment variables"

    # Avoid local copy for setting environment variables
    path = sys.path[:]
    try:
        sys.path.remove(os.path.abspath('.'))
    except:
        pass
    
    lib_dirs = list(get_all_lib_dirs())
    bin_dirs = list(get_all_bin_dirs())
        
    print "The following directories contains shared library :", '\n'.join(lib_dirs), '\n'
    print "The following directories contains binaries :", '\n'.join(bin_dirs), '\n'

    set_win_env(['OPENALEA_LIB=%s'%(';'.join(lib_dirs+bin_dirs)),
                 'PATH=%OPENALEA_LIB%',])

    try:
        set_lsb_env('openalea',
                    ['OPENALEA_LIB=%s'%(':'.join(lib_dirs)),
                     'OPENALEA_BIN=%s'%(':'.join(bin_dirs)),
                     'LD_LIBRARY_PATH=$OPENALEA_LIB',
                     'PATH=$OPENALEA_BIN'
                     ])
    except:
        print "\nIMPORTANT !!!"
        print "Add the following lines to your /etc/profile or your ~/.bashrc :\n"
        print "# Set OpenAlea variables"
        print "$(/usr/bin/alea_config)"
        print ""
        return


    sys.path = path
