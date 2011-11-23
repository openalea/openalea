# -*- python -*-
#
#       OpenAlea.Deploy: OpenAlea setuptools extension
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA
#
#       File author(s): Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
"""Setuptools commands.

To extend setuptools, we have to replace setuptools function with our
own function.
"""

__license__ = "Cecill-C"
__revision__ = " $Id$ "

import os
import subprocess
import sys
import shutil
from distutils.errors import *
import stat

from os.path import join as pj
from setuptools import Command
from setuptools.dist import assert_string_list, assert_bool
from distutils.command.build import build as old_build
from setuptools.command.install_lib import install_lib as old_install_lib
from setuptools.command.build_py import build_py as old_build_py
from setuptools.command.build_ext import build_ext as old_build_ext
from setuptools.command.install import install as old_install
from setuptools.command.easy_install import easy_install as old_easy_install
from setuptools.command.develop import develop as old_develop
from distutils.command.clean import clean as old_clean

import distutils.command.build
import setuptools.command.build_py
import setuptools.command.build_ext
import setuptools.command.install
import setuptools.command.install_lib

from distutils.dist import Distribution

import pkg_resources
from distutils.errors import DistutilsSetupError
from distutils.util import convert_path
from distutils.dir_util import mkpath

import re
import new
import ConfigParser

from util import get_all_lib_dirs, get_all_bin_dirs, DEV_DIST
from install_lib import get_dyn_lib_dir
from util import get_base_dir, get_repo_list, OPENALEA_PI
from util import is_virtual_env
from environ_var import set_lsb_env, set_win_env

import install_lib


# Utility


def copy_data_tree(src, dst, exclude_pattern=['(RCS|CVS|\.svn)', '.*\~']):
    """
    Copy an entire directory tree 'src' to a new location 'dst'.

    :param exclude_pattern: a list of pattern to exclude.
    """
    names = os.listdir(src)
    mkpath(dst)
    outfiles = []

    for p in exclude_pattern:
        names = filter(lambda x: not(re.match(p, x)), names)

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
                dist.bin_dirs) or \
                dist.add_plat_name
    except:
        return dist.has_ext_modules()


def set_has_ext_modules(dist):
    """ Set new function handler to dist object """
    m = new.instancemethod(has_ext_modules, dist, Distribution)
    dist.has_ext_modules = m


class build(old_build):
    """ Override sub command order in build command """

    # We change the order of distutils because scons will install
    # extension libraries inside python repository.

    sub_commands = [('build_ext', old_build.has_ext_modules),
                    ('build_py', old_build.has_pure_modules),
                    ('build_clib', old_build.has_c_libraries),
                    ('build_scripts', old_build.has_scripts),
                   ]


class build_py(old_build_py):
    """
    Enhanced 'build_py'
    Create namespace
    """

    def initialize_options(self):
        old_build_py.initialize_options(self)
        self.scons_ext_param = ""  # None value are not accepted
        self.scons_path = None     # Scons path

    def run(self):
        # Run others commands
        self.run_command("create_namespaces")

        # Add share_dirs
        d = self.distribution.share_dirs
        if (d):
            if (not os.path.exists(self.build_lib)):
                self.mkpath(self.build_lib)

            for (name, dir) in d.items():
                copy_data_tree(dir, pj(self.build_lib, name))

        ret = old_build_py.run(self)
        return ret


class build_ext(old_build_ext):
    """
    Enhanced 'build_ext'
    Add lib_dirs and inc_dirs parameters to package parameter
    """

    # User options
    user_options = []
    user_options.extend(old_build_ext.user_options)
    user_options.append(('scons-ext-param=',
                           None,
                           'External parameters to pass to scons.'))
    user_options.append(('scons-path=',
                           None,
                           'Optional scons executable path.'
                           'eg : C:\Python25\scons.bat for windows.'))

    def initialize_options(self):
        old_build_ext.initialize_options(self)
        self.scons_ext_param = ""  # None value are not accepted
        self.scons_path = None     # Scons path

    def run(self):
        # Run others commands

        self.run_command("scons")
        self.run_command("cmake")

        # Add lib_dirs and include_dirs in packages
        # Copy the directories containing the files generated
        # by scons and the like.
        for d in (self.distribution.lib_dirs,
                  self.distribution.inc_dirs,
                  self.distribution.bin_dirs,
                  #self.distribution.share_dirs,
                  ):

            if (not d or self.inplace==1):
                continue

            if (not os.path.exists(self.build_lib)):
                self.mkpath(self.build_lib)

            for (name, dir) in d.items():
                copy_data_tree(dir, pj(self.build_lib, name))

        return old_build_ext.run(self)


