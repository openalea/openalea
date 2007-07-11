from setuptools import setup, find_packages

from os.path import join as pj


build_prefix = 'build-scons'

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

    # namespace
    # ! warning : Ensure you have the following code in the openalea.__init__.py
    # try:
    #     import pkg_resources
    #     pkg_resources.declare_namespace(__name__)
    # except ImportError:
    #     import pkgutil
    #     __path__ = pkgutil.extend_path(__path__, __name__)


    namespace_packages = ["openalea"],
    
    packages = ['openalea.fakepackage', 'lib', 'test', 'include.fakepackage', 'openalea'],
    package_dir = { 'openalea.fakepackage':  pj('src','fakepackage'),
                    'lib' : pj(build_prefix,'lib'),
                    'test' : pj(build_prefix,'lib'),
		    'include.fakepackage' : pj(build_prefix,'include', 'fakepackage'),
		    }, 
		    
    package_data = { '' : ['*'],},
    
    include_package_data = True,
    zip_safe= False,

    # Specific options of openalea.deploy
    create_namespace = True,

    shared_lib = ['lib', 'test'],
    shared_include = ['include'],
    shared_data = [],

    # Scripts
    entry_points = { 'console_scripts': [
                           'fake_script = openalea.fakepackage.amodule:console_script', ],
                     'gui_scripts': [
                           'fake_gui = openalea.fakepackage.amodule:gui_script',]},

     # Dependencies
     setup_requires = ['OpenAlea.Deploy'],
     #install_requires = [],
    
)
