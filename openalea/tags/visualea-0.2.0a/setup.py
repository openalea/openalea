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


name= 'visualea'
namespace=config.namespace 
pkg_name= namespace + '.' + name

sys.path.append("src")
import visualea.metainfo as metainfo

version= metainfo.version

description= 'OpenAlea GUI.' 
long_description= ''

author= 'OpenAlea consortium'
author_email= 'samuel.dufour@sophia.inria.fr, christophe.pradal@cirad.fr'

url= metainfo.url
license= 'Cecill v2' 

if sys.platform == 'win32':
    script='scripts/visualea.py' 
else:
    script='scripts/visualea' 

setup(
    name=name,
    version=version,
    description=description,
    long_description=long_description,
    author=author,
    author_email=author_email,
    url=url,
    license=license,

    packages= [ pkg_name ],
    package_dir= { pkg_name : pj('src',name)},
    scripts=[script]
    
    )


