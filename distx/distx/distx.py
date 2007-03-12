# -*- python -*-
# -*- coding: cp1252 -*-
################################################################################
#
#       OpenAlea.DistX:  Distutils extension
#
#       Copyright or © or Copr. 2006 INRIA - CIRAD - INRA  
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
################################################################################

__doc__="""
This module extends the distutils package and adds:
  - external scons call
  - creation of a pure namespace ( python package with an empty __init__.py )
  - may install data outside  python directories (e.g. lib, headers for shared libraries ).
    Thus, we can share libraries between python packages (e.g. for common datastructures.)

  Some ideas are taken from Twisted distutils extensions.
"""

__license__= "Cecill-C"
__revision__=" $Id$ "


import os
from os.path import join as joindir
import sys
import re
from string import join, split
from shutil import copytree, copyfile

from distutils.core import Extension, Distribution, Command
from distutils.command.install import install
from distutils.command.build import build
from distutils.dep_util import newer
from distutils.util import convert_path, change_root
from distutils.dir_util import mkpath

from build_py import build_py as distx_build_py
from bdist_nsi import distx_bdist_nsi

################################################################################
# Define Exceptions

class SconsError(Exception):
   """Scons subprocess Exception"""

   def __str__(self):
	return "Scons subprocess has failed."


################################################################################

class distx_build(build):
    """
    Extends default build command with distx specific actions.
    """

    def initialize_options (self):
        build.initialize_options(self)
	self.scons_ext_param = ""  # None value are not accepted
	self.scons_path = None     # Scons path


    def has_scons_scripts(self):
        return self.distribution.has_scons_scripts()
    
    def has_namespace(self):
        return self.distribution.has_namespace()

    # Sub Commands
    sub_commands = []
    sub_commands.append( ('build_scons', has_scons_scripts) )
    sub_commands.append( ('build_namespace', has_namespace) )
    sub_commands.extend( build.sub_commands )

    # User options
    user_options = []
    user_options.extend( build.user_options )
    user_options.append( ( 'scons-ext-param=' ,
                           None,
                           'External parameters to pass to scons.' ) )
    user_options.append( ( 'scons-path=',
                           None,
                           'Optional scons executable path.'
                           'eg : C:\Python24\scons.bat for windows.' ) )

    


################################################################################


class build_scons (Command):
    """
    Allows to call scons in an external process.
    """

    description = "Run SCons in an external process."
    
    user_options =[( 'scons-ext-param=',
                    None,
                    'External parameters to pass to scons.' ),
		  ( 'scons-path=',
                    None,
                    'Optional scons executable path. eg : C:\Python24\scons.bat for windows.' )]


    def initialize_options (self):
        self.outfiles = None
        self.scons_scripts = None    #scons directory
        self.scons_parameters = None #scons parameters
	self.build_dir = None        #build directory
	self.scons_ext_param = None  #scons external parameters
	self.scons_path = None


    def finalize_options (self):
        
        # Set default values
        self.scons_scripts = self.distribution.scons_scripts
        self.scons_parameters = self.distribution.scons_parameters
        if( not self.scons_parameters ):
           self.scons_parameters = "" 

        self.set_undefined_options( 'build',
                                    ('build_lib', 'build_dir'),
                                    ('scons_ext_param', 'scons_ext_param'),
                                    ('scons_path', 'scons_path'))


    def get_source_files(self):
        return []
        

    def run (self):
        """
        Run scons command with subprocess module if availaible.
        """

        if( not self.scons_scripts ):
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
                param = ' '.join( self.scons_parameters )
                
		# Integrated Build parameter
                build_param = 'python_build_dir=%s ' % ( self.build_dir,)
                build_param += 'py_pkg_name=%s ' % ( self.distribution.metadata.get_name(),)
                
		# External parameters (from the command line)
		externp =self.scons_ext_param
	
		if(self.scons_path):
		    command = self.scons_path
		else:
		    command = 'scons'

                command_param = file_param + ' ' + build_param + ' ' + param + ' '+externp
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



