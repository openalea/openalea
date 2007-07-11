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
                 "shared_lib = setuptools.dist:assert_string_list",
                 "shared_include = setuptools.dist:assert_string_list",
                 "shared_data = setuptools.dist:assert_string_list",
                 ],
              
              "egg_info.writers": [
                 "shared_lib.txt = setuptools.command.egg_info:write_arg",
                 "shared_include.txt = setuptools.command.egg_info:write_arg",
                 "shared_data.txt = setuptools.command.egg_info:write_arg",

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
