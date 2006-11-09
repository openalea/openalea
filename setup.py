"""
Copyright CIRAD, INRIA

...

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

description= "OpenAlea pure namespace"
author= "OpenAlea developpers team"
url= "http://openalea.gforge.inria.fr"
license="LGPL"

setup(
    name= config.namespace,
    version= config.version,
    description= description,
    author=author,
    url=url,
    license=license,

    #pure python  packages
    packages= [config.namespace],

    )
