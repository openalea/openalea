# -*- python -*-

import os, sys
from setuptools import setup
pj= os.path.join


name = 'OpenAlea.SConsx'
namespace = 'openalea'
pkg_name = 'openalea.sconsx'

version = '0.4.7'

description = 'Scons Extension to build multi-platform packages for OpenAlea and others.' 
long_description = \
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
author = 'Christophe Pradal'
author_email = 'christophe.pradal@cirad.fr'

# URL
url = 'http://openalea.gforge.inria.fr'

# LGPL compatible INRIA license
license = 'Cecill-C' 

setup(name = name,
      version = version,
      description = description,
      long_description = long_description,
      author = author,
      author_email = author_email,
      license = license,

      namespace_packages = ['openalea'],
      create_namespaces = True,
      zip_safe = False,

      packages = ["openalea.sconsx", "openalea.sconsx.tools"],
      package_dir = { pkg_name : pj('src','sconsx'),
                      '' : 'src'},

      # Dependencies
      setup_requires = ['openalea.deploy'],
      install_requires = [],
      dependency_links = ['http://openalea.gforge.inria.fr/pi'],
      )
