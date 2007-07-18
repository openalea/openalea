from ez_setup import use_setuptools
use_setuptools()


from setuptools import setup, find_packages
from os.path import join as pj


setup(
    # Metadata for PyPi
    name = "OpenAlea.Deploy",
    version = "0.1",
    author = "Samuel Dufour-Kowalski",
    author_email = "samuel.dufour@sophia.inria.fr",
    description = "Setuptools extension for OpenAlea",
    license = 'Cecill-C',
    keywords = ['setuptools', 'shared lib'],
    url = 'openalea.gforge.inria.fr',

    namespace_packages = ["openalea"],
    
    packages = find_packages('src'),
    package_dir = { '' : 'src', }, 
    include_package_data = True,
    zip_safe = True,

    entry_points = {
              "distutils.setup_keywords": [
                 "lib_dirs = openalea.deploy.command:validate_shared_dirs",
                 "inc_dirs = openalea.deploy.command:validate_shared_dirs",
                 "scons_scripts = openalea.deploy.command:validate_scons_scripts",
                 "scons_parameters = setuptools.dist:assert_string_list",
                 "create_namespaces = openalea.deploy.command:validate_create_namespaces",
                 "postinstall_scripts = openalea.deploy.command:validate_postinstall_scripts",
                 ],
              
              "egg_info.writers": [
                 "lib_dirs.txt = openalea.deploy.command:write_keys_arg",
                 "inc_dirs.txt = openalea.deploy.command:write_keys_arg",
                 "postinstall_scripts.txt = setuptools.command.egg_info:write_arg",
                 ],

              "distutils.commands":[
                 "scons = openalea.deploy.command:scons",
                 "create_namespaces = openalea.deploy.command:create_namespaces",
                 "alea_install = openalea.deploy.command:alea_install",
                 ],
              
              "console_scripts": [
                 "alea_install = openalea.deploy.alea_install:main", ],
              },

     #install_requires = [],
    
)