class cmd_install_lib(old_install_lib):
    """ Overide install_lib command (execute build_ext before build_py)"""

    def build(self):
        if not self.skip_build:
            if self.distribution.has_ext_modules():
                self.run_command('build_ext')

            if self.distribution.has_pure_modules():
                self.run_command('build_py')

# Validation functions


def validate_create_namespaces(dist, attr, value):
    """ Validation for create_namespaces keyword """
    assert_bool(dist, attr, value)

    if (value and dist.namespace_packages):
        setuptools.command.build_py.build_py = build_py
        setuptools.command.develop.develop = develop


def validate_scons_scripts(dist, attr, value):
    """ Validation for scons_scripts keyword """
    assert_string_list(dist, attr, value)
    if (value):
        setuptools.command.build_ext.build_ext = build_ext
        distutils.command.build.build = build
        setuptools.command.install_lib.install_lib = cmd_install_lib
        set_has_ext_modules(dist)


def validate_cmake_scripts(dist, attr, value):
    """ Validation for cmake_scripts keyword """
    assert_string_list(dist, attr, value)
    if (value):
        setuptools.command.build_ext.build_ext = build_ext
        distutils.command.build.build = build
        setuptools.command.install_lib.install_lib = cmd_install_lib
        set_has_ext_modules(dist)


def validate_pylint_options(dist, attr, value):

    try:
        assert type(value[0]) == str
    except ValueError:
        raise ValueError("""options %s in the setup.py must be a  such as
            --disable-msg=C0103 that can be used as pylint options""" % attr)


def validate_pylint_packages(dist, attr, value):
    if isinstance(value, list):
        pass
    else:
        raise ValueError("""options %s in the setup.py must be a list of path
             where to find the python source files """ % attr)



def validate_bin_dirs(dist, attr, value):
    """ Validation for shared directories keywords"""

    try:
        assert_string_list(dist, attr, list(value.keys()))
        assert_string_list(dist, attr, list(value.values()))

        if (value):
            # Change commands
            setuptools.command.build_ext.build_ext = build_ext
            setuptools.command.install.install = install
            setuptools.command.install_lib.install_lib = cmd_install_lib
            setuptools.command.develop.develop = develop
            set_has_ext_modules(dist)


    except (TypeError, ValueError, AttributeError, AssertionError):
        raise DistutilsSetupError(
            "%r must be a dict of strings (got %r)" % (attr, value))


def validate_share_dirs(dist, attr, value):
    """ Validation for shared directories keywords"""
    try:
        assert_string_list(dist, attr, list(value.keys()))
        assert_string_list(dist, attr, list(value.values()))

        if (value):
            # Change commands
            setuptools.command.build_py.build_py = build_py
            setuptools.command.install.install = install
            set_has_ext_modules(dist)

    except (TypeError, ValueError, AttributeError, AssertionError):
        raise DistutilsSetupError(
            "%r must be a dict of strings (got %r)" % (attr, value))


def validate_postinstall_scripts(dist, attr, value):
    """ Validation for postinstall_scripts keyword"""
    try:
        assert_string_list(dist, attr, value)

        if (value):
            # Change commands
            setuptools.command.install.install = install

    except (TypeError, ValueError, AttributeError, AssertionError):
        raise DistutilsSetupError(
            "%r must be a list of strings (got %r)" % (attr, value))

def validate_add_plat_name(dist, attr, value):
    """ Validation for add_plat_name keyword"""
    try:
        assert_bool(dist, attr, value)

        if (value):
            # Change commands
            set_has_ext_modules(dist)

    except (TypeError, ValueError, AttributeError, AssertionError):
        raise DistutilsSetupError(
            "%r must be a boolean (got %r)" % (attr, value))

