# -*- coding: utf-8 -*-
__revision__ = "$Id: $"


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
# * name is the full name (e.g., OpenAlea.VPLTK) whereas pkg_name is only 'vpltk'

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

# Define global variables


# dependencies to other eggs
setup_requires = ['openalea.deploy']
install_requires = []

# web sites where to find eggs
dependency_links = ['http://openalea.gforge.inria.fr/pi']

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
    package_data={'openalea.vpltk.qt': ['*.ui'], },

    # postinstall_scripts = ['',],

    # Declare scripts and wralea as entry_points (extensions) of your package
    entry_points={
        'plugin': ['vpltksample = openalea.vpltk.sample'],

        #'wralea' : ['vpltk = openalea.vpltk_wralea' if has_project else 'vpltk = vpltk_wralea' ],
        #'console_scripts': [
        #       'fake_script = openalea.fakepackage.amodule:console_script', ],
        # 'gui_scripts': [
        #      'fake_gui = openalea.fakepackage.amodule:gui_script',],
        #	'wralea': wralea_entry_points
    },
)
