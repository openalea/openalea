import os, sys
from setuptools import setup
sys.path.append("src")
import visualea.metainfo as metainfo
pj = os.path.join


# Meta Informations
name = 'OpenAlea.Visualea'
namespace = 'openalea'
pkg_name = 'openalea.visualea'
version = '0.6.2'

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
    py_modules = ['visualea_postinstall'],
    namespace_packages = ["openalea"],
    create_namespaces = True,
    
    packages = [pkg_name],
    package_dir = {pkg_name : pj('src', 'visualea'), '' : 'src', },
    include_package_data = True,
    zip_safe = False,
    
    # Scripts
    entry_points = { 'gui_scripts': [
                           'visualea = openalea.visualea.visualea_script:start_gui',
                           'aleashell = openalea.visualea.shell:main',

                           ]},

    postinstall_scripts = ['visualea_postinstall'],
    share_dirs = { 'share' : 'share' },
 
    # Dependencies
    setup_requires = ['openalea.deploy'],
    dependency_links = ['http://openalea.gforge.inria.fr/pi'],
    install_requires = ['openalea.core'],
 
    )


