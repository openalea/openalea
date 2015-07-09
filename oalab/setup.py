# -*- coding: utf-8 -*-
__revision__ = "$Id$"

import sys
import os

from setuptools import setup, find_packages
from openalea.deploy.metainfo import read_metainfo

# Reads the metainfo file
metadata = read_metainfo('metainfo.ini', verbose=True)
for key, value in metadata.iteritems():
    exec("%s = '%s'" % (key, value))

# The metainfo files must contains
# version, release, project, name, namespace, pkg_name,
# description, long_description,
# authors, authors_email, url and license
# * version is 1.0.0 and release 1.0
# * project must be in [openalea, vplants, alinea]
# * name is the full name (e.g., OpenAlea.OALab) whereas pkg_name is only 'oalab'

# name will determine the name of the egg, as well as the name of
# the pakage directory under Python/lib/site-packages). It is also
# the one to use in setup script of other packages to declare a dependency to this package)
# (The version number is used by deploy to detect UPDATES)


# Packages list, namespace and root directory of packages

pkg_root_dir = 'src'
pkgs = [pkg for pkg in find_packages(pkg_root_dir)]
top_pkgs = [pkg for pkg in pkgs if len(pkg.split('.')) < 2]
packages = pkgs
package_dir = dict([('', pkg_root_dir)] + [(namespace + "." + pkg, pkg_root_dir + "/" + pkg) for pkg in top_pkgs])


# List of top level wralea packages (directories with __wralea__.py)
# wralea_entry_points = ['%s = %s'%(pkg,namespace + '.' + pkg) for pkg in top_pkgs]

# dependencies to other eggs
setup_requires = ['openalea.deploy']

# TODO: remove pygments 1.6 constraints when https://github.com/ipython/ipython/issues/6877 is fixed
install_requires = ['pygments==1.6']

# web sites where to find eggs
dependency_links = ['http://openalea.gforge.inria.fr/pi']
has_project = bool('openalea')
setup(
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
    packages=packages,
    package_dir=package_dir,

    # Namespace packages creation by deploy
    py_modules=['oalab_postinstall'],
    # namespace_packages = [namespace],
    # create_namespaces = False,
    zip_safe=False,

    # Dependencies
    setup_requires=setup_requires,
    install_requires=install_requires,
    dependency_links=dependency_links,


    # Eventually include data in your package
    # (flowing is to include all versioned files other than .py)
    include_package_data=True,
    # (you can provide an exclusion dictionary named exclude_package_data to remove parasites).
    # alternatively to global inclusion, list the file to include
    # package_data = {'' : ['*.pyd', '*.so'],},

    postinstall_scripts=['oalab_postinstall'],
    share_dirs={'share': 'share'},

    # Declare src and wralea as entry_points (extensions) of your package
    entry_points={

        'gui_scripts': [
            'oalab = openalea.oalab.main:main',
        ],


        'oalab.applet': [
            'OpenAleaLabApplet = openalea.oalab.plugin.builtin.applet',
        ],

        'oalab.plugin': [
            'PluginOpenAleaLab = openalea.oalab.plugin.builtin.oalab',
            'PluginVisualeaWidgetSelectors = openalea.oalab.plugin.builtin.oalab.visualea_control:PluginVisualeaWidgetSelectors',
        ],

        'oalab.lab': [
            'OpenAleaLabs = openalea.oalab.plugin.builtin.lab',
        ],

        'oalab.interface': [
            'OpenAleaLabInterfacePlugin = openalea.oalab.plugin.builtin.interface',
        ],

        'openalea.core': [
            'OpenAleaLabOpenAleaCorePlugin = openalea.oalab.plugin.builtin.core',
        ],

        # 'console_scripts': [
        #       'fake_script = openalea.fakepackage.amodule:console_script', ],
        # 'gui_scripts': [
        #      'fake_gui = openalea.fakepackage.amodule:gui_script',],
        'wralea': [
            'oalab = openalea.oalab_wralea',
        ],

        'plugin': [
            'oalab = openalea.oalab_wralea',
        ]
    },
)
