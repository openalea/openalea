import os, sys
pj = os.path.join

from setuptools import setup


# Package name
name = 'openalea.image'
namespace = 'openalea'
pkg_name = 'openalea.image'
version = '0.1.0' 
description = 'OpenAlea image handling.' 
long_description = \
"""
Set of functionality to work around images in openalea
this module is mainly based on PIL
"""

author = 'OpenAlea consortium'
author_email = 'david.da_silva@cirad.fr'

url = 'http://openalea.gforge.inria.fr'
license = 'Cecill-C' 

setup(
    name=name,
    version=version,
    description=description,
    long_description=long_description,
    author=author,
    author_email=author_email,
    url=url,
    license=license,

    namespace_packages=['openalea'],
    create_namespaces=True,
    zip_safe=False,

    
    packages=[pkg_name],
    package_dir={pkg_name : pj('src', 'image')},

    # entry_points
    entry_points = {
        "wralea": ["stat = openalea.image",]
        },


    # Dependencies
    setup_requires = ['openalea.deploy'],
    install_requires = ['openalea.core'],
    dependency_links = ['http://openalea.gforge.inria.fr/pi'],
                     
    )


