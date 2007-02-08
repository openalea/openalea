# -*- python -*-

import os, sys
pj= os.path.join

try:
    from openalea.distx import setup
except ImportError:
    print """
ImportError : openalea.distx package not found.
Please, first install the openalea.distx package.
See http://openalea.gforge.inria.fr
"""
    sys.exit()


name= 'sconsx'
namespace= 'openalea'
pkg_name= namespace + '.' + name

version= '0.3.0'

description= 'Scons Extension to build multi-platform packages for OpenAlea and others.' 
long_description= \
"""
Scons Configuration Utilities for OpenAlea.

SConsX is a set of tools to enhance multi platform configuration,
build and installation.
This package extends scons with:
    * automatic dependency between tools,
    * default path for library depending on the platform ( Linux, Windows or Cygwin )
    * automatic option settings
    * Support for different compilers on Linux and Windows (e.g. gcc, msvc, mingw)
"""

# Author
author= 'Christophe Pradal'
author_email= 'christophe.pradal@cirad.fr'

# URL
url= 'http://openalea.gforge.inria.fr'

# LGPL compatible INRIA license
license= 'Cecill-C' 

setup(name= name,
      version= version,
      description= description,
      long_description= long_description,
      author= author,
      author_email= author_email,
      license=license,
      namespace=[namespace],
      packages= [ "openalea.sconsx", "openalea.sconsx.tools" ],
      package_dir= { pkg_name : 'src'}
      )
