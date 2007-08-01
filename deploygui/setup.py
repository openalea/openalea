

from setuptools import setup, find_packages
from os.path import join as pj



setup(
    # Metadata for PyPi
    name = "OpenAlea.Deploy-Gui",
    version = "0.1",
    author = "Samuel Dufour-Kowalski",
    author_email = "samuel.dufour@sophia.inria.fr",
    description = "OpenAlea graphical installer",
    license = 'Cecill-C',
    keywords = ['Graphical installer'],
    url = 'openalea.gforge.inria.fr',

    namespace_packages = ["openalea"],
    
    packages = find_packages('src'),
    package_dir = { '' : 'src', }, 
    include_package_data = True,
    zip_safe = True,

    entry_points = {
              "gui_scripts": [
                 "alea_install_gui = openalea.deploygui.alea_install_gui:main", ],
              },

    # Dependencies
    install_requires = ['OpenAlea.Deploy'],
    dependency_links = ['http://gforge.inria.fr/frs/...?id=79'],
    
)
