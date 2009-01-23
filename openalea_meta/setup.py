import os, sys
pj = os.path.join

from setuptools import setup, find_packages

external_dependencies = [
'numpy>=1.0.4',
'scipy == 0.6',
'matplotlib<=0.91.4',
'PIL<=1.1.6',
'qt4>=4.4.3'
]

alea_dependencies = [
'openalea.deploy > 0.5',
'openalea.deploygui > 0.5',
'openalea.core > 0.5',
'openalea.visualea > 0.5',
'openalea.stdlib > 0.5',
'openalea.sconsx > 0.5',
]

install_requires = alea_dependencies
if sys.platform.startswith('win'):
    install_requires += external_dependencies 

setup(
    name = 'OpenAlea',
    version = '0.6.2' ,
    description = 'OpenAlea packages and all its dependencies.', 
    long_description = '',
    author = 'OpenAlea consortium',
    author_email = 'christophe dot pradal at cirad dot fr',
    url = 'http://openalea.gforge.inria.fr',
    license = 'Cecill-C',


    create_namespaces=False,
    zip_safe=False,

    packages=find_packages('src'),

    package_dir={"":"src" },

    # Add package platform libraries if any
    include_package_data=True,

    # Dependencies
    setup_requires = ['openalea.deploy'],
    install_requires = install_requires,
    dependency_links = ['http://openalea.gforge.inria.fr/pi'],

    # entry_points
    entry_points = {"wralea": ['openalea = openalea']},
    )


