====== $NAME ======

**Authors** : XXX

**Institutes** : INRIA / CIRAD 

**Status** : Python package 

**License** : Cecill-C

**URL** : http://openalea.gforge.inria.fr

===== About =====

=== Description ===

$NAME is a XXX



$NAME package aims to demonstrate :

  *How to create a simple package with C++ wrappers.
  *How to create a simple SCons and SConsX SConstruct file. 
  *How to write the installer script setup.py with distutils and DistX.
  *How to write Unit Tests in python
  
=== Content ===

The $NAME package contains :

  *Meta informations files (README.TXT, AUTHORS.TXT, LICENSE.TXT).
  *General layout to reproduct for others packages (**please replace $NAME with your package name**).
  *Installation file (setup.py).
  *Autobuild scripts (SConstruct, src/cpp/SConscript, src/wrapper/SConscript).
  *C++ library (src/cpp, src/include).
  *C++ wrappers example with boost.python (src/wrapper).
  *Python package (src/$name).
  *Custom system configuration (options.py and setup.cfg).

$NAME package is composed by two **demonstration** C++ libraries : ''libsceneobj_cpp'' and ''libscenecontainer_cpp''.
Each library is wrapped in two Python sub modules ''sceneobj'' and ''scenecontainer''


The dependencies between libraries are:

         +---------------------+             +---------------+
         | scenecontainer.pyd  |             | sceneobj.pyd  |
         +------------+--------+             +-------+-------+
                      |                              |
                     \|/                            \|/
         +------------+----------+        +----------+---------+
         |libscenecontainer_cpp. +------->+libsceneobj_cpp.so  |
         +-----------------------+        +--------------------+

The file ''examples/example1.py'' contains a python script which uses these wrapped libraries.

===== Installation =====

=== Download ===

Go to http://gforge.inria.fr/frs/?group_id=79

=== Requirements ===

* Scons >= 0.96.93
* SconsX
* OpenAlea.Deploy
* Boost.Python


=== Installation ===

There is no need to install //$NAME// since it is an example package.

=== Utilisation ===

$NAME must be adapted to your need. The default installation command is:

<code>
python setup.py install
</code>



===== Documentation =====

Have a look to the tutorial "how to create an OpenAlea package" on the OpenAlea website.



	




