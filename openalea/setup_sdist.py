"""
  OpenAlea. Copyright 2006 CIRAD, INRIA

  This script is use to generate source distribution of OpenAlea
"""


from distutils.core import setup

description= "OpenAlea namespace and base configuration"
author= "OpenAlea developpers team"
url= "http://openalea.gforge.inria.fr"
license="Cecill-C"

setup(
    name= "OpenAlea",
    version= "0.1.0",
    description= description,
    author=author,
    url=url,
    license=license,

    scripts=["install.py", "create_config.py", "setup.py"]

    )


