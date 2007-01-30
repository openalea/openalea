====== OpenAlea.Config ======

**Authors** : OpenAlea consortium

**Institutes** : INRIA, CIRAD, INRA

**Type** : Pure Python package

**Status** : Stable

**License** : Cecill-C

===== About =====

OpenAlea.Config package configure the system in order to install OpenAlea packages. Particulary, 
it define the directory where the package will be installed.

**This package is necessary to install other openalea packages, but doesn't provide any user functionality.**

===== Installation =====

=== Download ===

OpenAlea is available on the [[http://gforge.inria.fr/projects/openalea/|GForge repositery]]

=== Requirements ===

  * [[http://www.python.org/download/|Python >= 2.3]]


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

== Configuration file ==

The config.py file contains system installation variables. 


namespace= 'openalea'
version= '0.0.2'
prefix_dir= r'/usr/local/openalea'
lib_dir= r'/usr/local/openalea/lib'
include_dir= r'/usr/local/openalea/include'
bin_dir= r'/usr/local/openalea/bin'

doc_dir=r'/usr/local/openalea/doc'
test_dir=r'/usr/local/openalea/test'
setting_dir=r'/usr/local/openalea'


Others packages will be able to use these variables to know where to be installed.

===== Quick Example =====


from openalea import config 

print config.version
print config.prefix_dir
print config.include_dir



