# Version: $Id$
#
#

# Commentary:
#
#

# Change Log:
#
#

# Code:

# -*- coding: utf-8 -*-

"""setup file for core package"""
__revision__ = "$Id$"

import os

from setuptools import setup

pj = os.path.join

from openalea.deploy.metainfo import read_metainfo

metadata = read_metainfo('metainfo.ini', verbose=True)

for key, value in metadata.iteritems():
    exec("%s = '%s'" % (key, value))

setup (
    name=name,
    version=version,
    description=description,
    long_description=long_description,
    author=authors,
    author_email=authors_email,
    url=url,
    license=license,

    namespace_packages=['openalea'],
    create_namespaces=True,
    zip_safe=False,
    include_package_data=True,

    packages=[
        'openalea.qt',
    ],

    package_dir={
        '': 'src',
        'openalea.qt': pj('src', 'core'),
    },

    setup_requires=['openalea.deploy'],

    install_requires=[],

    dependency_links=['http://openalea.gforge.inria.fr/pi'])

#
# setup.py ends here
