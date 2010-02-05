# -*- coding: iso-8859-15 -*-

# Header
import os, sys
pj= os.path.join

from setuptools import setup, find_packages

#Check OS
"""
if not sys.platform.startswith('win'):
    print 'This package contain only Boost binary for MS Windows'
    print 'Please use your system installer to install Boost library'
    exit(1);
"""

# Package name
name= 'SCons'
version= '1.2.0.d20100117'


# Description of the package

# Short description
description= 'Scons revision 1.2.0.d20100117' 


license= 'Copyright (c) 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010 The SCons Foundation' 


# For other meta-information, please read the Python distutils documentation.
packages=[pkg for pkg in find_packages('engine')]
print packages

package_dir = dict([(pkg, 'engine/' + pkg.replace('.','/')) for pkg in packages])
print package_dir
# Main setup
setup(
    # Meta data
    name=name,
    version=version,
    description=description,
    license=license,

    packages=packages,

    package_dir=package_dir,

    bin_dirs = {'EGG-INFO/scripts': 'script'},

    zip_safe = False,
    setup_requires = ['openalea.deploy'],
    dependency_links = ['http://openalea.gforge.inria.fr/pi'],

    )
print package_dir

