

from setuptools import setup, find_packages
from os.path import join as pj

setup(
    # Metadata for PyPi
    name = "OpenAlea.DeployGui",
    version = "0.3.2",
    author = "Samuel Dufour-Kowalski",
    author_email = "samuel.dufour@sophia.inria.fr",
    description = "OpenAlea graphical installer",
    license = 'Cecill-C',
    keywords = ['Graphical installer'],
    url = 'openalea.gforge.inria.fr',

    namespace_packages = ["openalea"],

    py_modules = ['deploygui_postinstall'],
    packages = ["openalea", "openalea.deploygui"],
    package_dir = { 'openalea' : 'src/openalea', 'openalea.deploygui': 'src/openalea/deploygui' }, 
    include_package_data = True,
    zip_safe = False,

    share_dirs = { 'share' : 'share'},
    entry_points = {
              "gui_scripts": [
                 "alea_install_gui = openalea.deploygui.alea_install_gui:main", ],
              },
    
    postinstall_scripts = ['deploygui_postinstall'],
    # Dependencies
    install_requires = ['OpenAlea.Deploy>=0.3.3'],
    dependency_links = ['http://gforge.inria.fr/frs/...?id=79'],
    
)
