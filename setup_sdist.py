"""
  OpenAlea.Config : Copyright 2006 CIRAD, INRIA
  
"""

#  This script is only used to generate source distribution of OpenAlea.Config
#  Use setup.py to generate bdist_wininst 


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

    scripts=["ChangeLog.txt",
             "install.py", "create_config.py", "setup.py", "oac_postinstall.py"]

    )


