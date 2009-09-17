# -*- coding: iso-8859-15 -*-

# Header
import os, sys
pj= os.path.join

from setuptools import setup

# Package name
name= 'qhull'
version= '2003.1'


# Description of the package

# Short description
description= 'qhull binary and development package'

license= 'QHull  License' 

# Main setup
setup(
    # Meta data
    name=name,
    version=version,
    description=description,
    license=license,

    include_package_data = True, 
    lib_dirs = { 'lib' : 'lib' },
    inc_dirs = { 'include' : 'include' },
    bin_dirs = { 'bin' : 'bin' },

    packages = ['man', 'share'],
    share_dirs = { 'man' : 'man', 'share':'share' },

    zip_safe = False,
    setup_requires = ['openalea.deploy'],
    dependency_links = ['http://openalea.gforge.inria.fr/pi'],
 
    )