class build_namespace (Command):
    """
    Create an empty namespace.
    """
    
    description = "Create empty namespaces"

    # No specific user options
    user_options = [] 


    def initialize_options (self):
        # Namespace name
        self.namespace = None 
        self.build_dir = None
        self.outfiles = []
        

    def finalize_options (self):
        # Set default values
        self.set_undefined_options('build',
                                   ('build_lib', 'build_dir'))

        self.namespace =self.distribution.namespace


    def get_source_files(self):
       return []
        

    def get_outputs(self):
       return self.outfiles


    def run (self):
        """
        Create one or several namespaces and sub namespaces if any. 
        """
        self.outfiles = []
        self.mkpath(self.build_dir)

        if(not self.namespace):
            return

        for namespace in self.namespace:
            namespacedir = self.build_dir+os.sep;

            # Process composite namespace (ex : name.subname.subname)
            for subnamespace in split(namespace, '.'):

                # Create directory
                namespacedir += subnamespace + os.sep
                self.mkpath( namespacedir )
                print "creating %s" % (namespacedir,)
                
                # Create __init__.py in each subnamespace
                newfile = joindir( namespacedir, '__init__.py' )
                if not os.path.exists( newfile ):
                   print "creating %s" % (newfile,)
                   f = open( newfile, 'w' )
                   f.write("# -*- python -*-")
                   f.write("# Automatically generated file.")
                   f.close()
                self.outfiles.append( newfile )
               
    
            
        

###############################################################################
# Install commands

class distx_install (install):
    """
    Main install command which extends default install command with
    distx specific actions.
    """
    
    def initialize_options (self):
        install.initialize_options(self)
	self.external_prefix = None

    def finalize_options (self):
	install.finalize_options(self)

    def has_namespace (self):
        return self.distribution.has_namespace()

    def has_external_data (self):
        return self.distribution.has_external_data()

    def has_win_var (self):
        return self.distribution.has_win_var()

    def has_lsb_var (self):
       return self.distribution.has_lsb_var()

    def has_freedesk_shortcut (self):
       return self.distribution.has_freedesk_shortcut()

    def has_win_shortcut (self):
       return self.distribution.has_win_shortcut()

    def has_winreg(self):
       return self.distribution.has_winreg()
        


    # Define sub command
    sub_commands = []
    sub_commands.extend( install.sub_commands )
    sub_commands.append( ( 'install_namespace', has_namespace ) )
    sub_commands.append( ( 'install_external_data', has_external_data ) )
    sub_commands.append( ( 'set_win_var', has_win_var ) )
    sub_commands.append( ( 'set_lsb_var', has_lsb_var ) )
    sub_commands.append( ( 'win_shortcut', has_win_shortcut ) )
    sub_commands.append( ( 'freedesk_shortcut', has_freedesk_shortcut ) )
    sub_commands.append( ( 'winreg', has_winreg ) )


    # Define user options
    user_options = []
    user_options.extend(install.user_options)
    user_options.append( ('external-prefix=',
                          None,
                          'Prefix directory to install external data.'),
                         )


class install_namespace(Command):
    """
    Install pure namespace
    """
    
    description = "install namespace"

    user_options = [('install-dir=', None, "directory to install namespaces to")]

    boolean_options = []


    def initialize_options (self):
        self.install_dir = None
        self.force = 0
        self.build_dir = None
        self.skip_build = None


    def finalize_options (self):
        self.set_undefined_options('build', ('build_lib', 'build_dir'))
        self.set_undefined_options('install',
                                   ('install_lib', 'install_dir'),
                                   ('force', 'force'),
                                   ('skip_build', 'skip_build'),
                                  )

    def run (self):
        if not self.skip_build:
            self.run_command('build_namespace')
        
        self.outfiles = self.copy_tree(self.build_dir, self.install_dir)


    def get_outputs(self):
        return self.outfiles or []


class install_external_data(Command):
    """
    Install external data (libraries, includes, documentation, ...).
    """

    description = "Install external data"

    # Specific user options
    user_options = []
    user_options.append(( 'external-prefix=',
                          None,
                          'Prefix directory to install external data.' ))
    user_options.append(( 'force',
                          'f',
                          'Force installation (overwrite existing files).' ))

    boolean_options = ['force']


    def initialize_options (self):
        self.external_prefix = None
        self.external_data = None
        self.root = None
        self.force = 0


    def finalize_options (self):
        self.set_undefined_options('install',
                                   ('external_prefix', 'external_prefix'),
                                   ('root', 'root'),
                                   ('force', 'force'),
                                  )
        
        self.external_data = self.distribution.external_data

        # We use openalea external prefix if no prefix specified
        if( not self.external_prefix ):
            try:
                import openalea
                self.external_prefix= openalea.config.prefix_dir
                print 'INFO: Using OpenAlea prefix %s for external_prefix.' % (self.external_prefix,)
            except ImportError:
                print "!!ERROR: OpenAlea config not found. Use --external-prefix option instead.\n"
                sys.exit(1)
            

    def run (self):
        """Run install command"""
        if self.external_data:
            self.copy_external_data()


    def copy_data_tree (self, src, dst, exclude_pattern=['(RCS|CVS|\.svn)', '.*\~']):
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
             ret = self.copy_data_tree(src_name, dst_name, exclude_pattern)
             outfiles += ret

          else:
             copyfile(src_name, dst_name)
             outfiles.append(dst_name)

       return outfiles
  

    def copy_external_data (self):
        """
        Copy external data to final directory.
        """
        print "Install external data ", 

	if( self.external_prefix ):
            self.external_prefix= os.path.normpath(self.external_prefix)
            print "with prefix : ", self.external_prefix
        
        self.outfiles = []

	for (dest, src) in self.external_data.items():
           try:
                    
              # Define destination directory
              if(self.external_prefix and not os.path.isabs(dest)):
                 dest = joindir(self.external_prefix,dest)

              dest=os.path.normpath(dest)
                                   
              # Define root directory (for bdist compatibility)
              if self.root:
                 dest = change_root(self.root, dest)
                    
              mkpath(dest)

              self.outfiles += self.copy_data_tree(src, dest)

           except Exception, i:
              print i



    def get_inputs (self):
        return self.distribution.external_data


    def get_outputs(self):
        return self.outfiles


