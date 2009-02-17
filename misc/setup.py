""" This setup file is not yet operational for installation, or egg creation. 

However, the following command can be used to build the sphinx documentation  

>>> python setup.py sphinx_build

"""

import os, sys
pj = os.path.join

name = 'OpenAlea.misc'
namespace = 'misc'
version='0.6.2'
description = 'OpenAlea documentation.' 
long_description = ''
author = 'OpenAlea consortium'
author_email = 'Thomas.Cokelaer@inria.fr'
url = 'http://openalea.gforge.inria.fr'
__license__= 'Cecill-C' 
__revision__ = "$Id$"

from setuptools import setup

setup(
    name=name,
    version=version,
    description=description,
    long_description=long_description,
    author=author,
    author_email=author_email,
    url=url,
    license=license,
    )


