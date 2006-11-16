# -*- coding: iso-8859-15 -*-

__doc__="""
Module=distx.py
Author=Samuel Dufour-Kowalski
Licence=Cecill-C

Version:"0.1.0"

Description:

distx.py is a distutils extension which add some specific options and command to distribute
OpenAlea packages.

Distutils new extra sub commands :

Build sub command:

  build_namespace :  	     Create empty namespaces
				No parameters

  build_scons :              Run scons scripts
				Use scons_scripts option from setup.py
				Use scons_parameters option from setup.py
				Use '--scons-ext-param=' for adding scons options from command line
				Use '--scons-path=' to specify scons program path.
				Distutils build directory is automatically passed as a parameter nammed 'distutils_build_dir'

Install sub command

  install_external_data :    Install external data
				Parameter '--external-prefix=' : base directory for external data 
				if destination directory is not absolute



  Nota : Scons is responsible to compile  external library. It does not interact with distutils. 
	Scons is first executed, before any other distutils command. 
	 You can transmit parameters to scons with setup.py in order to specify destination directory
         ex : external libraries can be put in src/lib
              boost.python libraries must be put in the python_package hierarchy
         However, final installation is managed by the distutils functions. 


Setup new parameters :

  scons_scripts : list of script to execute with scons (SConstruct)
  scons_parameters : list of strings to pass to scons as parameters
  namespace : list of strings defining namespace
  external_data : map with the form { destination directory :source directory } to install external data.
		 parameter 'external-prefix' is prepend to dest directory if dest is not absolute
  add_env_path : list of subdirectories to add to PATH environment variable
                      (only for nt os)

Usage:

from openalea.distx import setup 
from openalea import config #retrive openalea config file
from os.path import join as joindir

packagename='my_openalea_package'
namespace='openalea'

if __name__ == '__main__':
    setup(name=packagename,
          version='1.0',
          author='me',
          ...

          #Define where to execute scons
          #scons is responsible to put compiled library in the write place ( lib/, package/, etc...)
          scons_scripts = ['SConstruct'],
          #scons parameters  
          scons_parameters = [ 'lib=lib'],
      

          #define empty namespace
          namespace= [namespace],
          #pure python  packages
          packages= [namespace+'.'+my_openalea_package],
          #python packages directory
          package_dir= {namespace+'.'+my_openalea_package : joindir('src',my_openalea_package)},
      
          #add package platform libraries if any
          package_data= { namespace+'.'+my_openalea_package : ['*.so', '*.pyd', '*.dll']},
                     
	  #copy shared data in default OpenAlea directory
	  #map of 'destination subdirectory' : 'source subdirectory'
	  external_data={pj(config.prefix_dir, 'doc', name) : 'doc',
         	          pj(config.prefix_dir, 'examples', name): 'examples' ,
                	   pj(config.prefix_dir, 'test', name): 'test',
	                   pj(config.prefix_dir, 'include'):  pj('src', 'include'),
        	           pj(config.prefix_dir,'lib'):  pj('src','lib'),
        	           },

	  #ONLY FOR WINDOWS 
	  #Add to PATH environment variable for openalea lib
	  add_env_path=[pj(config.prefix_dir,'lib')]
          
"""


from distutils.core import Extension,Distribution,Command
from distutils.command.install import install
from distutils.command.build import build
from distutils.dep_util import newer
from distutils.util import convert_path, change_root
from os.path import join as joindir
from shutil import copytree
from distutils.dir_util import mkpath
from string import join, split
import os,sys
from distutils.command.bdist_wininst import bdist_wininst

#Exceptions

class SconsError(Exception):
   """Scons subprocess Exception"""

   def __str__(self):
	return "Scons subprocess has failed."


#####################################################"
# Utility functions

