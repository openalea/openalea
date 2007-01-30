"""
  OpenAlea.Config : Copyright 2006 CIRAD, INRIA

  This script is use to generate source distribution of OpenAlea.Config
"""


from distutils.core import setup
import version

description= "OpenAlea namespace creation and configuration"
author= "OpenAlea developers team"
url= "http://openalea.gforge.inria.fr"
license="Cecill-C"



setup(
    name= "OpenAlea.Config",
    version= version.version,
    description= description,
    author=author,
    url=url,
    license=license,

    scripts=["install.py", "create_config.py", "setup.py", "finalize_setup.py"]

    )