def write_keys_arg(cmd, basename, filename, force=False):
    """ Egg-info writer """

    argname = os.path.splitext(basename)[0]
    value = getattr(cmd.distribution, argname, None)
    if value is not None:
        value = '\n'.join(value.keys()) + '\n'
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

    user_options =[('scons-ext-param=',
                    None,
                    'External parameters to pass to scons.'),
                    ('scons-path=',
                    None,
                    'Optional scons executable path. eg : C:\Python25\scons.bat for windows.')]

    def initialize_options(self):
        self.outfiles = None
        self.scons_scripts = []   #scons directory
        self.scons_parameters = [] #scons parameters
        self.build_dir = None        #build directory
        self.scons_ext_param = None  #scons external parameters
        self.scons_path = None

    def finalize_options(self):

        # Set default values
        try:
            self.scons_scripts = self.distribution.scons_scripts
            self.scons_parameters = self.distribution.scons_parameters
        except:
            pass

        if (not self.scons_parameters):
            self.scons_parameters = ""

        self.set_undefined_options('build_ext',
                                   ('build_lib', 'build_dir'),
                                   ('scons_ext_param', 'scons_ext_param'),
                                   ('scons_path', 'scons_path'))

    def get_source_files(self):
        return []

    def run(self):
        """
        Run scons command with subprocess module if available.
        """
        if (not self.scons_scripts):
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
                file_param = '-f %s' % (s, )

                # Join all parameters strings from setup.py scons_parameters list
                param = ' '.join(self.scons_parameters)

                # Integrated Build parameter
                build_param = 'python_build_dir=%s ' % (self.build_dir, )
                build_param += 'py_pkg_name=%s ' % (self.distribution.metadata.get_name(), )

                # External parameters (from the command line)
                externp = self.scons_ext_param

                if (self.scons_path):
                    command = self.scons_path
                else:
                    command = 'scons'

                command_param = file_param + ' ' + build_param + ' ' + param + ' ' + externp
                commandstr = command + ' ' + command_param

                print commandstr

                # Run SCons
                if (subprocess_enabled):
                    retval = subprocess.call(commandstr, shell=True)
                else:
                    retval =os.system(commandstr)

                # Test if command success with return value
                if (retval != 0):
                    raise SconsError()

            except SconsError, i:
                print i, " Failure..."
                sys.exit(1)

            except Exception, i:
                print "!! Error : Cannot execute scons command:", i,
                print " Failure..."
                sys.exit(1)


# CMake Management

class CMakeError(Exception):
    """CMake subprocess Exception"""

    def __str__(self):
        return "CMake subprocess has failed."


class cmake(Command):
    """
    Call CMake in an external process.
    """

    description = "Run CMake"

    def initialize_options(self):
        self.cmake_scripts = []   #cmake directory
        self.build_dir = None        #build directory

    def finalize_options(self):

        # Set default values
        try:
            self.cmake_scripts = self.distribution.cmake_scripts
        except:
            pass


        self.set_undefined_options('build_ext',
                                   ('build_lib', 'build_dir'),
                                    )


    def run(self):
        """
        Run Cmake command with subprocess module if available.
        """
        if (not self.cmake_scripts):
            return

        # try to import subprocess package
        try:
            import subprocess
            subprocess_enabled = True
        except ImportError:
            subprocess_enabled = False


        # run each CMake script from setup.py
        for s in self.cmake_scripts:
            try:
                # Join all the SCons parameters.
                #file_param = s
                file_param = '../src'

                cmake_cmd = 'cmake'

                cmake_cmd_param = file_param
                commandstr = cmake_cmd + ' ' + cmake_cmd_param

                print commandstr

                if not os.path.isdir('build-cmake') :
                    os.mkdir('build-cmake')

                os.chdir('build-cmake')


                # Run CMake
                if (subprocess_enabled):
                    retval = subprocess.call(commandstr, shell=True)
                else:
                    retval =os.system(commandstr)

                # Test if command success with return value
                if (retval != 0):
                    raise CMakeError()


                make_cmd = 'make'
                commandstr = make_cmd

                # Run Make
                if (subprocess_enabled):
                    retval = subprocess.call(commandstr, shell=True)
                else:
                    retval =os.system(commandstr)

                # Test if command success with return value
                if (retval != 0):
                    raise CMakeError()

                os.chdir(os.pardir)

            except CMakeError, i:
                print i, " Failure..."
                sys.exit(1)

            except Exception, i:
                print "!! Error : Cannot execute cmake command:", i,
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

