import os, sys
pj = os.path.join

from setuptools import setup


# Package name
name = 'openalea.stat'
namespace = 'openalea'
pkg_name = 'openalea.stat'
version = '0.1.0' 
description = 'OpenAlea common statistic functions.' 
long_description = ''

author = 'OpenAlea consortium'
author_email = 'florence.chaubert@cirad.fr, david.da_silva@cirad.fr'

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
    package_dir={pkg_name : pj('src', 'stat')},

    # Dependencies
    setup_requires = ['openalea.deploy'],
    install_requires = ['openalea.core', 'openalea.plotools'],
    dependency_links = ['http://openalea.gforge.inria.fr/pi'],

    # entry_points
    entry_points = {
        "wralea": ["stat = openalea.stat",]
        },

                     
    )


