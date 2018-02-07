# -*- coding: utf-8 -*-

"""setup file for core package"""
__revision__ = "$Id$"

import os
from setuptools import setup
pj = os.path.join


# to get the version
# execfile("src/core/version.py")

from openalea.deploy.metainfo import read_metainfo
metadata = read_metainfo('metainfo.ini', verbose=True)
for key, value in metadata.iteritems():
    exec("%s = '%s'" % (key, value))


setup(
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

    packages=find_packages('src'),
    package_dir={'': 'src'},

    # Dependencies
    setup_requires=['openalea.deploy'],
    install_requires=[],
    dependency_links=['http://openalea.gforge.inria.fr/pi'],

    share_dirs={'share': 'share'},

    # entry_points
    entry_points={
        "wralea": ["openalea.flow control = openalea.core.system", ],
        "console_scripts": ["alea = openalea.core.alea:main"],

        'openalea.core': [
            'openalea.core/openalea = openalea.core.plugin.builtin',
        ],
    },



)