"""

    user_options = []

    def initialize_options(self):
        self.namespaces = []
        self.build_dir = None

    def finalize_options(self):
        # Set default values
        self.set_undefined_options('build',
                                   ('build_lib', 'build_dir'))
        try:
            self.namespaces = self.distribution.namespace_packages
            if (self.namespaces is None):
                self.namespaces = []
#             # Add namespace to packages
#             for ns in self.namespaces:
#                 if (ns not in self.distribution.packages):
#                     self.distribution.packages.append(ns)
        except:
            pass

    def create_empty_namespace(self, name):
        """ Create a directory with a __init__.py """

        nsdir = pj(self.build_dir, name)

        if (not os.path.exists(nsdir)):
            self.mkpath(nsdir)

        initfilename = pj(nsdir, '__init__.py')

        if (not os.path.exists(initfilename)):
            f = open(initfilename, 'w')
            f.write(self.namespace_header)
            f.close()

    def run(self):
        """ Run command """

        for namespace in self.namespaces:
            print "creating %s namespace"%(namespace)
            self.create_empty_namespace(namespace)


# Installation


class install(old_install):
    """
    Overload install command
    Use alea_install instead of old_easy_install
    """

    user_options = []
    user_options.extend(old_install.user_options)
    user_options.append(('install-dyn-lib=',
                          None,
                          'Directory to install dynamic library.'))

    def initialize_options(self):
        old_install.initialize_options(self)
        self.install_dyn_lib = None

    def finalize_options(self):
        # Add openalea package link
        if (not self.install_dyn_lib):
            self.install_dyn_lib = get_dyn_lib_dir()
        self.install_dyn_lib = os.path.expanduser(self.install_dyn_lib)
        old_install.finalize_options(self)

    def do_egg_install(self):

        alea_install = self.distribution.get_command_class('alea_install')

        cmd = alea_install(
            self.distribution, args="x", root=self.root, record=self.record,
        )

        cmd.install_dyn_lib = self.install_dyn_lib
        cmd.ensure_finalized()  # finalize before bdist_egg munges install cmd

        self.run_command('bdist_egg')
        args = [self.distribution.get_command_obj('bdist_egg').egg_output]

        if setuptools.bootstrap_install_from:
            # Bootstrap self-installation of setuptools
            args.insert(0, setuptools.bootstrap_install_from)

        cmd.args = args
        cmd.run()
        setuptools.bootstrap_install_from = None


class alea_install(old_easy_install):
    """
    Overload old_easy_install to add

    - Environment variable
    - Postinstall Scripts
    """

    user_options = []
    user_options.extend(old_easy_install.user_options)
    user_options.extend([ ('install-dyn-lib=', None, 'Directory to install dynamic library.'),
                          ('gforge-login=',    None, "Login to connect to private gforge repository"),
                          ('gforge-passwd=',   None, "Password to connect to private gforge repository"),
                        ])

    def initialize_options(self):
        old_easy_install.initialize_options(self)
        self.install_dyn_lib = None
        self.gforge_login    = None
        self.gforge_passwd   = None

    def finalize_options(self):    
        # Add openalea package link
        repolist = get_repo_list()
        if (not self.find_links):
            self.find_links = ""
        self.find_links += " " + " ".join(repolist)

        self.dist = None

        # dynamic library installation path
        if (not self.install_dyn_lib):
            self.install_dyn_lib = get_dyn_lib_dir()

        self.install_dyn_lib = os.path.expanduser(self.install_dyn_lib)

        old_easy_install.finalize_options(self)

    def run(self):
        self.set_system()
        
        from openalea.deploy.gforge_util import add_private_gforge_repositories, find_login_passwd
        rc_user, rc_pass = find_login_passwd()
        self.gforge_login = self.gforge_login or rc_user
        self.gforge_passwd = self.gforge_passwd or rc_pass
        if self.gforge_login and self.gforge_passwd:
            add_private_gforge_repositories(self.gforge_login, self.gforge_passwd)
        
        old_easy_install.run(self)

        # Activate the correct egg
        self.dist.activate()
        if (self.dist.key in pkg_resources.working_set.by_key):
            del pkg_resources.working_set.by_key[self.dist.key]
        pkg_resources.working_set.add(self.dist)

	# Call postinstall
        self.postinstall(self.dist)

	# Set environment
        set_env(self.install_dyn_lib)


    def set_system(self):
        """ Set environment """
        if ("win32" in sys.platform):
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
                set_win_env(['PATH=%s'%(pywin32lib, ), ])
            except:
                pass

    def process_distribution(self, requirement, dist, deps=True, *info):
        """
        Just a way to retrieve the current distribution object.
        """
        ret = old_easy_install.process_distribution(self, requirement, dist, deps, *info)
        # save distribution
        self.dist = dist

        return ret

    def postinstall(self, dist):
        """ call postinstall scripts """
        print "Post installation"

        if (dist):
            pkg_resources.require(dist.project_name)
            sys.path.append(dist.location)

        try:
            lstr = dist.get_metadata("postinstall_scripts.txt")
        except:
            lstr = []

        # Add pywin32 path
        if ('win32' in sys.platform):
            try:
                win32dir = pj(get_base_dir('pywin32'), 'pywin32_system32')

                if (win32dir not in os.environ['PATH']):
                    os.environ['PATH'] += ";" + win32dir
            except:
                print "!!Error : pywin32 package not found. Please install it before."

        # process postinstall
        for s in pkg_resources.yield_lines(lstr):
            print "Executing %s"%(s)

            try:
                module = __import__(s, globals(), locals(), s.split('.'))
                module.install()

            except Exception, e:
                print "Warning : Cannot execute %s"%(s, )
                print e


def set_env(dyn_lib=None):
    """
    Set environment
    dyn_lib is the directory to install dynamic library
    """

    virtualenv = is_virtual_env()

    print "Install dynamic libs "

    #lib_dirs = list(get_all_lib_dirs())
    dyn_lib = install_lib.install_lib(dyn_lib)


    print "Setting environment variables"

    # Get all the dirs containing shared libs of the devel pkg
    # plus the global shared lib directory.
    lib_dirs = list(get_all_lib_dirs(precedence=DEV_DIST)) + [dyn_lib]
    bin_dirs = list(get_all_bin_dirs())

    print "The following directories contains shared library :", '\n'.join(lib_dirs), '\n'
    print "The following directories contains binaries :", '\n'.join(bin_dirs), '\n'

    # To fix the lost of access rights during the step of extract and instal .egg on Linux and MacOsX
    for d in bin_dirs:
        try:
            for f in os.listdir(d):
                filepath = os.path.join(d, f)
                if os.path.isfile(filepath):
                    if not os.access(filepath, os.X_OK):
                        os.chmod(filepath, stat.S_IRWXU | stat.S_IXGRP +  stat.S_IRGRP | stat.S_IXOTH + stat.S_IROTH)
        except:
            pass

    if (is_virtual_env()):
        print "EDIT the activate script to setup PATH and/or LD_LIBRARY_PATH"
        return

    all_dirs = set(lib_dirs + bin_dirs)
    set_win_env(['OPENALEA_LIB=%s'%(';'.join(all_dirs)),
                 'PATH=%OPENALEA_LIB%', ])

    try:
        vars = ['OPENALEA_LIB=%s'%(':'.join(lib_dirs)),
                'OPENALEA_BIN=%s'%(':'.join(bin_dirs)),
                'LD_LIBRARY_PATH=$OPENALEA_LIB',
                'PATH=$OPENALEA_BIN']
        if 'darwin' in sys.platform :
            vars.append('DYLD_LIBRARY_PATH=$OPENALEA_LIB')
            vars.append('DYLD_FRAMEWORK_PATH=$OPENALEA_LIB')
        set_lsb_env('openalea',vars)
    except:
        return


class develop(old_develop):
    """
    Overloaded develop command
    """

    # Redirect namespace
    # This is done when you have meta pacckages
    # in development mode.
    # It is an indirection to look for development directory
    # even if the directory path do not contain the namespace.
    redirect_ns = """
