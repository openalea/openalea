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
packages=find_packages('src')
package_dir={'': 'src'}

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
    #install_requires = ['openalea.core', 'openalea.grapheditor'],

    )


