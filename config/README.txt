OpenAlea.Config package
-----------------------

Authors : OpenAlea consortium

Institutes : INRIA, CIRAD

Status : Python package

License : Cecill-C
About

OpenAlea package defines :

    * openalea python namespace.
    * openalea.config configuration module which defines the system variable.

This package is necessary to install other openalea packages, but doesn’t provide any user functionality.

Requirements
------------

Python >= 2.3

OpenAlea have no other requirement (it defines only basic configuration).

However, other packages will depend on this package.


Quick install
-------------

Execute the install.py script. It will lauch a graphical dialog to configure OpenAlea and install it.

Custom install
--------------

The create_config.py script create system configuration file. 
You can specify the OpenAlea directory with the --prefix option.

python create_config.py [--prefix=openalea_dir]
python setup.py install



How to use OpenAlea configuration
------------------------

from openalea import config 
 
print config.version
print config.prefix_dir
print config.include_dir

