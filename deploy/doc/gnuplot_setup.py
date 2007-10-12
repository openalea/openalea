import sys
import os

from setuptools import setup, find_packages

setup(
    # Metadata for PyPi
    name = "gnuplot",
    version = "4.2.2-1",
    author = "",
    author_email = "",
    description = "The Gnuplot Plotting Utility",
    license = 'The Gnuplot license',
    keywords = '',
    url = 'http://www.gnuplot.info/',
    
    include_package_data = True,
    zip_safe= False,

    # Specific options of openalea.deploy
    bin_dirs = {'bin': 'bin' },
    share_dirs = {'contrib' : 'contrib','demo':'demo','docs':'docs','info' : 'info'},

    # Dependencies
    setup_requires = ['openalea.deploy'],
    dependency_links = ['http://openalea.gforge.inria.fr/pi'],
    #install_requires = [],
    
)

