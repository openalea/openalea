import os, sys
pj = os.path.join

from setuptools import setup, find_packages

# Package name
#name = 'OpenAlea.PlantGLX'
name = 'plantglx'
namespace = 'openalea'
#pkg_name = 'openalea.plantglx'
pkg_name = 'plantglx'
version = '0.0.1a' 
description = 'Spline, Nurbs curve and surface tools such as interpolation.' 
long_description = description

author = 'Christophe Pradal'
author_email = 'christophe.pradal@cirad.fr'

url = 'http://openalea.gforge.inria.fr'
license = 'Cecill' 

setup(
    name=name,
    version=version,
    description=description,
    long_description=long_description,
    author=author,
    author_email=author_email,
    url=url,
    license=license,

    #namespace_packages=['openalea'],
    #create_namespaces=False,
    zip_safe=False,
    
    packages = find_packages('src/openalea'),  # include all packages under src
    package_dir = {'':'src/openalea'},   # tell distutils packages are under src

    #packages=[pkg_name],
    #package_dir={pkg_name : pj('src', 'openalea', 'plantglx')},

    # Dependencies
    #setup_requires = ['openalea.deploy'],
    #install_requires = ['openalea.core'],
    #dependency_links = ['http://openalea.gforge.inria.fr/pi'],
                     
    )


