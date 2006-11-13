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

  build_scons :              Build subdirectory with scons
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

  Nota 2 : the command bdist_wininst is desactivated.
          This is because it is impossible with wininst python installer to install 3rd party data.
	   Use simple bdist_instead

Setup new parameters :

  scons_script : list of script to execute with scons (SConstruct)
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
          scons_script = ['./SConstruct'],
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

#GLOBAL PARAMETERS





class distx_build(build):
    """build command which extend default build command with distx specific actions"""


    def initialize_options (self):
        build.initialize_options(self)
	self.scons_ext_param="" #None value are not accepted
 	self.scons_path=None #scons path

    def has_scons_script(self):
        return self.distribution.has_scons_script()
    
    def has_namespace(self):
        return self.distribution.has_namespace()
    
    
    sub_commands = []
    sub_commands.extend(build.sub_commands)
    sub_commands.append(('build_scons', has_scons_script))
    sub_commands.append(('build_namespace', has_namespace))

    #define user options
    user_options = []
    user_options.extend(build.user_options)
    user_options.append( ('scons-ext-param=' , None, "External parameters to pass to scons."))
    user_options.append( ('scons-path=' , None, "Optional scons executable path. eg : C:\Python24 for windows."))




class SconsError(Exception):
   """Scons subprocess Exception"""

   def __str__(self):
	return "Scons subprocess has failed."



class build_scons (Command):
    """Build subdirectory with scons"""
    
    description = "Build subdirectory with scons"
    
    user_options=[('scons-ext-param=' , None, "External parameters to pass to scons."),
		  ('scons-path=' , None, "Optional scons executable path. eg : C:\Python24\scons.bat for windows.")]

    def initialize_options (self):
        self.outfiles = None
        self.scons_script=None #scons directory
        self.scons_parameters=None #scons parameters
	self.build_dir=None #build directory
	self.scons_ext_param=None #scons external parameters
	self.scons_path=None

    def finalize_options (self):
        
        #set default values
        self.scons_script = self.distribution.scons_script
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
        if not(self.scons_script) or len(self.scons_script)==0:
            return

        #cwd=os.getcwd() #get current directory

        #try to import subprocess package
        try:
            import subprocess
            subprocess_enabled=True
        except ImportError:
            subprocess_enabled=False
            

        #run each scons  script
        for s in self.scons_script:
            try:
                #os.chdir(d)
                file_param='-f %s'%(s,)
                
		#join all parameters strings for setup.py scons_parameters list
                param=join(self.scons_parameters, sep=' ') 
		#build parameter
		build_param='distutils_build_dir='+self.build_dir
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
        

class distx_bdist_wininst (bdist_wininst):
    """Desactivate bdist_wininst"""

#     def initialize_options (self):
#         bdist_wininst.initialize_options(self)
# 	self.external_prefix = None

#     def finalize_options (self):
#         bdist_wininst.finalize_options(self)
#         self.set_undefined_options('install',
# 				   ('external_prefix', 'external_prefix'),
#                                   )


    def run(self):
        if self.distribution.has_external_data():
            print """

BDIST_WININST command doesn't work properly with external_data.
Use instead simple BDIST command or other system installer.

"""
        else :
            bdist_wininst.run(self)


#     def create_extern_script(self):
#         """Create a install script to place external data in the rigth place"""

#         external_data=self.distribution.external_data

#         if(not external_data or len(external_data)==0): return
        
#         self.external_prefix=convert_path(self.external_prefix)
        
#         print 'import shutils'

# 	for (dest, src) in self.external_data.items():
        
#             #define destination directory
#             if(self.external_prefix and not os.path.isabs(dest)):
#                 dest=joindir(self.external_prefix,dest)

#             normal_install_dir=joindir(sys.prefix, dest)
#             final_install_dir=dest

#             print "shutil.copytree(%s, %s)"%(normal_install_dir, final_install)

        

        

class distx_sdist (sdist):
    """Desactivate sdist"""

    def run(self):
        if self.distribution.has_external_data():
            print """

SDIST command doesn't work properly with external_data.
Abording...
"""

class DistxDistribution(Distribution):
    """Main installation class
    Define association between command string and command classes
    and define setup extended parameters
    """
    def __init__(self,attrs=None):
        self.external_data  = None
        self.namespace=None
        self.scons_script  = None
        self.scons_parameters = None
        self.add_env_path=None
        
        Distribution.__init__(self,attrs)
        self.cmdclass = { 'install_external_data':install_external_data,
                          'install':distx_install,
                          'build_scons':build_scons,
                          'build_namespace': build_namespace, 
                          'build':distx_build,
                          'bdist_wininst':distx_bdist_wininst,
                          'sdist':distx_sdist,
                         }

    def has_external_data(self):
        return self.external_data and len(self.external_data.items()) > 0

    def has_namespace(self):
        return self.namespace and len(self.namespace) > 0


    def has_scons_script(self):
        return self.scons_script and len(self.scons_script) > 0




def setup(**attrs):
    "Setup overloaded"
    from distutils.core import setup
    attrs['distclass'] = DistxDistribution
    setup(**attrs)



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

        

    
