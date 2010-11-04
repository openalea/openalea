# -*- coding: utf-8 -*-
__revision__ = "$Id$"

import os, sys
pj = os.path.join

from setuptools import setup, find_packages

from openalea.deploy.metainfo import read_metainfo
metadata = read_metainfo('metainfo.ini', verbose=True)
for key,value in metadata.iteritems():
    exec("%s = '%s'" % (key, value))


platform = sys.platform
if platform.startswith('win'):
    external_dependencies = ['matplotlib>=0.99.1',
                             'scipy>=0.7.1',
                             'numpy>=1.4.0']
else:
    external_dependencies = ['matplotlib',
                             'scipy',
                             'numpy']

#if platform != 'darwin':
#    external_dependencies.append('PIL<=1.1.6')

alea_dependencies = [
'openalea.core == 0.9.0',
'openalea.deploy == 0.9.0',
'openalea.deploygui == 0.9.0',
'openalea.grapheditor == 0.9.0',
'openalea.misc == 0.9.0',
'openalea.visualea == 0.9.0',
'openalea.stdlib == 0.9.0',
'openalea.sconsx == 0.9.0',
'openalea.scheduler == 0.9.0',
'openalea.numpy == 0.9.0',
'openalea.pylab == 0.9.0',
'openalea.image == 0.9.0',
'openalea.pkgbuilder == 0.9.0',
#'openalea.container >=2.0.1.dev', part of vplants 
#'openalea.mtg >=0.7.0.dev', part of vplants
]

install_requires = alea_dependencies

# Add dependencies on Windows and Mac OS X platforms
if 'win' in platform:
    install_requires += external_dependencies 

build_prefix = "build-scons"

setup(
    name = name,
    version = version,
    description = description,
    long_description = long_description,
    author = authors,
    author_email = authors_email,
    url = url,
    license = license,

    namespace_packages = ['openalea'],
    create_namespaces=False,
    zip_safe=False,

    packages=find_packages('src'),

    package_dir={"":"src" },

    #scons_scripts=['SConstruct'],

    # Add package platform libraries if any
    include_package_data=True,
    package_data = {'' : ['*.png']},
    # Dependencies
    setup_requires = ['openalea.deploy'],
    install_requires = install_requires,
    dependency_links = ['http://openalea.gforge.inria.fr/pi'],

    # entry_points
    entry_points = {"wralea": ['openalea = openalea']},
    )


