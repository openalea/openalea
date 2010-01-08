# -*- coding: iso-8859-15 -*-

# Header
import os, sys
pj= os.path.join

from setuptools import setup

#Check OS
"""
if not sys.platform.startswith('win'):
    print 'This package contain only Boost binary for MS Windows'
    print 'Please use your system installer to install Boost library'
    exit(1);
"""

# Package name
name= 'BoostPython'
version= '1.41'


# Description of the package

# Short description
description= 'Boost.Python binary and header for Ubuntu 9.10' 


license= 'Boost Software License V 1.0' 


# For other meta-information, please read the Python distutils documentation.

# Main setup
setup(
    # Meta data
    name=name,
    version=version,
    description=description,
    license=license,

    lib_dirs = { 'lib' : 'lib' },
    inc_dirs = { 'include' : 'include' },

    zip_safe = False,
    setup_requires = ['openalea.deploy'],
    dependency_links = ['http://openalea.gforge.inria.fr/pi'],
 
    )


