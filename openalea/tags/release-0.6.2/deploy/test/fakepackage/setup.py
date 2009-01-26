import sys
import os

from setuptools import setup, find_packages
from os.path import join as pj




build_prefix = "build-scons"

# Setup function
setup(
    # Metadata for PyPi
    name = "OpenAlea.FakePackage",
    version = "0.1",
    author = "Me",
    author_email = "me@example.com",
    description = "This is an Example Package",
    license = '',
    keywords = '',
    url = '',

    # Scons
    scons_scripts = ["SConstruct"],
    scons_parameters = ["build_prefix=%s"%(build_prefix)],

    # Packages
    namespace_packages = ["openalea"],
    create_namespaces = True,
    packages = ['openalea.fakepackage', ],
    
    package_dir = { 'openalea.fakepackage':  pj('src','fakepackage'), }, 
		    
    #package_data = {'' : ['*'],},
    include_package_data = True,
    zip_safe= False,

    # Specific options of openalea.deploy
    lib_dirs = {'lib': pj(build_prefix, 'lib') },
    inc_dirs = {'include': pj(build_prefix, 'include') } ,
    share_dirs = { 'share' : 'examples'},
    postinstall_scripts = ['openalea.fakepackage.postinstall',],
    
    # Scripts
    entry_points = { 'console_scripts': [
                           'fake_script = openalea.fakepackage.amodule:console_script', ],
                     'gui_scripts': [
                           'fake_gui = openalea.fakepackage.amodule:gui_script',]},

    # Dependencies
    setup_requires = ['openalea.deploy'],
    dependency_links = ['http://openalea.gforge.inria.fr/pi'],
    #install_requires = [],
    
)
