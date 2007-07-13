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
                 "include_dirs = openalea.deploy.command:validate_shared_dirs",
                 "scons_scripts = openalea.deploy.command:validate_scons_scripts",
                 "scons_parameters = setuptools.dist:assert_string_list",
                 "create_namespaces = openalea.deploy.command:validate_create_namespaces",
                 ],
              
              "egg_info.writers": [
                 "lib_dirs.txt = openalea.deploy.command:write_keys_arg",
                 "include_dirs.txt = openalea.deploy.command:write_keys_arg",
                 ],

              "distutils.commands":[
                 "scons = openalea.deploy.command:scons",
                 "create_namespaces = openalea.deploy.command:create_namespaces",
                 ],  },
#     # Scripts
#     entry_points = { 'console_scripts': [
#                            'fake_script = openalea.fakepackage.amodule:console_script', ],
#                      'gui_scripts': [
#                            'fake_gui = openalea.fakepackage.amodule:gui_script',]},

#      # Dependencies
#      setup_requires = ['OpenAlea.Deploy'],
     #install_requires = [],
    
)
