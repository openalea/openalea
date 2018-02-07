# -*- coding: utf-8 -*-
__revision__ = "$Id$"

import sys
import os

from setuptools import setup, find_packages

from openalea.deploy.metainfo import read_metainfo

metadata = read_metainfo('metainfo.ini', verbose=True)
for key,value in metadata.iteritems():
    exec("%s = '%s'" % (key, value))

namespace = 'openalea'
packages=find_packages('src')
package_dir={'': 'src'}

setup_requires = ['openalea.deploy']
install_requires = []
# web sites where to find eggs
dependency_links = ['http://openalea.gforge.inria.fr/pi']

# setup function call
#
setup(
    # Meta data (no edition needed if you correctly defined the variables above)
    name=name,
    version=version,
    description=description,
    long_description=long_description,
    author=authors,
    author_email=authors_email,
    url=url,
    license=license,
    keywords='',

    # package installation
    packages= packages,
    package_dir= package_dir,

    # Namespace packages creation by deploy
    namespace_packages=[namespace],
    create_namespaces=True,

    zip_safe=False,

    # Dependencies
    setup_requires=setup_requires,
    install_requires=install_requires,
    dependency_links=dependency_links,

    include_package_data=True,
)
