#!/usr/bin/env python

from distutils.core import setup

long_description= \
"""
Scons Configuration Utilities for ALEA.

scons_util is a set of tools to enhance multi platform configuration, 
build and installation.
This package extend scons with:
    * automatic dependency between tools,
    * default path for library depending on the platform ( Linux or Windows )
    * automatic option setting
"""
setup(name="scons-utils",
      version="0.0.3",
      description="Scons Configuration Utilities for ALEA",
      long_description= long_description,
      author="Christophe Pradal",
      author_email="christophe.pradal@cirad.fr",
      license="LGPL",
      packages=['scons_util','scons_util.tools'],
      package_dir = {'scons_util': 'src'}
     )
