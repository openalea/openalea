"""
  OpenAlea.Config : Copyright 2006 CIRAD, INRIA
"""

try:
  from  openalea import config
except ImportError, e:
    error= """Please, run the command:
    python create_config.py
    or
    python create_config.py --prefix=/usr/local/openalea
    or
    python create_config.py --prefix=C:/openalea
    """
    raise Exception(error)

from distutils.core import setup

description= "OpenAlea namespace and configuration"
author= "OpenAlea developpers team"
url= "http://openalea.gforge.inria.fr"
license="Cecill-C"

setup(
    name= "OpenAlea.Config",
    version= config.version,
    description= description,
    author=author,
    url=url,
    license=license,

    #pure python  packages
    packages= [config.namespace],

    )


