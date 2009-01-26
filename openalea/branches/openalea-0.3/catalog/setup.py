import os, sys
pj = os.path.join

from setuptools import setup


# Package name
name = 'OpenAlea.Catalog'
namespace = 'openalea'
pkg_name = 'openalea.catalog'
version = '0.3.2' 
description = 'OpenAlea Logical Component Catalog.' 
long_description = ''

author = 'OpenAlea consortium'
author_email = 'samuel.dufour@sophia.inria.fr, christophe.pradal@cirad.fr'

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
    package_dir={pkg_name : pj('src', 'catalog')},

    # Dependencies
    setup_requires = ['openalea.deploy'],
    install_requires = ['openalea.core'],
    dependency_links = ['http://openalea.gforge.inria.fr/pi'],
                     
    )


