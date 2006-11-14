#!/usr/bin/env python

from distutils.core import setup

long_description= \
"""
Scons Configuration Utilities for OpenAlea.

SConsX is a set of tools to enhance multi platform configuration,
build and installation.
This package extend scons with:
    * automatic dependency between tools,
    * default path for library depending on the platform ( Linux, Windows or Cygwin )
    * automatic option settings
"""
setup(name="sconsx",
      version="0.1.0",
      description="Scons Configuration Utilities for OpenAlea",
      long_description= long_description,
      author="Christophe Pradal",
      author_email="christophe.pradal@cirad.fr",
      license="LGPL",
      packages=['sconsx','sconsx.tools'],
      package_dir = {'sconsx': 'src'}
     )