def add_env_var(newvar):
    """Update any environment variable persistently by changing windows registry
    newvar is a string like 'var=value'
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
    #specific treatment for PATH variable
    if name.upper() == 'PATH':
            
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

#################################################################

class distx_build(build):
    """build command which extend default build command with distx specific actions"""


    def initialize_options (self):
        build.initialize_options(self)
	self.scons_ext_param="" #None value are not accepted
 	self.scons_path=None #scons path

    def has_scons_scripts(self):
        return self.distribution.has_scons_scripts()
    
    def has_namespace(self):
        return self.distribution.has_namespace()
    
    
    sub_commands = []
    sub_commands.append(('build_scons', has_scons_scripts))
    sub_commands.append(('build_namespace', has_namespace))
    sub_commands.extend(build.sub_commands)

    #define user options
    user_options = []
    user_options.extend(build.user_options)
    user_options.append( ('scons-ext-param=' , None, "External parameters to pass to scons."))
    user_options.append( ('scons-path=' , None, "Optional scons executable path. eg : C:\Python24 for windows."))




##########################################################################


class build_scons (Command):
    """Build subdirectory with scons"""
    
    description = "Build subdirectory with scons"
    
    user_options=[('scons-ext-param=' , None, "External parameters to pass to scons."),
		  ('scons-path=' , None, "Optional scons executable path. eg : C:\Python24\scons.bat for windows.")]

    def initialize_options (self):
        self.outfiles = None
        self.scons_scripts=None #scons directory
        self.scons_parameters=None #scons parameters
	self.build_dir=None #build directory
	self.scons_ext_param=None #scons external parameters
	self.scons_path=None

    def finalize_options (self):
        
        #set default values
        self.scons_scripts = self.distribution.scons_scripts
        self.scons_parameters=self.distribution.scons_parameters
        if(not self.scons_parameters) : self.scons_parameters="" #None value are not accepted

	#set default values
        self.set_undefined_options('build',
                                   ('build_lib', 'build_dir'),
				   ('scons_ext_param', 'scons_ext_param'),
                                   ('scons_path', 'scons_path'))

    def get_source_files(self):
        return []
        
    def run (self):
        """Run scons command with subprocess if available"""
        if not(self.scons_scripts) or len(self.scons_scripts)==0:
            return

        #cwd=os.getcwd() #get current directory

        #try to import subprocess package
        try:
            import subprocess
            subprocess_enabled=True
        except ImportError:
            subprocess_enabled=False
            

        #run each scons  script
        for s in self.scons_scripts:
            try:
                #os.chdir(d)
                file_param='-f %s'%(s,)
                
		#join all parameters strings for setup.py scons_parameters list
                param=join(self.scons_parameters, sep=' ') 
		#build parameter
                build_param='python_build_dir=%s py_pkg_name=%s'%(self.build_dir, self.distribution.metadata.get_name())
		#external parameters
		externp=self.scons_ext_param
	
		if(self.scons_path):
		    command=self.scons_path
		else:
		    command='scons'

		commandstr=command+' '+file_param+' '+build_param+' '+param+' '+externp
                print commandstr
                
                if(subprocess_enabled): #subprocess call
                    retval=subprocess.call(commandstr, shell=True)
                    
                else: #standard os.system command
                    retval=os.system(commandstr)
		    
                #test id command has succeed
		if(retval!=0) : raise SconsError()

            except SconsError, i:
		print i, " Exiting..."
		sys.exit()  

            except Exception, i:
                print "Error : Cannot execute scons command:", i, "Exiting..."
		sys.exit()

        #return to origin directory
        #os.chdir(cwd)

class build_namespace (Command):
    """Create an empty Namespace"""
    
    description = "Create empty namespaces"

    
    user_options=[] #No specific user options

    def initialize_options (self):
        self.namespace=None #namespace name
        self.build_dir=None
        self.outfiles =None
        
    def finalize_options (self):
        
        #set default values
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
            #for each sub namespace
            for subnamespace in split(namespace, '.'):

                #create directory
                namespacedir+=subnamespace+os.sep
                self.mkpath(namespacedir)
            
                #create __init__.py in each subnamespace
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

    
    #define sub command
    sub_commands = []
    sub_commands.extend(install.sub_commands)
    sub_commands.append(('install_external_data', has_external_data))


    #define user options
    user_options = []
    user_options.extend(install.user_options)
    user_options.append( ('external-prefix=' , None, "Prefix directory to install external data..."))




class install_external_data(Command):
    """Sub Command which install external data"""

    description = "Install external data"

    #specific user options
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

        

    def run (self):
        """Run install command"""
        if self.external_data:
            self.copy_external_data()

        #ADD ENVIRONMENT VARIABLES for windows
        if('win' in sys.platform and self.distribution.add_env_path):

            for p in self.distribution.add_env_path:
                add_env_var("PATH="+ os.path.abspath(p))



  

    def copy_external_data (self):
        """Copy external Data from build directory to final directory"""

        print "Install external data", 
	if(self.external_prefix and self.external_prefix!=""): print "with prefix : ", self.external_prefix
	
        self.external_prefix=convert_path(self.external_prefix)

        self.outfiles = []

	for (dest, src) in self.external_data.items():
		try:
                    #define destination directory
		    if(self.external_prefix and not os.path.isabs(dest)):
	                    dest=joindir(self.external_prefix,dest)

                    #define root directory (for bdist)
                    if self.root : dest = change_root(self.root, dest)
                    self.mkpath(dest)

                    self.outfiles+=self.copy_tree(src, dest)

		except Exception, i:
			print i





    def get_inputs (self):
        return self.distribution.external_data or []

    def get_outputs(self):
        return self.outfiles or []
        

#########################################################################

class distx_bdist_wininst (bdist_wininst):
    """Desactivate bdist_wininst"""

    def initialize_options (self):
        bdist_wininst.initialize_options(self)
	self.external_prefix = None
        self.install_script=None

        name=self.distribution.metadata.get_name()
        self.post_install_name=name+'_postinstall_script.py'

        #add script if bdist_wininst command
        if(os.name=='nt'):
           if(not self.distribution.scripts or self.distribution.scripts=='') :
              self.distribution.scripts=[self.post_install_name]
           else:
              self.scripts.append(self.post_install_name)

        #change external prefix
        cmdobj=self.distribution.get_command_obj('install_external_data')
        cmdobj.external_prefix='__'+name+'__'+'bdist_wininst'

        
    def finalize_options (self):
        bdist_wininst.finalize_options(self)
        self.set_undefined_options('install',
				   ('external_prefix', 'external_prefix'),
                                  )
        

    def run(self):
        if(os.name!='nt') :
            print "bdist_wininst : No NT OS\n"
            return

        if self.distribution.has_external_data():

            scriptname=self.create_postinstall_script(self.install_script)
            self.install_script=scriptname

        bdist_wininst.run(self)


    def create_postinstall_script(self, initial_script):
        """Create a install script to place external data in the rigth place
        @param initial_script : name of the initial postinstall script or None
        @return the new post install script name
        """

        external_data=self.distribution.external_data
        if(not external_data or len(external_data)==0): return

        # open file to write
        outscript=file(self.post_install_name, 'w')
        
        self.external_prefix=convert_path(self.external_prefix)
        
        

        base_script_str="""
