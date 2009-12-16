""" 
>>> python setup.py sphinx_build

"""

import os, sys
from setuptools import setup, find_packages

__revision__ = "$Id$"

# just an alias
pj = os.path.join

from openalea.deploy.metainfo import read_metainfo
metadata = read_metainfo('metainfo.ini', verbose=True)
for key,value in zip(metadata.keys(), metadata.values()):
    exec("%s = '%s'" % (key, value))

keywords = ['sphinx', 'multisetup']


setup(
    name=name,
    version=version,
    author=authors,
    author_email=authors_email,
    description=description,
    long_description=long_description,
    url=url,
    license=license,
    keywords=keywords,

    namespace_packages = ['openalea'],
    packages = find_packages('src'),

    package_dir = { '' : 'src'},


    entry_points = {
        "console_scripts": [
                 "alea_init_sphinx = openalea.misc.sphinx_tools:init",
                 "make_develop = openalea.misc.make_develop:main",
                 "upload_dist = openalea.misc.upload_dist:main",
                 "gforge_upload = openalea.misc.gforge_upload:main",
                 ],
    }

    )


