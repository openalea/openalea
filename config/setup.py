"""
  OpenAlea.Config : Copyright 2006 CIRAD, INRIA
"""

import sys
old_path=sys.path
sys.path=['.']
try:
  
    from  openalea import config
except ImportError, e:
    error= """Please, run the command:
    python create_config.py
    or
    python create_config.py --prefix=/usr/local/openalea
    or
    python create_config.py --prefix=C:/openalea
    """
    raise Exception(error)

sys.path= old_path

from distutils.core import setup

description= "OpenAlea namespace and configuration"
author= "OpenAlea developers team"
url= "http://openalea.gforge.inria.fr"
license="Cecill-C"

d = setup(
    name= "OpenAlea.Config",
    version= config.version,
    description= description,
    author=author,
    url=url,
    license=license,

    #pure python  packages
    packages= [config.namespace],
    )


if(not 'install' in d.commands): sys.exit(0)

# create directories
print "Creating directories:"

import os

dirs = (config.prefix_dir,
        config.lib_dir, 
        config.include_dir,
        config.doc_dir,
        config.share_dir,
        config.bin_dir,
        config.test_dir)
	
for directory in dirs:
    try:
        print directory
        os.mkdir(directory)
    except Exception, e:
        print e

print "Setting environment variables"

import varenv

varenv.set_lsb_env('openalea', ['LD_LIBRARY_PATH=%s'%(config.prefix_dir,)])
varenv.set_win_env(['PATH=%s'%(config.prefix_dir,)])



