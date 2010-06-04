====== Starter ======

**Authors** : Samuel Dufour-Kowalski /  Christophe Pradal 

**Institutes** : INRIA / CIRAD 

**Status** : Python package 

**License** : Cecill-C

**URL** : http://openalea.gforge.inria.fr

===== About =====

=== Description ===

Starter is a dummy package. It can be used as an example to create a new autonomous package which
will be compatible with other OpenAlea packages.



Starter package aims to demonstrate :

  *How to create a simple package with C++ wrappers.
  *How to create a simple SCons and SConsX SConstruct file. 
  *How to write the installer script setup.py with distutils and DistX.
  *How to write Unit Tests in python
  
=== Content ===

The starter package contains :

  *Meta informations files (README.TXT, AUTHORS.TXT, LICENSE.TXT).
  *General layout to reproduct for others packages (**please replace starter with your package name**).
  *Installation file (setup.py).
  *Autobuild scripts (SConstruct, src/cpp/SConscript, src/wrapper/SConscript).
  *C++ library (src/cpp, src/include).
  *C++ wrappers example with boost.python (src/wrapper).
  *Python package (src/starter).
  *Custom system configuration (options.py and setup.cfg).

Starter package is composed by two **demonstration** C++ libraries : ''libsceneobj_cpp'' and ''libscenecontainer_cpp''.
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

There is no need to install //starter// since it is an example package.

=== Utilisation ===

Starter must be adapted to your need. The default installation command is:

<code>
python setup.py install
</code>


===== How to adapt starter for your own package =====

  *Rename the main directory with the name of your package,
  *Rename the sub-directory ''src/starter'' with the name of your python package and add the python source in
this directory,
  *Remove unnecessary files.
  *Adapt the ''setup.py'' distribution file,
  *Adapt the meta information files : ''README.TXT'', ''AUTHORS.TXT'', ''LICENSE.TXT'',
  *Add documentation in the doc subdirectories,
  *Add examples in the examples directory,
  *Add test in the test subdirectory,

  *If you developpe C++ files, 
     *Use the ''src/include'', ''src/cpp'' and ''src/wrapper'' for your headers, source files and wrappers,
     *Adapt the ''SConsctruct'' and ''SConscript'' compilation scripts for your needs.

===== Documentation =====

Have a look to the tutorial "how to create an OpenAlea package" on the OpenAlea website.



	




