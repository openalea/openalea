"""
  OpenAlea.Config : Copyright 2006 CIRAD, INRIA
"""


# To generate the windows installer
#   python setup.py bdist_wininst --install-script=oac_postinstall.py


import sys
old_path=sys.path
sys.path=['.']
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

sys.path= old_path

from distutils.core import setup
import version

description= "OpenAlea namespace and configuration"
author= "OpenAlea developers team"
url= "http://openalea.gforge.inria.fr"
license="Cecill-C"

# Add postinstall script if generate windows installer
if('win' in sys.platform
         and len(sys.argv)>1
         and sys.argv[1]=='bdist_wininst'):
    scriptname = 'oac_postinstall.py'
    sys.argv.append('--install-script=%s'%(scriptname,))
    scripts=[scriptname]
else :
    scripts=[]

# Distutils Setup function
d = setup(
    name= "OpenAlea.Config",
    version= version.version,
    description= description,
    author=author,
    url=url,
    license=license,
    scripts=scripts,

    packages= [config.namespace],
    )


# Post installtion
if('install' in d.commands):

    import oac_postinstall
    oac_postinstall.main()

