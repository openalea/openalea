====== DistX ======

Authors : Samuel Dufour-Kowalski / Christophe Pradal

Institutes : INRIA, CIRAD

Type : Python package

Status : Devel

License : Cecill-C

URL : http://openalea.inria.gforge.fr

===== About =====

DistX is an OpenAlea package which extends python Distutils library :
http://docs.python.org/lib/module-distutils.html|Distutils  

It provides :

  * Scons integration (external call).
  * Empty namespace creation.
  * External data installation (more complete than the distutils ''data_files'').
  * Windows environment variable modification.

DistX doesn't change the standard distutils behaviour. It adds only new functionnality. 


===== Installation =====


=== Download ===

DistX is available on http://gforge.inria.fr/projects/openalea/

=== Requirements ===

  * Python >=2.4, 
  * Scons (if you want use scons_build command),

=== Installation ===

python setup.py install


===== Using DistX =====

DistX has the same bahviour than Distutils. Please refer to Distutils documentation (http://docs.python.org/inst/inst.html)

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

//or//

python setup.py cmd-name --help




===== Distributing your package with DistX ====

== Create a Windows Installer (with the detection of the openalea configuration) ==

python setup.py bdist_wininst --with-remote-config 

== Create a RPM for linux==

python setup.py bdist_rpm

== Create a Source distribution ==

python setup.py sdist

=== Writing your setup.py script===

<code python>
#You can use distx in your setup.py as follow:

from openalea.distx import setup 
from openalea import config #retrieve openalea config file
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
          scons_parameters = [ 'build_prefix=build-scons'],
      

          #define empty namespace
          namespace= [namespace],
          #pure python  packages
          packages= [namespace+'.'+packagename],
          #python packages directory
          package_dir= {namespace+'.'+packagename : joindir('src',packagename)},
      
          #add package platform libraries if any
          package_data= { namespace+'.'+packagename : ['*.so', '*.pyd', '*.dll']},
                     
	  #copy shared data in default OpenAlea directory
	  #map of 'destination subdirectory' : 'source subdirectory'
	  external_data={pj('doc', packagename) : 'doc',
         	          pj('examples', packagename): 'examples' ,
                	   pj('test', packagename): 'test',
	                   pj('include'):  pj('src', 'include'),
        	           pj('lib'):  pj('src','lib'),
        	           },

          #Add to PATH environment variable for openalea lib on Windows platform
          set_env_var=['PATH='+pj(config.prefix_dir,'lib')]
</code>



===== Technical description =====

=== DistX commands  ===

DistX defines new distutils extra commands (available from the command lines) :

  * install : Install the package. In addition to the default behaviour, ''install'' command call the ''install_external_data'' command.
      * Use ''--external-prefix='' to specify default base directory for external data. If not set, the system will try to use ''openalea.config.prefix_dir'' which is the openalea directory.

  * install_namespace : Install pure namespaces.
      * Use ''install-dir='' to specify the directory to install namespaces to.

  * install_external_data  :    Install data outside the python layout distribution.
      * Use ''--external-prefix='' to specify default base directory for external data. If not set, the system will try to use ''openalea.config.prefix_dir'' which is the openalea directory.

  * set_env_var  : Set windows environment variables.


  * build  : Build the package. In addition to the default behaviour, ''buil'' command call the ''build_namespace'' and ''build_scons'' command.

  * build_namespace  : Create empty namespaces. 

  * build_scons  : Run scons scripts to build platform dependant library.
      *	Use ''--scons-ext-param='' to pass to scons particular options.
      * Use ''--scons-path='' to specify scons program path.

  * bdist_wininst  : Create a windows installer
      * Use ''--external-prefix='' to specify default base directory for external data. If not set, the system will try to use ''openalea.config.prefix_dir'' which is the openalea data directory.
      * Use ''--with-remote-config'' to create an installer which will retrieve OpenAlea configuration when the package is installed on a remote system. When the configuration is not found on the remote system, the installer will use ''--external-prefix'' value.


  * bdist_rpm  : create a linux rpm.



=== DistX setup parameters  ===

DistX add optional parameters to pass to setup in the ''setup.py'' script.

      * ''namespace'' : a list of strings corresponding to the namespaces to create.

      * ''scons_scripts'' : a list of string. Scons is called  for each script name in the list (ex : SConstruct).
      * ''scons_parameter'' a list of string. The strings are joined and passed as parameter to scons.
          * Nota 1  : Distutils build directory is automatically passed as a parameter named 'distutils_build_dir'.
          * Nota 2  : Scons is responsible to compile external library. It does not interact with distutils. Scons is first executed, before any other distutils command. You can transmit parameters to scons with setup.py in order to specify destination directory.  However, final installation is managed by the distutils functions. 

      * ''external_data'' : dictionnary with the form { destination directory : source directory }. Each source directory is copied to destination directory.

      * ''set_env_var'' : list of string with the form ''VAR=VALUE''. If ''VAR'' is ''PATH'', ''VALUE'' is added to the PATH variable. In other case, the variable ''VAR'' is REPLACED by ''VALUE''. This parameter is only used on Windows platform.