import varenv

class set_lsb_var (Command):
    """
    Set environment variable on ldb compatible platform.
    set_lsb_var=[ 'LD_LIBRARY_PATH=/usr/foo', 'FOO=bar' ]:
      - Add /usr/foo to LD_LIRABRY_PATH environment variable.
      - For other variables, create or replace the value.
    """
    
    description = "Set environment variable on lsb compatible platform"
    
    user_options = []

    def initialize_options (self):
       self.set_lsb_var = None

    def finalize_options (self):
       self.set_lsb_var = self.distribution.set_lsb_var


    def get_outputs(self):
        return []


    def run (self):
       varenv.set_lsb_env(self.distribution.get_name(), self.set_lsb_var)


class set_win_var (Command):
    """
    Set environment variable on windows platform.
    set_win_var=[ 'PATH=C:\lib', 'FOO=C:\foo\' ]:
      - Add C:\lib to PATH environment variable.
      - For other variables, create or replace the value.
    """
    
    description = "Set environment variable on windows platform"
    
    user_options = []

    def initialize_options (self):
       self.set_win_var = None


    def finalize_options (self):
       self.set_win_var = self.distribution.set_win_var


    def get_outputs(self):
        return []


    def run (self):
       varenv.set_win_env(self.set_win_var)



# Shortcut
import shortcut as shortcut_py

class freedesk_shortcut (Command):
    """
    """
    
    description = "Add a shortcut on Free desktop compatible system"
    
    user_options = []

    def initialize_options (self):
       self.freedesk_shortcut = None

    def finalize_options (self):
       self.shortcuts = self.distribution.freedesk_shortcuts

    def get_outputs(self):
        return []

    def run (self):
       for shortcut in self.shortcuts:

           shortcut.fill_with_metadata(self.distribution.metadata)
           if(not shortcut.target):
               print "ERROR : shortcut has no target parameter."
               return
            
           shortcut_py.CreateFDShortCut(shortcut.name,
                                     shortcut.target,
                                     shortcut.arguments,
                                     shortcut.version,
                                     shortcut.icon,
                                     shortcut.description,
                                     shortcut.group)


class win_shortcut (Command):
    
    description = "Add a shortcut on Win32 compatible system"
    
    user_options = []

    def initialize_options (self):
       self.shortcuts = None

    def finalize_options (self):
       self.shortcuts = self.distribution.win_shortcuts

    def get_outputs(self):
       return []

    def run (self):
        
       for shortcut in self.shortcuts:

           shortcut.fill_with_metadata(self.distribution.metadata)
           if(not shortcut.target):
               print "ERROR : shortcut has no target parameter."
               return

           shortcut_py.CreateWinShortCut(shortcut.name, shortcut.target,
                                      shortcut.arguments,
                                      os.path.dirname(shortcut.target),
                                      shortcut.icon,
                                      shortcut.description,
                                      shortcut.group)
           

class distx_winreg (Command):
    
    description = "Add a registery key on Win32 compatible system"
    
    user_options = []

    def initialize_options (self):
       self.winreg = []

    def finalize_options (self):
       self.winreg = self.distribution.winreg

    def get_outputs(self):
       return []

    def run (self):
       
       if((not 'win' in sys.platform) or (sys.platform == 'cygwin')):
          return
       try:
          import _winreg 

       except ImportError, e:
          print "!!ERROR: Can not access to Windows registry."
          return

       for (key, subkey, name, value) in self.winreg:

          if(name and value):
             _winreg.SetValue(key, subkey, name, value)




################################################################################

