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

from setuptools import setup, find_packages

pj = os.path.join

from openalea.deploy.metainfo import read_metainfo

metadata = read_metainfo('metainfo.ini', verbose=True)

for key, value in metadata.iteritems():
    exec("%s = '%s'" % (key, value))

namespace = 'openalea'
pkg_root_dir = 'src'
pkgs = [ pkg for pkg in find_packages(pkg_root_dir) if namespace not in pkg]
top_pkgs = [pkg for pkg in pkgs if  len(pkg.split('.')) < 2]
packages = [ namespace + "." + pkg for pkg in pkgs]
package_dir = dict([('',pkg_root_dir)] + [(namespace + "." + pkg, pkg_root_dir + "/" + pkg) for pkg in top_pkgs])

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

    packages= packages,
    package_dir= package_dir,

    setup_requires=['openalea.deploy'],

    install_requires=[],

    dependency_links=['http://openalea.gforge.inria.fr/pi'])

#
# setup.py ends here
