# -*- python -*-
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

__doc__="""
This module extends the distutils package and adds
 -external scons call
 -pure namespace
 -external data installation
"""

__license__= "Cecill-C"
__revision__=" $Id $ "


from distutils.core import Extension,Distribution,Command
from distutils.command.install import install
from distutils.command.build import build
from distutils.dep_util import newer
from distutils.util import convert_path, change_root
from os.path import join as joindir
from shutil import copytree, copyfile
from distutils.dir_util import mkpath
from string import join, split
import os,sys
import distx_wininst
import re

##################################################
# Exceptions

class SconsError(Exception):
   """Scons subprocess Exception"""

   def __str__(self):
	return "Scons subprocess has failed."




#################################################################

class distx_build(build):
    """distx_build command extends default build command with distx specific actions"""


    def initialize_options (self):
        build.initialize_options(self)
	self.scons_ext_param=""  # None value are not accepted
	self.scons_path=None     # Scons path


    def has_scons_scripts(self):
        return self.distribution.has_scons_scripts()
    
    def has_namespace(self):
        return self.distribution.has_namespace()
    
    # Sub Commands
    sub_commands = []
    sub_commands.append(('build_scons', has_scons_scripts))
    sub_commands.append(('build_namespace', has_namespace))
    sub_commands.extend(build.sub_commands)

    # User options
    user_options = []
    user_options.extend(build.user_options)
    user_options.append( ('scons-ext-param=' , None, "External parameters to pass to scons."))
    user_options.append( ('scons-path=' , None, "Optional scons executable path. eg : C:\Python24 for windows."))




##########################################################################


class build_scons (Command):
    """build_scons command allows to call scons in a external process"""
    
    description = "Build subdirectory with scons"
    
    user_options=[('scons-ext-param=' , None, "External parameters to pass to scons."),
		  ('scons-path=' , None, "Optional scons executable path. eg : C:\Python24\scons.bat for windows.")]

    def initialize_options (self):
        self.outfiles = None
        self.scons_scripts=None    #scons directory
        self.scons_parameters=None #scons parameters
	self.build_dir=None        #build directory
	self.scons_ext_param=None  #scons external parameters
	self.scons_path=None

    def finalize_options (self):
        
        # Set default values
        self.scons_scripts = self.distribution.scons_scripts
        self.scons_parameters=self.distribution.scons_parameters
        if(not self.scons_parameters) : self.scons_parameters="" 

        self.set_undefined_options('build',
                                   ('build_lib', 'build_dir'),
				   ('scons_ext_param', 'scons_ext_param'),
                                   ('scons_path', 'scons_path'))

    def get_source_files(self):
        return []
        
    def run (self):
        """ Run scons command with subprocess module if availaible"""
        if not(self.scons_scripts) or len(self.scons_scripts)==0:
            return

        #cwd=os.getcwd() #get current directory

        # try to import subprocess package
        try:
            import subprocess
            subprocess_enabled=True
        except ImportError:
            subprocess_enabled=False
            

        # run each scons script from setup.py
        for s in self.scons_scripts:
            try:
                #os.chdir(d)
                file_param='-f %s'%(s,)
                
		# Join all parameters strings from setup.py scons_parameters list
                param=join(self.scons_parameters, sep=' ')
                
		# Integrated Build parameter
                build_param='python_build_dir=%s py_pkg_name=%s'%(self.build_dir, self.distribution.metadata.get_name())
                
		# External parameters (from the command line)
		externp=self.scons_ext_param
	
		if(self.scons_path):
		    command=self.scons_path
		else:
		    command='scons'

		commandstr=command+' '+file_param+' '+build_param+' '+param+' '+externp
                
                print commandstr

                # Run SCons
                if(subprocess_enabled):
                   
                    retval=subprocess.call(commandstr, shell=True)
                else:
                   retval=os.system(commandstr)
		    
                # Test if command success with return value
		if(retval!=0) : raise SconsError()

            except SconsError, i:
		print i, " Exiting..."
		sys.exit()  

            except Exception, i:
                print "!!Error : Cannot execute scons command:", i, "Exiting..."
		sys.exit()

        # Return to origin directory
        #os.chdir(cwd)

