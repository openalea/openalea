# -*- coding: iso-8859-15 -*-


#Check dependencies
import sys
import distx

# Package name
name = 'distx'
namespace ='openalea'

version = '0.2.0'

description = 'Distutils extension' 
long_description = 'DistX add functionalities to distutils (scons call, external data, windows path)...'

author = 'Samuel Dufour-Kowalski'
author_email = 'samuel.dufour@sophia.inria.fr'
url = 'http://gforge.inria.fr'

license = 'Cecill-C' #LGPL compatible INRIA licence

from distx import setup

setup(
    name=name,
    version=version,
    description=description,
    author=author,
    author_email=author_email,
    url=url,
    license=license,
    long_description=long_description,
    
    namespace=[namespace],

    #pure python  packages
    packages=[namespace+'.'+name],
    package_dir={namespace+'.'+name : name},
)


    
