# -*- coding: utf-8 -*-
__revision__ = "$Id: setup.py 2249 2010-02-08 17:27:37Z cokelaer $"

import sys
import os

from setuptools import setup, find_packages
from openalea.deploy.metainfo import read_metainfo

# Reads the metainfo file
metadata = read_metainfo('metainfo.ini', verbose=True)
for key,value in metadata.iteritems():
    exec("%s = '%s'" % (key, value))


pkg_root_dir = 'src'
pkgs = [ pkg for pkg in find_packages(pkg_root_dir)]
top_pkgs = [pkg for pkg in pkgs if  len(pkg.split('.')) < 2]
packages = pkgs
package_dir = dict( [('',pkg_root_dir)] + [(namespace + "." + pkg, pkg_root_dir + "/" + pkg) for pkg in top_pkgs] )


# Define global variables 
has_scons = False

build_prefix = None
scons_scripts=None
lib_dirs = None
inc_dirs = None
bin_dirs = None


setup_requires = ['openalea.deploy']
if("win32" in sys.platform):
    install_requires = ['openalea.numpy']
else:
    install_requires = []
    
# web sites where to find eggs
dependency_links = ['http://openalea.gforge.inria.fr/pi']

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
    keywords = '',	
    
    # package installation
    packages= packages,	
    package_dir= package_dir,

    # Namespace packages creation by deploy
    namespace_packages = [namespace],
    #create_namespaces = True,
    zip_safe= False,
    
    # Dependencies
    setup_requires = setup_requires,
    install_requires = install_requires,
    dependency_links = dependency_links,


    lib_dirs = lib_dirs,
    inc_dirs = inc_dirs,
    bin_dirs = bin_dirs,
    
    include_package_data = True,
    
    entry_points = {
            "wralea": [ "pylab = openalea.pylab_main_wralea",
                        "pylab.demo = openalea.pylab_demo_wralea",
                        "pylab.plotting = openalea.pylab_plotting_wralea",
                        "pylab.datasets = openalea.pylab_datasets_wralea",
                        "pylab.decorators = openalea.pylab_decorators_wralea",
                        "pylab.test = openalea.pylab_test_wralea",
                        "pylab.patches = openalea.pylab_patches_wralea",
                        "pylab.mplot3d = openalea.pylab_3d_wralea",
            ]
            },

    )


