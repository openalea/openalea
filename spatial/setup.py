import os, sys
pj = os.path.join

from setuptools import setup


# Package name
name = 'OpenAlea.Spatial'
namespace = 'openalea'
pkg_name = 'openalea.spatial'
version = '0.2' 
description = 'OpenAlea module for spatial distributions.' 
long_description = ''

author = 'OpenAlea consortium'
author_email = 'david.da_silva@cirad.fr, frederic.boudon@cirad.fr'

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
    package_dir={pkg_name : pj('src', 'spatial')},

    # Dependencies
    setup_requires = ['openalea.deploy'],
    install_requires = ['openalea.core'],
    dependency_links = ['http://openalea.gforge.inria.fr/pi'],
                     
    )


