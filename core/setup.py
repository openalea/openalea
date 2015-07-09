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

    packages=[
        'openalea.core',
        'openalea.core.algo',
        'openalea.core.control',
        'openalea.core.graph',
        'openalea.core.graph.interface',
        'openalea.core.interpreter',
        'openalea.core.plugin',
        'openalea.core.project',
        'openalea.core.service',
        'openalea.core.system',
    ],

    package_dir={
        '': 'src',
        'openalea.core': pj('src', 'core'),
        'openalea.core.algo': pj('src', 'core', 'algo'),
        'openalea.core.control': pj('src', 'core', 'control'),
        'openalea.core.graph': pj('src', 'core', 'graph'),
        'openalea.core.graph.interface': pj('src', 'core', 'graph', 'interface'),
        'openalea.core.interpreter': pj('src', 'core', 'interpreter'),
        'openalea.core.plugin': pj('src', 'core', 'plugin'),
        'openalea.core.project': pj('src', 'core', 'project'),
        'openalea.core.service': pj('src', 'core', 'service'),
        'openalea.core.system': pj('src', 'core', 'system'),
    },

    # Dependencies
    setup_requires=['openalea.deploy'],
    install_requires=[],
    dependency_links=['http://openalea.gforge.inria.fr/pi'],

    # entry_points
    entry_points={
        "wralea": ["openalea.flow control = openalea.core.system", ],
        "console_scripts": ["alea = openalea.core.alea:main"],

        'openalea.core': [
            'OpenAleaBuiltin = openalea.core.plugin.builtin',
        ],
    },



)
