# -*- coding: utf-8 -*-
__revision__ = "$Id$"

import os, sys
from setuptools import setup
pj= os.path.join


from openalea.deploy.metainfo import read_metainfo
metadata = read_metainfo('metainfo.ini', verbose=True)
for key,value in metadata.iteritems():
    exec("%s = '%s'" % (key, value))

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

setup(name = name,
      version = version,
      description = description,
      long_description = long_description,
      author = authors,
      author_email = authors_email,
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