from distutils.command.bdist_rpm import bdist_rpm

class distx_bdist_rpm(bdist_rpm):
    """bdist_rpm command"""
    
    def finalize_options (self):
        """Ensure architecture name"""
        self.force_arch = os.uname()[4]
        bdist_rpm.finalize_options (self)
        


################################################################

from distutils.command.sdist import sdist


class distx_sdist (sdist):
    """
    Add external data in source distribution.
    """
    
    def add_defaults (self):
        sdist.add_defaults(self)
        self.filelist.extend(self.get_all_files(os.curdir))
        

    def get_all_files(self, basedir):
        """
        Return all the files under the base directory.
        """
        files= []
        for f in os.listdir(basedir):
           f = joindir( basedir, f )
           if os.path.isdir( f ):
              files += self.get_all_files( f )
           else:
              files.append( os.path.normpath( f ) )
        return files


    def prune_file_list (self):
        """
        Exclude files before generating MANIFEST.
        """
        sdist.prune_file_list (self)
        self.filelist.exclude_pattern(r'(RCS|CVS|\.svn)/.*', is_regex=1)
        self.filelist.exclude_pattern(r'(RCS|CVS|\.svn)\\.*', is_regex=1)
        self.filelist.exclude_pattern(r'.*\~', is_regex=1)
        self.filelist.exclude_pattern(r'^(.+/)*\..*', is_regex=1)
        self.filelist.exclude_pattern(r'^(.+\\)*\..*', is_regex=1)
        self.filelist.exclude_pattern(r'^build.*/', is_regex=1)
        self.filelist.exclude_pattern(r'dist/', is_regex=1)
        self.filelist.exclude_pattern(r'dist\\', is_regex=1)
        self.filelist.exclude_pattern(r'.*\.so$', is_regex=1)
        self.filelist.exclude_pattern(r'.*\.dll$', is_regex=1)
        self.filelist.exclude_pattern(r'.*\.pyd$', is_regex=1)
        self.filelist.exclude_pattern(r'.*\.pyo$', is_regex=1)
        self.filelist.exclude_pattern(r'.*\.pyc$', is_regex=1)
        self.filelist.exclude_pattern(r'.*\.os$', is_regex=1)
        


################################################################

class DistxDistribution(Distribution):
    """
    Main distribution class.
    Defines association between command strings and command classes
    and extend setup parameters.
    """
    
    def __init__(self,attrs=None):

        have_package_data = hasattr(self, "package_data")
        if not have_package_data:
            self.package_data = {}
            
        self.external_data = None
        self.namespace = None
        self.scons_scripts = None
        self.scons_parameters = None
        self.include_package_lib = True
        self.set_win_var = []
        self.set_lsb_var = []
        self.set_env_var = None # Deprecated

        self.win_shortcuts = []
        self.freedesk_shortcuts = []
        self.winreg = []

        Distribution.__init__(self,attrs)

        if(self.set_env_var != None):
           print "DistX Warning : set_env_var parameter is Deprecated !!\n"
           print "Use instead set_win_var and set_lsb_var parameters !!\n"

        if(set_win_var == None and set_env_var != None):
           self.set_win_var = self.set_env_var
        
        self.cmdclass = { 'install_namespace' : install_namespace,
                          'install_external_data' : install_external_data,
                          'set_win_var' : set_win_var,
                          'set_lsb_var' : set_lsb_var,
                          'win_shortcut' : win_shortcut,
                          'freedesk_shortcut' : freedesk_shortcut,
                          'install' : distx_install,
                          'build_scons' : build_scons,
                          'build_namespace' : build_namespace, 
                          'build' : distx_build,
                          'bdist_wininst' : distx_bdist_nsi,
                          'bdist_nsi' : distx_bdist_nsi,
                          'bdist_rpm' : distx_bdist_rpm,
                          'sdist' : distx_sdist,
                          'build_py': distx_build_py,
                          'winreg' : distx_winreg,
                         }


    def has_external_data(self):
        return bool(self.external_data)

    def has_win_var(self):
        return bool(self.set_win_var)

    def has_lsb_var(self):
       return bool(self.set_lsb_var)

    def has_win_shortcut(self):
       return bool(self.win_shortcuts)

    def has_winreg(self):
       return bool(self.winreg)

    def has_freedesk_shortcut(self):
        return bool(self.freedesk_shortcuts)

    def has_namespace(self):
        return bool(self.namespace)

    def has_scons_scripts(self):
        return bool(self.scons_scripts)


def setup(**attrs):
    "Setup overloaded"
    from distutils.core import setup
    attrs['distclass'] = DistxDistribution
    return setup(**attrs)
