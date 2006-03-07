#!/usr/bin/env python

from distutils.core import setup

long_description= \
"""
ALEA framework for plant modelling and simulation.

"""
setup(name="openalea",
      version="0.0.1",
      description="OpenAlea framework for plant modelling and simulation.",
      long_description= long_description,
      author="ALEA developper team",
      license="LGPL",
      packages=['alea','alea.kernel','alea.gui'],
      package_dir = {'alea':'alea','alea.kernel': 'alea/kernel/src','alea.gui':'alea/gui/src'}
     )
