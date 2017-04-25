# -*- coding: utf-8 -*-
__revision__ = "$Id$"

import sys
from setuptools import setup, find_packages
from os.path import join as pj

from openalea.deploy.metainfo import read_metainfo

metadata = read_metainfo('metainfo.ini', verbose=True)
for key,value in metadata.iteritems():
    exec("%s = '%s'" % (key, value))

namespace = 'openalea'
pkg_root_dir = 'src'
pkgs = [ pkg for pkg in find_packages(pkg_root_dir) if namespace not in pkg]
top_pkgs = [pkg for pkg in pkgs if  len(pkg.split('.')) < 2]
packages = [ namespace + "." + pkg for pkg in pkgs]
package_dir = dict( [('',pkg_root_dir)] + [(namespace + "." + pkg, pkg_root_dir + "/" + pkg) for pkg in top_pkgs] )

setup(
    name=name,
    version=version,
    description=description,
    long_description=long_description,
    author=authors,
    author_email=authors_email,
    url=url,
    license=license,
    keywords='visual programming',

    # Packages
    py_modules = ['visualea_postinstall'],
    namespace_packages = [namespace],
    create_namespaces = True,

    packages = packages,
    package_dir = package_dir,
    package_data = {'openalea.visualea.resources' : ['*.ui', '*.png'],},
    include_package_data = True,
    zip_safe = False,

    # Scripts
    entry_points = { 'gui_scripts': [
                           'visualea = openalea.visualea.visualea_script:start_gui',
                           'aleashell = openalea.visualea.shell:main',],},

    postinstall_scripts = ['visualea_postinstall'],
    share_dirs = { 'share' : 'share' },

    # Dependencies
    setup_requires = ['openalea.deploy'],
    dependency_links = ['http://openalea.gforge.inria.fr/pi'],

    )
