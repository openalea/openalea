import os, sys
pj = os.path.join

from setuptools import setup


# Package name
name = 'OpenAlea.Stand'
namespace = 'openalea'
pkg_name = 'openalea.stand'
version = '0.1.0' 
description = 'OpenAlea module for stand modelling.' 
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

    
    packages=[pkg_name,
              pkg_name + '.forestry_stand',
              ],

    package_dir={pkg_name : pj('src', 'stand'), 
                 pkg_name + '.forestry_stand' : pj('src', 'stand', 'forestry_stand') ,
                 '' : 'src', },

    package_data={ '' : ['*.*']},

    # Dependencies
    setup_requires = ['openalea.deploy'],
    install_requires = ['openalea.core'],
    dependency_links = ['http://openalea.gforge.inria.fr/pi'],

    # entry_points
    entry_points = {
        "wralea": ["stand = openalea.stand",
                   "demo = openalea.stand.forestry_stand",
                   ]
        },

                     
    )


