#!/usr/bin/env python

from setuptools import setup
import os, os.path, sys, distutils.util

name="MinGW"
version="5.1.4-1"
description="MinGW compiler distrubution with GCC 4.4"
author="The guys at www.mingw.org for the hard work, Daniel Barbeau Vasquez for the egg"
author_email="daniel.barbeau@sophia.inria.fr"
url="www.mingw.org"


def unix_style_join(*args):
    l = len(args)
    if l == 1 : return args[0]
    
    ret = args[0]
    for i in range(1,l-1):
        ret += ("/" if args[i]!="" else "")+ args[i]
    
    if args[l-1] != "":
        ret += ("/" if args[l-2]!="" else "") + args[l-1]
        
    return ret
    
    
######################################
# FINDING THE MINGW INSTALLATION DIR #
######################################
OLD_DIR = os.getcwd()
MINGWDIR = OLD_DIR
if not os.path.exists(os.path.join(MINGWDIR, "bin", "mingw32-g++.exe")):
    MINGWDIR = os.path.join("c:\\", "mingw")
if not os.path.exists(os.path.join(MINGWDIR, "bin", "mingw32-g++.exe")):
    print "ERROR: could not find MINGW directory :", MINGWDIR 
    sys.exit(-1)
os.chdir(MINGWDIR)
MINGWDIR = MINGWDIR.replace("\\", "/") #because distutils expects / instead of \\

#####################################################################
# some voodoo to identify the files to copy and where to place them #
#####################################################################
raw_files = os.walk(MINGWDIR)
data_files = []
for i,j,k in raw_files:
    for f in k:
        #we want to reproduce the same hierarchy inside the egg.
        #as inside the MINGWDIR.
        rel = os.path.relpath(i,MINGWDIR).replace("\\","/") 
        file_ = unix_style_join( rel, f)        
        data_files.append( ("" if rel == "." else rel,[file_]) )

#############
# Let's go! #
#############
setup(name=name,
      version=version,
      description=description,
      author=author,
      author_email=author_email,
      url=url,
      data_files = data_files,
      zip_safe = False,
      bin_dirs = { 'bin' : 'bin' },
      lib_dirs = { 'lib' : 'lib' },      
      inc_dirs = { 'include' : 'include' },
      setup_requires = ['openalea.deploy'],
      dependency_links = ['http://openalea.gforge.inria.fr/pi'],      
      )
      
os.chdir(OLD_DIR)