"""setup file for stdlib package"""
import os
from setuptools import setup, find_packages

__license__ = 'Cecill-C' 
__revision__ = "$Id$"

pj = os.path.join

name = 'OpenAlea.StdLib'
version = '0.7.0'
description = 'OpenAlea standard logical component library.' 
long_description = ''
author = 'OpenAlea consortium'
author_email = 'samuel.dufour@sophia.inria.fr, christophe.pradal@cirad.fr'
url = 'http://openalea.gforge.inria.fr'

setup(
    name=name,
    version=version,
    description=description, 
    long_description = '',
    author = author,
    author_email = author_email,
    url = url,
    license = license,

    create_namespaces=False,
    zip_safe=False,

    packages=find_packages('src'),

    package_dir={"":"src" },

    # Add package platform libraries if any
    include_package_data=True,
    package_data = {'' : ['*.csv'],},

    # Dependencies
    setup_requires = ['openalea.deploy'],
    install_requires = ['openalea.core'],
    dependency_links = ['http://openalea.gforge.inria.fr/pi'],

    # entry_points
    entry_points = {
        "wralea": ['openalea.color = openalea.color', 
                   'openalea.csv = openalea.csv', 
                   'openalea.string = openalea.string',
                   'openalea.data = openalea.data',
                   'openalea.file = openalea.file',
                   'openalea.functional = openalea.functional',
                   'openalea.image = openalea.image',
                   'openalea.math = openalea.math', 
                   'openalea.model = openalea.model',
                   'openalea.pickling = openalea.pickling', 
                   'openalea.plotools = openalea.plotools',
                   'openalea.python = openalea.python',
                   'openalea.spatial = openalea.spatial',
                   'openalea.stand = openalea.stand',
                   'openalea.stat = openalea.stat',
                   'openalea.system = openalea.system',
                   'openalea.tutorial = openalea.tutorial',

                   # Deprecated
                   'catalog.color = deprecated', 
                   'catalog.data = deprecated',
                   'catalog.csv = deprecated', 
                   'catalog.file = deprecated',
                   'catalog.functional = deprecated',
                   'catalog.math = deprecated', 
                   'catalog.model = deprecated',
                   'catalog.pickling = deprecated', 
                   'catalog.python = deprecated',
                   'catalog.string = deprecated',
              ],
        },
    
    pylint_packages = [ 'src' + os.sep + x.replace('.',os.sep) for x in find_packages('src')],

    )


