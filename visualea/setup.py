

# Header

#Check dependencies

#####################
# Import dependencies

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


##############
# Setup script

# Package name
name= 'visualea'

#openalea namespace
namespace=config.namespace 

pkg_name= namespace + '.' + name

# Package version policy
version= '0.1.0' 

# Description of the package

# Short description
description= 'OpenAlea GUI.' 

long_description= ''

# Author
author= 'OpenAlea consortium'
author_email= 'samuel.dufour@sophia.inria.fr, christophe.pradal@cirad.fr'

# URL
url= 'http://openalea.gforge.inria.fr'

# LGPL compatible INRIA license
license= 'Cecill-C' 


# Main setup
setup(
    # Meta data
    name=name,
    version=version,
    description=description,
    long_description=long_description,
    author=author,
    author_email=author_email,
    url=url,
    license=license,
    

    # pure python  packages
    packages= [ pkg_name ],
    # python packages directory
    package_dir= { pkg_name : pj('src',name)},

    scripts=['scripts/visualea']
    
    )


