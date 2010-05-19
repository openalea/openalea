# -*- coding: utf-8 -*-
__revision__ = "$Id: setup.py 2249 2010-02-08 17:27:37Z cokelaer $"


import sys
import os

from setuptools import setup, find_packages

# Reads the metainfo file
from openalea.deploy.metainfo import read_metainfo
metadata = read_metainfo('metainfo.ini', verbose=True)
for key,value in metadata.iteritems():
    exec("%s = '%s'" % (key, value))


pkgs = [ pkg for pkg in find_packages('src') if namespace not in pkg]
top_pkgs = [pkg for pkg in pkgs if  len(pkg.split('.')) < 2]
packages = [ namespace + "." + pkg for pkg in pkgs]
package_dir = dict( [('','src')] + [(namespace + "." + pkg,  "src/" + pkg) for pkg in top_pkgs] )

setup_requires = ['openalea.deploy']
# web sites where to find eggs
dependency_links = ['http://openalea.gforge.inria.fr/pi']


# scons build-prefix 
#(to be kept only if you contruct C/C++ binaries)

#build_prefix = "build-scons"
install_requires = []


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
    keywords = '',	
    # package installation
    packages= packages,	
    package_dir= package_dir,
    # Namespace packages creation by deploy
    namespace_packages = [namespace],
    create_namespaces = True,
    # tell setup not  tocreate a zip file but install the egg as a directory (recomended to be set to False)
    zip_safe= False,
    # Dependencies
    setup_requires = setup_requires,
    install_requires = install_requires,
    dependency_links = dependency_links,


    #lib_dirs = {'lib' : build_prefix+'/lib' },
    #inc_dirs = { 'include' : build_prefix+'/include' },

    include_package_data = True,
    entry_points = {
            "wralea": [ "openalea.pylab = pylab_main_wralea",
                        "openalea.pylab.demo = pylab_demo_wralea",
                        "openalea.pylab.nodes = pylab_nodes_wralea",
                        "openalea.pylab.text = pylab_text_wralea",
                        "openalea.pylab.test = pylab_test_wralea",
                        "openalea.pylab.patches = pylab_patches_wralea",
                        "openalea.pylab.mplot3d = pylab_3d_wralea",
            ]
            },


    )