import os
import shutil
from distutils.dir_util import remove_tree, mkpath

def copyalltree (src, dst):
    "Copy an entire directory tree 'src' to a new location 'dst'.  "
    
    names = os.listdir(src)
    mkpath(dst)
    directory_created(dst)
            
    for n in names:
        src_name = os.path.join(src, n)
        dst_name = os.path.join(dst, n)

        if os.path.isdir(src_name):
            copyalltree(src_name, dst_name)

        else:
            shutil.copyfile(src_name, dst_name)
            file_created(dst_name)

def add_env_var(newvar):
    "Update any environment variable persistently by changing windows registry newvar is a string like 'var=value'"

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
    #specific treatment for PATH variable
    if name.upper() == 'PATH':
            
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

"""

        #write header
        outscript.write(base_script_str)

        #write external data installer
    	for (dest, src) in external_data.items():
        
            # define destination directory
            if(self.external_prefix and not os.path.isabs(dest)):
                    dest=joindir(self.external_prefix,dest)

        
            normal_install_dir=change_root(sys.prefix, dest)
            final_install_dir=dest
            #we move from c:\python24\dir to c:\dir directory 
            outscript.write("copyalltree(r\'%s\', r\'%s\')\n"%(normal_install_dir, final_install_dir))
            outscript.write("remove_tree(r\'%s\')\n"%(normal_install_dir))
            outscript.write("os.removedirs(os.path.dirname(os.path.abspath(r\'%s\')))\n"%(normal_install_dir))
           

        #add environment variable
        if(self.distribution.add_env_path):
            for p in self.distribution.add_env_path:
                outscript.write('add_env_var(\"PATH=\"+ os.path.abspath(r\'%s\'))'%(p,))


        #Call initial postinstall _script
        if(initial_script):
            try:
                importname= split(initial_script, '.')[0]
                outscript.write("import %s"%(importname,))
            except Exception, e:
                print '\n!! Warning !! Cannot include %s script in post install script.\n', e

        outscript.close()

        return self.post_install_name
        

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
        self.add_env_path=None

        Distribution.__init__(self,attrs)
        
        
                        
                
                    
        self.cmdclass = { 'install_external_data':install_external_data,
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

    def has_namespace(self):
        return self.namespace and len(self.namespace) > 0


    def has_scons_scripts(self):
        return self.scons_scripts and len(self.scons_scripts) > 0




def setup(**attrs):
    "Setup overloaded"
    from distutils.core import setup
    attrs['distclass'] = DistxDistribution
    setup(**attrs)




        

    
