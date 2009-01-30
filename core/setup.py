#Check dependencies

import os, sys
pj = os.path.join

name = 'OpenAlea.Core'
namespace = 'openalea'

execfile("src/core/version.py")

description = 'OpenAlea Component platform core.' 
long_description = ''
author = 'OpenAlea consortium'
author_email = 'samuel.dufour@sophia.inria.fr, christophe.pradal@cirad.fr'
url = 'http://openalea.gforge.inria.fr'
__license__= 'Cecill-C' 
__revision__ = "$Id$"

from setuptools import setup

setup(
    name=name,
    version=version,
    description=description,
    long_description=long_description,
    author=author,
    author_email=author_email,
    url=url,
    license=license,

    namespace_packages = ['openalea'],
    create_namespaces = True,
    zip_safe = False,
    include_package_data = True,

    packages = [ 'openalea.core', 'openalea.core.graph', 'openalea.core.algo',
                'openalea.core.graph.interface' ],
    
    package_dir = { 'openalea.core' : pj('src','core'),
                    'openalea.core.system' : pj('src','core', 'system'),
                    'openalea.core.algo' : pj('src','core', 'algo'),
                    'openalea.core.graph' : pj('src','core', 'graph'),
                    'openalea.core.graph.interface' : pj('src', 'core', 'graph','interface'),
                    '':'src',
                  },

    # Dependencies
    setup_requires = ['openalea.deploy'],
    install_requires = [],
    dependency_links = ['http://openalea.gforge.inria.fr/pi'],

    # entry_points
    entry_points = {
              "wralea": ["openalea.flow control = openalea.core.system",],
              "console_scripts": ["alea = openalea.core.alea:main"],
              },


    )


