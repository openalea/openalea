====== DistX ======

**Authors** : Samuel Dufour-Kowalski / Christophe Pradal

**Institutes** : INRIA, CIRAD

**Status** : Python package

**License** : Cecill-C

===== About =====

DistX is an OpenAlea package which extends python Distutils library to facilitate package installation. It provides :
  * **Scons** integration (external call).
  * **Empty namespace** creation.
  * **External data** installation (more complete than the distutils ''data_files''.
  * **Windows PATH** variable modification.


DistX defines new distutils extra commands :

=== Distutils build subcommands ===


  *//build_namespace// : Create empty namespaces. 
      * Use ''namespace'' option from //setup.py//.

   *//build_scons// : run scons scripts.
      * Use ''scons_scripts'' option from //setup.py//.
      * Use ''scons_parameter'' option from //setup.py//.
      *	Use ''--scons-ext-param='' for adding scons options from the command line.
      * Use ''--scons-path='' to specify scons program path from the command line.

Nota :Distutils build directory is automatically passed as a parameter nammed 'distutils_build_dir'

=== Distutils install subcommands ===

  *//install_external_data// :    Install external data
    * Use ''--external-prefix=''  to specify base directory for external data (if destination directory is not absolute) from the command line.



//Nota// : Scons is responsible to compile  external library. It does not interact with distutils. 
Scons is first executed, before any other distutils command. You can transmit parameters to scons with setup.py in order to specify destination directory.  However, final installation is managed by the distutils functions. 



=== Setup function new parameters ===

  * **scons_scripts** : list of scons script to execute (ex SConstr
  * **scons_parameters** : list of strings to pass to scons as parameters
  * **namespace** : list of strings defining namespace
  * **external_data** : map with the form { destination directory :source directory } to install external data.
Command line parameter ''--external-prefix='' is prepend to destination directory if the destination directory is not absolute.
  * **add_env_path** : list of subdirectories to add to PATH environment variable (only for win32 os)


===== Installation =====


=== Download ===

DistX is available on the [[http://gforge.inria.fr/projects/openalea/|GForge repositery]]

=== Requirements ===

DistX has no particular requirement (just Python and Scons if you use scons_build command).

However, when using DistX, it can be usefull to use the OpenAlea base package which define the system configuration, in order to retrieve openalea directory prefix.


=== Installation ===

<code bash>
python setup.py install
</code>


===== Quick Example =====

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
</code>


For a more complete exemple, see the [[packages:utilities:starter|starter]] package.
