====== OpenAlea.Config ======

Authors : OpenAlea consortium
Institutes : INRIA, CIRAD, INRA
Type : Pure Python package
Status : Stable
License : Cecill-C

===== About =====

OpenAlea.Config package configure the system in order to install OpenAlea packages. Particulary, 
it define the directory where the packages will be installed and adapt your environment to share dynamic libraries.

**This package is necessary to install other openalea packages, but doesn't provide any user functionality.**

===== Installation =====


OpenAlea is available here : http://gforge.inria.fr/projects/openalea


=== Requirements ===

  * Python >=2.3  : http://www.python.org/download



=== Binary Installer  ===

If you download a binary package (rpm or win32.exe), simply run the installer. 
In this case, the OpenAlea directory cannot be customised. The default OpenAlea installation
directory will be :

  * ''c:\openalea'' for windows systems.
  * ''/usr/local/openalea/'' for linux systems.

If you want to use an other directory, please use the source distribution.



=== Source Distribution  ===

In the case of a source distribution, first uncompress the archive file. 

  * Graphically, the ''install.py'' script display a dialog which create the configuration and install the package. Simply double click on the script to lauch it.

  * Or in a console, the ''create_config.py'' script create system configuration file. You can specify the OpenAlea directory with the ''--prefix'' option.

  python create_config.py --prefix=c:/openalea
  python setup.py install

or

  python create_config.py --prefix=/usr/local
  python setup.py install


===== Technical description =====

OpenAlea.Config provides :

  *''openalea'' python namespace.
  *''openalea.config'' configuration module which defines the system variables.
  * It declares the openalea shared directory for libraries, includes, data...
  * It sets enviroment variable on your system.


===== Quick Example =====

  from openalea import config 

  print config.version
  print config.prefix_dir
  print config.include_dir

