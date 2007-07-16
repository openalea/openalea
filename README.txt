OpenAlea.Deploy

Install and deploy OpenAlea packages.


Dependencies
------------
This package is based on setuptools


Description
-----------
It defines some setuptool extensions
  
  setup keywords:
  
     scons_scripts = [] : list of SCons script to exectute at build time
     scons_parameters = [] : parameters to pass to scons
     create_namespace = True, : create directory with __init__ corresponding to namespace
     lib_dirs = ['lib'] : define the shared library directory
     inc_dirs = ['include'] : : define the shared include directory
     postinstall_scripts = [] : Define the python module to execute during installation

  setuptool commands :
  
     scons : call scons scripts
     create_namespace : create the namespace declared in package_namespaces
     alea_install : overide easy_install to command to manage postinstall scripts
     

