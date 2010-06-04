How to create a new package automatically
#############################################

The main objective of this package is to make possible the creation of a package 
in a fully automatic way so that developers can create ready-to-use package with a
single command.

quickstart
===========


Once installed, the PackageBuilder package provides a script called `alea_create_package`, 
which is based on the class :class:`PackageBuilder` of the module :mod:`openalea.pkg_builder.layout`.
This script works as follows::


    alea_create_package --name newpackage --package NewPackage --release 0.8 --project openalea --languages cpp

where 

    * `name` is the physical name of the package (directory name and name used when import in python)
    * `package` is the name that appears in the egg filename e.g., VisuAlea in OpenAlea.VisuAlea
    * `release` will be used in the egg name and documentation
    * `languages` is the type of languages used in your pacakge. By default python is always setup but you may add other languages such as here , the CPP language.
    * `project` should be a valid project name: openalea or vplants or alinea.


The main objective of this package is to make possible the creation of a package 
in a fully automatic way so that developers can create ready-to-use package with a
single command.


check that the package is properly setup
=========================================

go in the new directory created for you (`newpackage` in the previous example) and type one of the standard command::

    python setup.py install
    python setup.py develop
    python setup.py nosetests 
