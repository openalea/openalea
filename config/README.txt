OpenAlea.Config
---------------

OpenAlea.Config is the base package to configure OpenAlea installation directory
and environment variables.


License
-------

OpenAlea.Config is released under a Cecill-C License.

See LICENSE.txt
Nota : Cecill-C license is a LGPL compatible license.


Dependances
-----------

Python >= 2.4   (See http://www.python.org)


Installation
------------

python install.py


Documentation
-------------

See the web site : http://openalea.gforge.inria.fr

====== OpenAlea.Config ======


Technical description
---------------------

OpenAlea.Config provides :

  *''openalea'' python namespace.
  *''openalea.config'' configuration module which defines the system variables.
  * It declares the openalea shared directory for libraries, includes, data...
  * It sets enviroment variable on your system.


Quick Example :

  from openalea import config 

  print config.version
  print config.prefix_dir
  print config.include_dir

