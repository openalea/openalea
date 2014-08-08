# -*- coding: utf-8 -*-
""" 
>>> python setup.py sphinx_build

"""
__revision__ = "$Id: setup.py 3618 2012-06-18 15:58:17Z pradal $"

import os, sys
from setuptools import setup, find_packages

__revision__ = "$Id: setup.py 3618 2012-06-18 15:58:17Z pradal $"

# just an alias
pj = os.path.join

from openalea.deploy.metainfo import read_metainfo
metadata = read_metainfo('metainfo.ini', verbose=True)
for key,value in metadata.iteritems():
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
    package_data = { '': ["*.rst"]},
    share_dirs = { 'share' : 'share' },


    entry_points = {
        "console_scripts": [
                 "alea_init_sphinx = openalea.misc.sphinx_tools:init",
                 "make_develop = openalea.misc.make_develop:main",
                 "upload_dist = openalea.misc.upload_dist:main",
                 "gforge_upload = openalea.misc.gforge_upload:main",
                 "alea_branch = openalea.misc.alea_branch:main",
                 ],

            "wralea": [ 
                        "openalea.misc.test = openalea.misc_wralea_test",
                        "openalea.misc= openalea.misc_wralea",
            ]

    }

    )


#            "wralea": [ "openalea.misc = misc_wralea",
#                        "openalea.misc.test = misc_wralea_test",
# #           ]

