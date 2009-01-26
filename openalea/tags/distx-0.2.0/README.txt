OpenAlea.DistX
--------------

Authors    : Samuel Dufour-Kowalski / Christophe Pradal
Institutes : INRIA, CIRAD
Type       : Python package
Status     : Stable
License    : Cecill-C
URL        : http://openalea.inria.gforge.fr

===== About =====

DistX is an OpenAlea package which extends python Distutils (http://docs.python.org/lib/module-distutils.html) to facilitate package installation in the OpenAlea framework. 
It provides :

  * Scons integration (external call).
  * Empty namespace creation.
  * External data installation (more complete than the distutils ''data_files'').
  * Environment variable modification on Windows and LSB compatible linux distribution.
  * Shortcut menu creation on Windows and free desktop compatible systems.
  * Convenience functions to include large packages and platform dependant libraries. 
  * NSIS windows installer generation.

DistX doesn't change the standard distutils behaviour. It adds only new functionnalities. 


===== Installation =====

=== Download ===

DistX is available on the GForge repository : [[http://gforge.inria.fr/frs/?group_id=79&release_id=782|OpenAlea.DistX]]

=== Requirements ===

  * Python >=2.4, 
  * OpenAlea.Config : which define the OpenAlea configuration.
  * Scons (if you use scons_build command),

  * NSIS installer on Windows (http://nsis.sourceforge.net/)

=== Installation ===

== Binary install == 

Lauch the windows installer on Windows system or use the ''rpm'' command on Linux system.

== Source Package ==

python setup.py install


===== Using DistX (User point of view) =====

DistX has the same bahviour than Distutils. Please refer to the Distutils user documentation (http://docs.python.org/inst/inst.html)

== Install a source package (with openalea configuration detection) ==

python setup.py install

== Install a source package (with a specific destination for external data) ==

python setup.py install --external-prefix=/opt/openalea 
python setup.py install --external-prefix=D:\openalea 


== Build a source package ==

python setup.py build

== Other commands ==

To get command help, type :

python setup.py --help-command

or

python setup.py cmd-name --help


===== Distributing your package with DistX (Developer point of view) ====

Before using DistX as a developper, have a look to the Distutils developer documention (http://docs.python.org/dist/dist.html).

=== Writing your setup.py script===

# You can use distx in your setup.py as follow:

from openalea.distx import setup, find_packages, find_package_dir, Shortcut 
from openalea import config #retrieve openalea config file
from os.path import join as joindir

packagename = 'my_openalea_package'
namespace = 'openalea'

if __name__ == '__main__':
    setup(name = packagename,
          version = '1.0',
          author = 'me',
          description = '',
          url = '',
          license = '',
          ...

          # Define where to execute scons
          # Scons is responsible to put compiled library in the write place ( lib/, package/, etc...)
          scons_scripts = ['SConstruct'],
          # Scons parameters  
          scons_parameters = [ 'build_prefix=build-scons'],
      

          # Define empty namespace
          namespace= [namespace],
        
          # Packages
          packages= find_packages(where= 'src', namespace = namespace),
          package_dir= find_packae_dir(where='src', namespace = namespace), 
      
          # Add package platform libraries if any
          include_package_lib = True,
                    
	      # Copy shared data in default OpenAlea directory
	      # Map of 'destination subdirectory' : 'source subdirectory'
	      external_data={ pj('doc', packagename) : 'doc',
            	          pj('examples', packagename): 'examples' ,
                	      pj('test', packagename): 'test',
	                      pj('include'):  pj('src', 'include'),
        	              pj('lib'):  pj('src','lib'),
        	            },

          # Add to PATH environment variable for openalea lib on Windows platform
          set_win_var=['PATH='+pj(config.prefix_dir,'lib')]
          set_lsb_var=['LD_LIBRARY_PATH='+pj(config.prefix_dir,'lib')]

          # Add shortcuts
          win_shortcuts = [Shortcut( name=name, target='c:\\python24\pythonw.exe', arguments='', group='OpenAlea', icon =''), ],
          freedesk_shortcuts = [Shortcut ( name = name, target = 'python', arguments = '', group = 'OpenAlea', icon='' )],
          
	  # Windows registery (key, subkey, name, value)
	  winreg = [('key', 'subkey', 'name', 'value')],


For a more complete exemple, see the Starter package.

== Create a Windows Installer (with the detection of the openalea configuration) ==

python setup.py bdist_nsi --nsis-dir="c:\Program Files\NSIS"

note : This require the installation of NSIS (http://nsis.sourceforge.net/)

== Create a RPM for linux==

python setup.py bdist_rpm

== Create a Source distribution ==

python setup.py sdist


===== Technical description =====

=== DistX commands  ===

DistX defines new distutils extra commands (available from the command lines) :

  install : Install the package. In addition to the default behaviour, ''install'' command call the ''install_external_data'' command.
      * Use ''--external-prefix='' to specify default base directory for external data. If not set, the system will try to use ''openalea.config.prefix_dir'' which is the openalea directory.

  install_namespace : Install pure namespaces.
      * Use ''install-dir='' to specify the directory to install namespaces to.

  install_external_data :    Install data outside the python layout distribution.
      * Use ''--external-prefix='' to specify default base directory for external data. If not set, the system will try to use ''openalea.config.prefix_dir'' which is the openalea directory.

  set_win_var : Set windows environment variables.

  set_lsb_var : Set environment variables on LSB compatible linux distributions. 
  
  set_win_var : Set windows environment variables.

  freedesk_shortcut : Create menu shorcuts on Freedesktop systems.
  
  win_shortcut : Create menu shorcuts on Windows systems.

  winreg : Add key in windows registery
  
  
  build : Build the package. In addition to the default behaviour, ''buil'' command call the ''build_namespace'' and ''build_scons'' command.

  build_namespace : Create empty namespaces. 

  build_scons : Run scons scripts to build platform dependant library.
      *	Use ''--scons-ext-param='' to pass to scons particular options.
      * Use ''--scons-path='' to specify scons program path.

  bdist_wininst or bdist_nsi : Create a windows installer. 
      * Use ''--external-prefix='' to set destination directory for external data
      By default the generated installer will use openalea directory

  bdist_rpm : create a linux rpm.



=== DistX setup parameters  ===

DistX add optional parameters to pass to setup in the ''setup.py'' script.

      * ''namespace'' : a list of strings corresponding to the namespaces to create.

      * ''scons_scripts'' : a list of string. Scons is called  for each script name in the list (ex : SConstruct).
      * ''scons_parameter'' a list of string. The strings are joined and passed as parameter to scons.
          Nota 1 : Distutils build directory is automatically passed as a parameter named 'distutils_build_dir'.
          Nota 2 : Scons is responsible to compile external library. It does not interact with distutils. 
          Scons is first executed, before any other distutils command. You can transmit parameters to scons with setup.py in order to specify destination directory.  
          However, final installation is managed by the distutils functions. 

      * ''include_package_lib'' : (True by default) include platform dependant libraries (.dll, .pyd, .so).
      * ''external_data'' : dictionnary with the form { destination directory : source directory }. Each source directory is copied to destination directory.

      * ''set_win_var'' : list of string with the form ''VAR=VALUE''. If ''VAR'' is ''PATH'', ''VALUE'' is added to the PATH variable. 
      In other case, the variable ''VAR'' is REPLACED by ''VALUE''. This parameter is only used on Windows platform.

      * ''set_lsb_var'' : list of string with the form ''VAR=VALUE''. If ''VAR'' is ''LD_LIBRARY_PATH'', ''VALUE'' is added to the variable.
      In other case, the variable ''VAR'' is REPLACED by ''VALUE''. This parameter is only used on Posix platform.
      
      * ''freedesk_shortcuts'' : list of Shortcut objects. A Shortcut oject is initialised with :
                                 name (link name), target (full executable path), arguments, group (menu category), icon (full path)
                                 
      * ''win_shortcuts'' : list of Shortcut objects. A Shortcut oject is initialised with :
                            name (link name), target (full executable path), arguments, group (menu category), icon (full path)
      
      * ''winreg'' : list of 4uples (key, subkey, name, value) defining the keys to add.
           
