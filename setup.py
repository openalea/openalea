#Check dependencies

import os, sys
pj= os.path.join

try:
    from openalea import config
except ImportError:
    print """
ImportError : openalea.config not found. 
Please install the openalea package before.	
See http://openalea.gforge.inria.fr
"""
    sys.exit()

from distutils.core import setup


name= 'core'
namespace=config.namespace 
pkg_name= namespace + '.' + name

import version as versionmodule
version = versionmodule.version

description= 'OpenAlea Component platform core.' 
long_description= ''

author= 'OpenAlea consortium'
author_email= 'samuel.dufour@sophia.inria.fr, christophe.pradal@cirad.fr'

url= 'http://openalea.gforge.inria.fr'
license= 'Cecill-C' 


setup(
    name=name,
    version=version,
    description=description,
    long_description=long_description,
    author=author,
    author_email=author_email,
    url=url,
    license=license,
    

    packages= [ pkg_name, 'graph' ],
    package_dir= { pkg_name : pj('src',name),
                   'graph' : pj('src','graph') 
                  },

    )


