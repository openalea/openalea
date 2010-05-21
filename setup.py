import os, sys
pj = os.path.join

from setuptools import setup, find_packages


# Package name
name = 'OpenAlea.PkgBuilder'
namespace = 'openalea'
pkg_name = 'openalea.pkg_builder'
version = '0.2.0' 
description = 'Creates a layout for openalea packages based on defined guidelines.' 

author = 'Christophe Pradal'
author_email = 'christophe pradal at cirad fr'

url = 'http://openalea.gforge.inria.fr'
license = 'Cecill-C' 

setup(
    name=name,
    version=version,
    description=description,
    author=author,
    author_email=author_email,
    url=url,
    license=license,

    namespace_packages=['openalea'],

    packages = find_packages('src'),
    package_dir={ '' : 'src' },
    zip_safe = True,

    # Dependencies
    install_requires = ['openalea.core'],
    dependency_links = ['http://openalea.gforge.inria.fr/pi'],
                     
    )


