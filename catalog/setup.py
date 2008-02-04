import os, sys
pj = os.path.join

from setuptools import setup


# Package name
name = 'OpenAlea.Catalog'
namespace = 'openalea'
pkg_name = 'openalea.catalog'
version = '0.4.0' 
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

    
    packages=['openalea.catalog', 
              'openalea.catalog.color', 'openalea.catalog.data',
              'openalea.catalog.csv', 'openalea.catalog.file',
              'openalea.catalog.functional',
              'openalea.catalog.math', 'openalea.catalog.model',
              'openalea.catalog.pickling', 'openalea.catalog.python',
              'openalea.catalog.string',
              ],

    package_dir={pkg_name : pj('src', 'catalog')},

    # Dependencies
    setup_requires = ['openalea.deploy'],
    install_requires = ['openalea.core'],
    dependency_links = ['http://openalea.gforge.inria.fr/pi'],

    # entry_points
    entry_points = {
        "wralea": ['catalog.color = openalea.catalog.color', 
                   'catalog.data = openalea.catalog.data',
                   'catalog.csv = openalea.catalog.csv', 
                   'catalog.file = openalea.catalog.file',
                   'catalog.functional = openalea.catalog.functional',
                   'catalog.math = openalea.catalog.math', 
                   'catalog.model = openalea.catalg.model',
                   'catalog.pickling = openalea.catalog.pickling', 
                   'catalog.python = openalea.catalog.python',
                   'catalog.string = openalea.catalog.string',
              ],

        },

                     
    )


