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
    

    packages= [ 'openalea.core', 'openalea.graph', 'openalea.graph.interface' ],
    package_dir= { 'openalea.core' : pj('src',name),
                   'openalea.graph' : pj('src','graph'),
                   'openalea.graph.interface' : pj('src','graph','interface') 
                  },

    )


