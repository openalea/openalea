# -*- coding: iso-8859-15 -*-


#Check dependencies
import sys
import distx

# Package name
name= 'distx'
namespace='openalea'

# Package version policy
# major.minor.patch
# alpha: patch + 'a'+ 'number'
# beta: patch= patch + 'b' + 'number'
major= '0'
minor= '1'
patch= '0'
version= '%s.%s.%s' % (major, minor, patch)

# Description of the package 
description= 'Distutils extension' #short description
long_description= 'distx add functionalities to distutils (scons call, external data)...'

# Author
author= 'Samuel Dufour-Kowalski'
author_email= 'samuel.dufour@sophia.inria.fr'

# URL
url= 'http://gforge.inria.fr'

# License: License for the template package.
# Please, choose an OpenSource license for distribution of your package.
license= 'Cecill-C' #LGPL compatible INRIA licence

# For other meta-information, please read the Python distutils documentation.
#from distutils.core import setup
from distx import setup

#MAIN SETUP
setup(

    #META DATA
    name=name,
    version=version,
    description=description,
    author=author,
    author_email=author_email,
    url=url,
    license=license,
    long_description=long_description,
    
    namespace= [namespace],

    #pure python  packages
    packages= [namespace+'.'+name],
    package_dir= {namespace+'.'+name : name},
    
   
)


    