class build_namespace (Command):
    """build_namespace command : Create an empty Namespace"""
    
    description = "Create empty namespaces"

    # No specific user options
    user_options=[] 

    def initialize_options (self):
        # Namespace name
        self.namespace=None 
        self.build_dir=None
        self.outfiles =None
        
    def finalize_options (self):
        
        # Set default values
        self.set_undefined_options('build',
                                   ('build_lib', 'build_dir'))

        self.namespace=self.distribution.namespace

    def get_source_files(self):
        return []
        
    def run (self):

        self.outfiles = []
        self.mkpath(self.build_dir)

        if(not self.namespace): return

        for namespace in self.namespace:
            namespacedir=self.build_dir+os.sep;

            # Process composite namespace (ex : name.subname.subname)
            for subnamespace in split(namespace, '.'):

                # Create directory
                namespacedir+=subnamespace+os.sep
                self.mkpath(namespacedir)
            
                # Create __init__.py in each subnamespace
                newfile=joindir(namespacedir, '__init__.py')
                f=open(newfile, 'w')
                self.outfiles.append(newfile)
                f.write("#Automatically generated file. Do not edit this file !")
                f.close()
            
        

#####################################################################################

class distx_install(install):
    """Main install command which extend default install command with distx specific actions"""
    
    def initialize_options (self):
        install.initialize_options(self)
	self.external_prefix = None
		
    def finalize_options (self):
	install.finalize_options(self)

    def has_external_data(self):
        return self.distribution.has_external_data()

    def has_env_var(self):
        return self.distribution.has_env_var()

    
    # Define sub command
    sub_commands = []
    sub_commands.extend(install.sub_commands)
    sub_commands.append(('install_external_data', has_external_data))
    sub_commands.append(('set_env_var', has_env_var))


    # Define user options
    user_options = []
    user_options.extend(install.user_options)
    user_options.append( ('external-prefix=' , None, "Prefix directory to install external data..."))
    


class install_external_data(Command):
    """install_external_data Command install external data (libraries, include, documentation...)"""

    description = "Install external data"

    # Specific user options
    user_options = [
	('external-prefix=' , None, "Prefix directory to install external data..."),
        ('force', 'f', "force installation (overwrite existing files)"),
        
    ]

    boolean_options = ['force']


    def initialize_options (self):
        self.external_prefix = None
        self.external_data= None
        self.root=None
        self.force = 0

    def finalize_options (self):
        self.set_undefined_options('install',
                                   ('external_prefix', 'external_prefix'),
                                   ('root', 'root'),
                                   ('force', 'force'),
                                  )
        
        self.external_data = self.distribution.external_data

        # We use openalea external prefix if no prefix specified
        if(not self.external_prefix):
            try:
                import openalea
                print 'USE OpenAlea config for external_prefix.'
                self.external_prefix=openalea.config.prefix_dir
            except ImportError:
                print "!!ERROR :  OpenAlea config not found. Use --external-prefix option instead\n";
                sys.exit(1)
            
        

    def run (self):
        """Run install command"""
        if self.external_data:
            self.copy_external_data()


    def copy_data_tree (self, src, dst, exclude_pattern=['(RCS|CVS|\.svn)', ".*\~"]):
       """Copy an entire directory tree 'src' to a new location 'dst'.
       @param exclude_pattern : a list of pattern to exclude"""
   
       names = os.listdir(src)
       mkpath(dst)
       outfiles=[]

       for p in exclude_pattern:
          names=filter( lambda x: not(re.match(p, x)) , names)
            
       for n in names:
          src_name = os.path.join(src, n)
          dst_name = os.path.join(dst, n)
                
          if os.path.isdir(src_name):
             ret=self.copy_data_tree(src_name, dst_name, exclude_pattern)
             outfiles+=ret

          else:
             copyfile(src_name, dst_name)
             outfiles.append(src_name)

       return outfiles
  

    def copy_external_data (self):
        """Copy external Data from build directory to final directory"""

        print "Install external data", 
	if(self.external_prefix and self.external_prefix!=""):
            self.external_prefix=os.path.normpath(self.external_prefix)
            print "with prefix : ", self.external_prefix
        
        self.outfiles = []

	for (dest, src) in self.external_data.items():
		try:
                    
                    # Define destination directory
		    if(self.external_prefix and not os.path.isabs(dest)):
	                    dest=joindir(self.external_prefix,dest)

                    dest=os.path.normpath(dest)
                    
                                   
                    # Define root directory (for bdist compatibility)
                    if self.root : dest = change_root(self.root, dest)
                    
                    mkpath(dest)

                    self.outfiles+=self.copy_data_tree(src, dest)

		except Exception, i:
			print i





    def get_inputs (self):
        return self.distribution.external_data or []

    def get_outputs(self):
        return self.outfiles or []
        


