#Check dependencies

import os, sys
pj = os.path.join

name = 'OpenAlea.misc'
namespace = 'misc'

version=0.1
description = 'OpenAlea documentation.' 
long_description = ''
author = 'OpenAlea consortium'
author_email = 'thomas.Cokelaer@inria.fr'
url = 'http://openalea.gforge.inria.fr'
__license__= 'Cecill-C' 
__revision__ = "$Id: setup.py 1586 2009-01-30 15:56:25Z cokelaer $"

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


