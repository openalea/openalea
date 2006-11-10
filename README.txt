OpenAlea main package
---------------------

Authors : OpenAlea consortium

Institutes : INRIA, CIRAD

Status : Python package

License : LGPL
About

OpenAlea package defines :

    * openalea python namespace.
    * openalea.config configuration module which defines the system variable.

This package is necessary to install other openalea packages, but doesn’t provide any user functionality.

Requirements
------------

OpenAlea have no requirement (it defines only basic configuration).

However, other packages will depend on this package.

Installation
------------

The create_config.py script create system configuration file. 
You can specify the OpenAlea directory with the --prefix option.

python create_config.py [--prefix=openalea_dir]
python setup.py install

Quick Example
-------------

from openalea import config 
 
print config.version
print config.prefix_dir
print config.include_dir

