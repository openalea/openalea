import os, sys
from setuptools import setup
pj = os.path.join


# Meta Informations
name = 'OpenAlea.Visualea'
namespace = 'openalea'
pkg_name = 'openalea.visualea'

sys.path.append("src")
import visualea.metainfo as metainfo

version = metainfo.version

description = 'OpenAlea visual programming environment.' 
long_description = ''
author = 'OpenAlea consortium'
author_email = 'samuel.dufour@sophia.inria.fr, christophe.pradal@cirad.fr'
url = metainfo.url
license = 'Cecill v2' 



setup(
    name=name,
    version=version,
    description=description,
    long_description=long_description,
    author=author,
    author_email=author_email,
    url=url,
    license=license,
    keywords='visual programming',

    # Packages
    namespace_packages = ["openalea"],
    create_namespaces = True,
    
    packages = [pkg_name],
    package_dir = {pkg_name : pj('src', 'visualea')},
    include_package_data = True,
    zip_safe = False,
    
    # Scripts
    entry_points = { 'gui_scripts': [
                           'visualea.py = openalea.visualea.visualea_script:start_gui',]},
 
    # Dependencies
    setup_requires = ['openalea.deploy'],
    dependency_links = ['http://openalea.gforge.inria.fr/pi'],
    install_requires = ['openalea.core'],
 
    )


