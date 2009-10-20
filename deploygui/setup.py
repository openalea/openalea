from setuptools import setup, find_packages
from os.path import join as pj
    

version = "0.7.0"
name = "OpenAlea.DeployGui"
author = "Samuel Dufour-Kowalski"
author_email = "samuel.dufour@sophia.inria.fr"
description = "OpenAlea graphical installer"
license = 'Cecill-V2'
keywords = ['Graphical installer']
url = 'openalea.gforge.inria.fr'

setup(
    # Metadata for PyPi
    name = name,
    version = version,
    author = author,
    author_email = author_email,
    description = description,
    license = license,
    keywords = keywords,
    url = url,

    namespace_packages = ["openalea"],

    py_modules = ['deploygui_postinstall'],
    packages = ["openalea", "openalea.deploygui"],
    package_dir = { 'openalea' : 'src/openalea', 'openalea.deploygui': 'src/openalea/deploygui', '':'src'  }, 
    include_package_data = True,
    zip_safe = False,

    share_dirs = { 'share' : 'share'},
    entry_points = {
              "gui_scripts": [
                 "alea_install_gui = openalea.deploygui.alea_install_gui:main", ],
              },
    
    postinstall_scripts = ['deploygui_postinstall'],
    # Dependencies
    install_requires = ['OpenAlea.Deploy>=0.4.13'],
    dependency_links = ['http://gforge.inria.fr/frs/...?id=79'],

)
