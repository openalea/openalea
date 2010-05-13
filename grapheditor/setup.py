# -*- coding: utf-8 -*-
__revision__ = "$Id$"

import sys
import os

from setuptools import setup, find_packages

from openalea.deploy.metainfo import read_metainfo

metadata = read_metainfo('metainfo.ini', verbose=True)
for key,value in metadata.iteritems():
    exec("%s = '%s'" % (key, value))



# Packages list, namespace and root directory of packages

# (this will determine the archive content and the names of your modules)
# (with the loop used bellow,all packages,ie all directories with a __init__.py, under pkg_root_dir will be recursively detected and named according to the directory hirearchy)
# (namespace allows you to choose a prefix for package names (eg alinea, openalea,...). 
# (This functionality needs deploy to be installed)
# (if you want more control on what to put in your distribution, you can manually edit the' packages' list 
# (the 'package_dir' dictionary must content the pkg_rootdir and all top-level pakages under it)

pkg_root_dir = 'src'
pkgs = [ pkg for pkg in find_packages(pkg_root_dir) if namespace not in pkg]
top_pkgs = [pkg for pkg in pkgs if  len(pkg.split('.')) < 2]
packages = [ namespace + "." + pkg for pkg in pkgs]
package_dir = dict( [('',pkg_root_dir)] + [(namespace + "." + pkg, pkg_root_dir + "/" + pkg) for pkg in top_pkgs] )

# List of top level wralea packages (directories with __wralea__.py) 
# (to be kept only if you have visual components)
#wralea_entry_points = ['%s = %s'%(pkg,namespace + '.' + pkg) for pkg in top_pkgs]

# dependencies to other eggs
# (This is used by deploy to automatically downloads eggs during the installation of your package)
# (allows 'one click' installation for windows user)
# (linux users generally want to void this behaviour and will use the dependance list of your documentation)
# (dependance to deploy is mandatory for runing this script)
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


    # Eventually include data in your package
    # (flowing is to include all versioned files other than .py)
    include_package_data = True,
    # (you can provide an exclusion dictionary named exclude_package_data to remove parasites).
    # alternatively to global inclusion, list the file to include   
    #package_data = {'' : ['*.pyd', '*.so'],},

    # postinstall_scripts = ['',],

    # Declare scripts and wralea as entry_points (extensions) of your package 
    entry_points = { 
		    #'console_scripts': [
                     #       'fake_script = openalea.fakepackage.amodule:console_script', ],
                     # 'gui_scripts': [
                      #      'fake_gui = openalea.fakepackage.amodule:gui_script',],
		#	'wralea': wralea_entry_points
		},
    )


