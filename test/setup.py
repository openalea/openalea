# -*- coding: iso-8859-15 -*-

# Header

#Check dependencies
import sys

try:
	from openalea import config
except ImportError:
	print """"
ImportError : openalea.config not found. 
Please install openalea package before.	
http://openalea.gforge.inria.fr
"""
	sys.exit()

try:
	from openalea.distx import setup
except ImportError:
	print """"
ImportError : openalea.distx package not found.
Please install openalea.distx package before
http://openalea.gforge.inria.fr
"""
        sys.exit()

from os.path import join as pj


# Package name
name= 'distx_tester'

#openalea namespace
namespace=config.namespace 

# Package version policy
# major.minor.patch
# alpha: patch + 'a'+ 'number'
# beta: patch= patch + 'b' + 'number'
major= '0'
minor= '0'
patch= '1a1'
version= '%s.%s.%s' % (major, minor, patch)

# Description of the package 
description= 'DistX test package.' #short description
long_description= 'DistX test package'

# Author
author= 'Samuel Dufour-Kowalski'
author_email= 'samuel.dufour@sophia.inria.fr'

# URL
url= 'http://gforge.inria.fr/projects/openalea/'

# License: License for the template package.
# Please, choose an OpenSource license for distribution of your package.
license= 'Cecill-C' #LGPL compatible INRIA licence

# For other meta-information, please read the Python distutils documentation.

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
    
    #Define where to execute scons
    #scons is responsible to put compiled library in the write place ( lib/, package/, etc...)
    scons_dir = ['.'],
    #scons parameters  
    scons_parameters = ['lib_dir=lib'],
      
    #pure python  packages
    packages= [namespace+'.'+name],
    #python packages directory
    package_dir= {namespace+'.'+name : pj('src',name)},

      
    #add package platform libraries if any
    package_data= { namespace+'.'+name : ['*.so', '*.dll', '*.pyd']},
                     

    #copy shared data in default OpenAlea directory
    #map of 'destination subdirectory' : 'source subdirectory'
    external_data={pj(config.prefix_dir, 'external', name) : 'external', },
    #external_data={pj('external', name) : 'external', },

    #ONLY FOR WINDOWS 
    #Add to PATH environment variable for openalea lib
    add_env_path=[pj(config.prefix_dir,'lib')]
    
   
      )


    
