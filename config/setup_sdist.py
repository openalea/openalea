"""
  OpenAlea.Config : Copyright 2006 CIRAD, INRIA

  This script is use to generate source distribution of OpenAlea
"""


from distutils.core import setup

description= "OpenAlea namespace creation and configuration"
author= "OpenAlea developpers team"
url= "http://openalea.gforge.inria.fr"
license="Cecill-C"

setup(
    name= "OpenAlea.Config",
    version= "0.1.0",
    description= description,
    author=author,
    url=url,
    license=license,

    scripts=["install.py", "create_config.py", "setup.py"]

    )


