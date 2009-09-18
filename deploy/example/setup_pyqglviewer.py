# -*- coding: iso-8859-15 -*-

# Header
import os, sys
pj= os.path.join

from setuptools import setup

# Package name
name= 'PyQGLViewer'
version= '2.3.4'


# Description of the package

# Short description
description= 'PyQGLViewer 0.7 and libQGLViewer 2.3.4 '
long_description= 'This egg was created from the source file. libQGLViewer was patched with a patch that is provided in the wiki (search for egg and pyql).'

license= 'GPL' 

# Main setup
setup(
    # Meta data
    name=name,
    version=version,
    description=description,
    license=license,

    include_package_data = True, 
    packages = ['examples', 'src/sip/'],
    lib_dirs = { 'lib' : 'lib'  },
    inc_dirs = { 'include' : 'include' },

    zip_safe = False,
    setup_requires = ['openalea.deploy'],
    dependency_links = ['http://openalea.gforge.inria.fr/pi'],
 
    )

