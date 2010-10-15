# -*- coding: iso-8859-15 -*-

# Header
import os, sys
from os import listdir
from os.path import exists
pj= os.path.join

from setuptools import setup


# Package name
name= 'Boost'
version= '1.44'

# Short description
description= 'Boost libs and headers.' 
license= 'Boost Software License V 1.0' 

#find boost include dir in cwd when boost is installed using --prefix
#into cwd. The include directory has a subdirectory named "boost-X_YY[_Z]"
cwd = os.getcwd()
includeDir = pj("include", "boost-"+version.replace(".", "_"))
if not exists(pj(cwd,includeDir)):
    secondTry = pj(cwd, "include")
    if exists(pj(secondTry, "boost")):
        includeDir = secondTry
    else:
        raise Exception("Include directory 'boost' not found in " + includeDir + " or " + secondTry + ".")
        sys.exit(-1)

# For other meta-information, please read the Python distutils documentation.

# Main setup
setup(
    # Meta data
    name=name,
    version=version,
    description=description,
    license=license,

    lib_dirs = { 'lib' : 'lib' },
    inc_dirs = { 'include' : includeDir },

    zip_safe = False,
    setup_requires = ['openalea.deploy'],
    dependency_links = ['http://openalea.gforge.inria.fr/pi'],
    )