class set_env_var (Command):
    """Set environment variable on windows platform"""
    
    description = "Set environment variable on windows platform"
    
    user_options=[]

    def initialize_options (self):
       self.set_env_var=None
        
    def finalize_options (self):
        
       self.set_env_var=self.distribution.set_env_var

        
    def run (self):
       if('win' in sys.platform ):

          for v in self.set_env_var:
             self.add_env_var(v)


    def add_env_var(self, newvar):
       """Update any environment variable persistently by changing windows registry
       @param newvar : a string like 'var=value'
       if 'var' == 'PATH', then 'value' is added to Path
       """

       try:
          import _winreg 
          import os, sys
          from string import find

       except Exception, e:
          return
    

       def queryValue(qkey, qname):
          qvalue, type_id = _winreg.QueryValueEx(qkey, qname)
          return qvalue

       regpath = r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment'
       reg = _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)
       key = _winreg.OpenKey(reg, regpath, 0, _winreg.KEY_ALL_ACCESS)
        
       name, value = newvar.split('=')

       # Specific treatment for PATH variable
       if name.upper() == 'PATH':
          value=os.path.normpath(value)
          actualpath = queryValue(key, name)
          
          listpath=actualpath.split(';')                
          if(not value in listpath):
             value= actualpath + ';' + value
             print "ADD to PATH :", value
          else :
             value= actualpath
            
          if value:
             _winreg.SetValueEx(key, name, 0, _winreg.REG_EXPAND_SZ, value)
        

       _winreg.CloseKey(key)    
       _winreg.CloseKey(reg)                        

        

##########################################################

from distutils.util import get_platform
from distutils.command.bdist_rpm import bdist_rpm

class distx_bdist_rpm(bdist_rpm):
    """bdist_rpm command"""
    
    def finalize_options (self):
        """Ensure architecture name"""
        self.force_arch=os.uname()[4]
        bdist_rpm.finalize_options (self)
        


################################################################

from distutils.command.sdist import sdist


class distx_sdist (sdist):
    """sdist command : add external data"""
    
    def add_defaults (self):
        sdist.add_defaults(self)
        self.filelist.extend(self.get_all_files(os.curdir))
        

    def get_all_files(self, basedir):

        ldir=[]
        for f in os.listdir(basedir):
           longf=joindir(basedir,f)
           if os.path.isdir(longf):
              ldir+=self.get_all_files( longf)
           else:
              ldir.append(os.path.normpath(longf))

        filter(os.path.isfile, ldir)
        return ldir

    def prune_file_list (self):
        """exclude files before generating MANIFEST"""
        sdist.prune_file_list (self)
        self.filelist.exclude_pattern(r'/(RCS|CVS|\.svn)/.*', is_regex=1)
        self.filelist.exclude_pattern(r'.*\~', is_regex=1)
        self.filelist.exclude_pattern(r'^(.+/)*\..*', is_regex=1)
        self.filelist.exclude_pattern(r'build', is_regex=1)
        self.filelist.exclude_pattern(r'dist', is_regex=1)
        self.filelist.exclude_pattern(r'.*\.so$', is_regex=1)
        self.filelist.exclude_pattern(r'.*\.dll$', is_regex=1)
        self.filelist.exclude_pattern(r'.*\.pyc$', is_regex=1)
        self.filelist.exclude_pattern(r'.*\.os$', is_regex=1)
        

# Import extern class for bdist_wininst
from distx_wininst import *

        
class DistxDistribution(Distribution):
    """Main installation class
    Define association between command string and command classes
    and define setup extended parameters
    """
    def __init__(self,attrs=None):
        self.external_data  = None
        self.namespace=None
        self.scons_scripts  = None
        self.scons_parameters = None
        self.set_env_var=None

        Distribution.__init__(self,attrs)
        
                    
        self.cmdclass = { 'install_external_data':install_external_data,
                          'set_env_var' : set_env_var,
                          'install':distx_install,
                          'build_scons':build_scons,
                          'build_namespace': build_namespace, 
                          'build':distx_build,
                          'bdist_wininst':distx_bdist_wininst,
                          'bdist_rpm':distx_bdist_rpm,
                          'sdist':distx_sdist,
                         }

    def has_external_data(self):
        return self.external_data and len(self.external_data.items()) > 0

    def has_env_var(self):
        return self.set_env_var and len(self.set_env_var) > 0

    def has_namespace(self):
        return self.namespace and len(self.namespace) > 0


    def has_scons_scripts(self):
        return self.scons_scripts and len(self.scons_scripts) > 0


def setup(**attrs):
    "Setup overloaded"
    from distutils.core import setup
    attrs['distclass'] = DistxDistribution
    setup(**attrs)




        

    