# Redirect path
import os

cdir = os.path.dirname(__file__)
pdir = os.path.join(cdir, "../../%s")
pdir = os.path.abspath(pdir)

__path__ = [pdir] + __path__[:]

from %s.__init__ import *
"""

    def initialize_options(self):
        """todo"""
        self.namespaces = []
        self.create_namespaces = False
        old_develop.initialize_options(self)

    def finalize_options(self):
        """todo"""
        try:
            self.namespaces = self.distribution.namespace_packages
            if (self.namespaces is None):
                self.namespaces = []
            self.create_namespaces = self.distribution.create_namespaces
        except:
            pass

        old_develop.finalize_options(self)
        # !! HACK !!
        # Modify inc, lib, share directory
        # We have to modify the path of the directories for scons.
        # When scons look for installation path of lib and inc,
        # we need build_scons/lib rather than lib because nothing is copied.
        for d in (self.distribution.lib_dirs,
                  self.distribution.inc_dirs,
                  self.distribution.bin_dirs,
                  self.distribution.share_dirs,
                  ):
            if (not d):
                continue
            for dest_dir, src_dir in d.items():
                # replace dest_dir by src_dir
                adir = os.path.join(self.setup_path, src_dir)
                d[adir] = adir
                del(d[dest_dir])

    def create_fake_namespace(self, name):
        """ Create namespace directory with a __init__.py """

        nsdir = pj(self.egg_path, name)
        if (not os.path.exists(nsdir)):
            self.mkpath(nsdir)

        initfilename = pj(nsdir, '__init__.py')

        if (not os.path.exists(initfilename)):
            f = open(initfilename, 'w')
            f.write(create_namespaces.namespace_header)
            f.close()

        # create indirection for each declared package
        for pkg_name in self.distribution.packages:

            full_pkg_name = pkg_name
            nsprefix = name + '.'
            if (not pkg_name.startswith(nsprefix)):
                continue

            # split name
            splitted = pkg_name.split('.')[1:]

            # keep only first order packages
            if (len(splitted)>1):
                continue

            # remove first component (ex for openalea.core.algo, we keep core.algo)
            pkg_name = splitted[0]

            # Create an __init__.py to redirect to real package directory
            pkg_dir = os.path.join(nsdir, pkg_name)

            if (not os.path.exists(pkg_dir)):
                self.mkpath(pkg_dir)

            initfilename = pj(pkg_dir, '__init__.py')

            if (not os.path.exists(initfilename)):
                f = open(initfilename, 'w')
                f.write(develop.redirect_ns%(pkg_name, full_pkg_name))
                f.close()

    def run(self):
        old_develop.run(self)

        # Redirect namespace
        if (self.create_namespaces):
            for namespace in self.namespaces:
                self.create_fake_namespace(namespace)

        # Set environment (i.e. copy libraries and env vars).
        # For develop, the libraries stay in place.
        set_env()


class egg_upload(Command):
    """ extension to setuptools to upload a distribution on the gforge

    :param release:  compulsory argument to specify the release name, as
        it appears on the gforge web site of Openalea, that is at
        https://gforge.inria.fr/frs/?group_id=79
    :param filename: a distribution filename or a regular expression such as ./dist/*egg
    :param login: your login name. will be asked later if not provided.
    :param password: your password. will be asked later if not provided.

    :Examples:

        >>> python setup.py egg_upload --filename dist/*egg --login name
        ... --release 0.7

    You can add the options in the setup.cfg::

        >>> [egg_dist]
        >>> filename = ./dist/*egg
        >>> login = yourname
    """

    description = "Upload the package on the OpenAlea GForge repository"

    user_options = [('login=', 'l', 'login name to the gforge'),
                    ('password=', None, 'your password to the gforge account'),
                    ('release=', None, 'release number. if not provided, try to obtain it from the setup.py'),
                    ('package=', None, 'name of the pacakge (compulsary)'),
                    ('project=', None, 'project [vplants, openalea] default:openalea'),
                    ('mode=', None, 'mode in [add, delete, query], default:add'),
                    ('glob=', None, 'a glob for filenames, if not provide, looks into ./dist/* '),
                    ('yes-to-all', None, 'reply yes to all questions (in particular it will overwrite existing files')]


    def initialize_options(self):
        self.login = None
        self.password = None
        self.glob = None
        self.release = None
        self.project = 'openalea'
        self.package = None
        self.yes_to_all = False
        self.dry_run = None
        self.mode = 'add'

    def finalize_options(self):

        if self.release is None:
            try:
                import warnings
                version = self.distribution.metadata.version
                self.release = '.'.join(version.split('.')[0:2])
                warnings.warn('Release not provided but found one in the setup.py (%s).' % self.release)
            except Exception, e:
                print e , 'release could not be found.'
                import sys
                sys.exit(0)

        if self.package is None:
            raise ValueError(" --package must be provided")

    def run(self):

        from openalea.misc.gforge_upload import Uploader
        from optparse import OptionParser
        parser = OptionParser()
        # here we need to have the destination names in agreement with prototype of Uploader class
        parser.add_option("--project", dest="project", default='openalea')
        parser.add_option("--package", dest="package", default=None)
        parser.add_option("--release", dest="release", default=None)
        parser.add_option("--login",    dest="login", default=None)
        parser.add_option("--mode",    dest="mode", default="add")
        parser.add_option("--password", dest="password", default=None)
        parser.add_option("--dry-run", dest="dry_run", default=None)
        parser.add_option("--glob", dest="glob", default=None)
        parser.add_option("--yes-to-all", dest="non_interactive", action="store_true", default=False)

        # now , we mimic the user arguments
        arguments = ' --mode %s' % self.mode
        arguments += ' --project %s' % self.project
        arguments += ' --package %s' % self.package
        arguments += ' --release %s' % self.release
        if self.login:
            arguments += ' --login %s' % self.login
        if self.glob:
            arguments += " --glob %s" % self.glob
        elif self.mode=='add':
            arguments += ' --glob dist/*egg'
        if self.dry_run:
            arguments += ' --dry-run %s' % self.dry_run
        if self.yes_to_all == 1:
            arguments += ' --yes-to-all '

        print 'Command that will be called is : \n\tgforge_upload %s' % arguments
        # password is afterwards so that it does not appear on the screen!
        if self.password:
            arguments += ' --password %s'%  self.password
        #and finally call the command
        (options, args) = parser.parse_args(arguments.split(" "))

        uploader = Uploader(options)
        uploader.run()



class pylint(Command):
    """ pylint extensions to setuptools

    There are two optional arguments, --pylint-packages and --pylint-options
    that can be provided in the setup.cfg file, or in the setup.py file, or as
    user arguments (see examples).

    The results (pylint's output) will be saved in the file .pylint.output

    :Examples:

        >>> python setup.py pylint
        >>> python setup.py pylint --pylint-packages
        >>> python setup.py pylint --pylint-options --disable-msg=C0103

    You can add the options in the setup.cfg::

        >>> [pylint]
        >>> pylint-packages = src/openalea/stat_tool,src/openalea/stat_tool
        >>> pylint-options = --disable-msg=C0103

    or the setup.py

        >>>  pylint_packages = ['src/openalea/stat_tool'],
        >>>  pylint_options = ['--disable-msg=C0103']


    """
    user_options = [('pylint-packages=', None, 'list of pathnames to parse with pylint'),
                    ('pylint-options=', None, 'optional arguments to pylint such as --disable-msg=C0103')]

    def initialize_options(self):
        self.output_filename = '.pylint.output'
        self.pylint_packages = None
        self.pylint_options = None
        self.pylint_base_options = ' --ignore=__wralea__.py '
        try:
            os.remove(self.output_filename)
        except:
            pass

    def finalize_options(self):
        # get the packages to give to pylint

        # if not defined in the setup.py or not provided as user arguments,
        # look into the setup.cfg
        if (not self.pylint_packages):
            self.pylint_packages = self.distribution.pylint_packages
            #print self.pylint_packages

        # if not defined in the setup.py or not provided as user arguments,
        # look into the setup.cfg
        if (not self.pylint_options):
            self.pylint_options = self.distribution.pylint_options

        # in the setup.cfg case or in the user arguments case, we have a
        # string (that we convert into a list)
        if isinstance(self.pylint_packages, str):
            self.pylint_packages = self.pylint_packages.split(',')

        # otherwise, we already have a list
        if self.pylint_options is None:
            self.pylint_options = ''


    def run(self):
        print '    PYLINT processing'
        if self.pylint_packages:
            #print '    Processing ' + self.pylint_packages + ' through pylint'
            cmd = 'pylint '
            for package in self.pylint_packages:
                cmd +=  package.replace('/', os.sep) + os.sep + '*.py '
            cmd += ' ' + self.pylint_options
            cmd += self.pylint_base_options
            print cmd
            status = subprocess.call(cmd,
                                     stdout=open(self.output_filename,'w+'),
                                     stderr=None, shell=True)
            if status!=0:
                print 'This command returns status (%s) different from 0.' % \
                    str(status)
            cmd = 'tail -n 1 %s ; grep \"Your code\"  %s ' % (self.output_filename, self.output_filename)
            subprocess.call(cmd, stdout=None, stderr=None, shell=True)
        else:
            raise('missing --pylint-packages in setup.py. skipped pylint processing')


class upload_sphinx(Command):
    """
    Upload sphinx documentation to the GForge repository (wiki)

    .. todo:: use gforge tools instead of scp ?
    """
    description = "Upload the documentation on the OpenAlea GForge repository"
    GFORGE_REPOSITORY = "http://gforge.inria.fr"
    DOMAIN = "scm.gforge.inria.fr"

    user_options = [
        ('repository=', 'r',
         "url of repository [default: %s]" % GFORGE_REPOSITORY),
        ('username=', 'u', "user id"),
        ('password=', 'p', "user password"),
        ('project=', None, None),
        ('package=', None, None),
        ('release=', None,None),
        ('unstable=', 'r', "put the documentation in the unstable repository"),
        ]

    def initialize_options(self):
        self.username = None
        self.password = None
        self.repository = self.GFORGE_REPOSITORY
        self.project = None
        self.package = None
        self.release = None
        self.unstable = True

    def finalize_options(self):
        if (not self.package):
            self.package = self.distribution.metadata.get_name()

        if not self.project:
            raise ValueError("""Project field missing. Provide it in your setup.cfg, in the [upload_sphinx] section.
                It should be either vplants, alinea or openalea. %s provided""" % self.project)
        elif self.project not in ['vplants','alinea','openalea']:
            raise ValueError("""Project must be vplants, alinea or openalea. Check your setup.cfg pupload_sphinx] section. %s provided""" % self.project)

        if self.unstable is True:
            print "Documentation will be uploaded to unstable directory"
            self.destination = '/home/groups/openalea/htdocs/beta_doc'
        else:
            print "Documentation will be uploaded to stable directory"
            self.destination = '/home/groups/openalea/htdocs/doc'

        if (not self.release):
            version = self.distribution.metadata.version
            try:
                versiontab = version.split(".")[:2]
                self.release = ".".join(versiontab)
            except IndexError:
                self.release = version

        if not self.username:
            self.username = raw_input('login:')
        # to be used with gforge tools only. not with scp tht is currently used.
        #if not self.password:
        #    self.password = raw_input('password:')

    def run(self):
        """.. todo:: fix this code so that gforge proxy and scp are not both used."""
        print """
                Warning: this option (sphinx_upload) will use the scp command to copy
                the documentation on the gforge. Be sure to have the right to do so.
                Requires to copy your ssh key on the server !
               """
        print "Copying files on the GForge. Be patient ..."

        self.test_and_build_dir()
        for output in  ['html' , 'latex']:

            cmd1 = 'scp -r %s %s@%s:%s/%s/%s/doc/_build/' \
                % ( os.path.join(os.getcwd(), 'doc', '_build', output),
                    self.username,
                    self.DOMAIN,
                    self.destination,
                    self.project,
                    self.package
                    )
            self.upload_file(cmd1)

    def test_and_build_dir(self):
        direc = "%s/%s/%s/doc/_build/"%(self.destination, self.project, self.package)

        cmd1 = 'ssh  %s@%s "if [ ! -d %s ]; then mkdir -p %s; fi;"' \
            % ( self.username,
                self.DOMAIN,
                direc,
                direc )

        print cmd1
        status = subprocess.call(cmd1 ,stdout=open('/tmp/test','w'),stderr=None, shell=True)
        if status!=0:
            print 'This command failed'
            import sys
            sys.exit(status)
        print "Ensured directory exists."



    def upload_file(self, command):
        print "Project: ", self.project
        print "Package: ", self.package
        print "Release: ", self.release
        print command
        status = subprocess.call(command ,stdout=open('/tmp/test','w'),stderr=None, shell=True)
        if status!=0:
            print 'This command failed'
            import sys
            #sys.exit(status)
        print "Files uploaded."


class alea_upload(Command):
    """
    Upload a package on the OpenAlea GForge repository
    """

    description = "Upload the package on the OpenAlea GForge repository"

    GFORGE_REPOSITORY = "http://gforge.inria.fr"

    user_options = [
        ('repository=', 'r',
         "url of repository [default: %s]" % GFORGE_REPOSITORY),
        ('username=', 'u', "user id"),
        ('password=', 'p', "user password"),
        ('project=', None, ""),
        ('package=', None, ""),
        ('release=', None, ""),

        ]

    def initialize_options(self):
        self.username = None
        self.password = None
        self.repository = self.GFORGE_REPOSITORY
        self.project = 'openalea'
        self.package = ''
        self.release = ''

    def finalize_options(self):
        if (not self.package):
            self.package = self.distribution.metadata.get_name()

        if (not self.release):
            version = self.distribution.metadata.version
            try:
                versiontab = version.split(".")[:2]
                self.release = ".".join(versiontab)
            except IndexError:
                self.release = version

        if 'HOME' in os.environ:
            rc = os.path.join(os.environ['HOME'], '.pypirc')
            if os.path.exists(rc):
                self.announce('Using PyPI login from %s' % rc)
                config = ConfigParser.ConfigParser({
                        'username': '',
                        'password': '',
                        'repository': ''})
                config.read(rc)
                if not self.repository:
                    self.repository = config.get('server-login', 'repository')
                if not self.username:
                    self.username = config.get('server-login', 'username')
                if not self.password:
                    self.password = config.get('server-login', 'password')

    def run(self):
        if not self.distribution.dist_files:
            raise DistutilsOptionError("No dist file created in earlier command")

        import gforge

        print "Login...."
        server = gforge.GForgeProxy()

        server.login(self.username, self. password)

        # Check package
        if (server.get_package_id(self.project, self.package) < 0):
            server.add_package(self.project, self.package)

        # Check release
        if (server.get_release_id(self.project, self.package, self.release) < 0):
            notes = ""
            changes = ""
            server.add_release(self.project, self.package, self.release, notes, changes)

        for command, pyversion, filename in self.distribution.dist_files:
            self.upload_file(server, command, pyversion, filename)

        print "Logout..."
        server.logout()

    def upload_file(self, server, command, pyversion, filename):

        print "Project: ", self.project
        print "Package: ", self.package
        print "Release: ", self.release
        print "Filename: ", filename

        server.add_file(self.project, self.package, self.release, filename)


class clean(old_clean):
    """
    Overloaded clean command

    If no SConstruct is found, there is no need to run scons -c, otherwise
    the command "scons -c" is launch
    """

    def run(self):
        old_clean.run(self)

        # Test if Sconstruct is present
        if os.path.isfile('SConstruct'):
            print 'Found an SConstruct file. Starting "scons -c" command'
            # Call scons -c: see the scons command#
            try:
                os.system('scons -c')
            except:
                print 'Failed to launch sconc -c'
        else:
            print 'No SConstruct found. Skipping "scons -c" command.'
