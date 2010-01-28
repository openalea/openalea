#!/usr/bin/env python

from setuptools import setup
import os, os.path, glob, sys, shutil, distutils.util

if distutils.util.get_platform() != "win32":
    print "Do not run this outside MSWindows."
    sys.exit(-1)

name="PIL"
version="1.1.7"
description="Python Imaging Library"
author="The folks at http://www.pythonware.com/ for the hard work, Daniel Barbeau Vasquez for the egg"
author_email="daniel.barbeau@sophia.inria.fr"
url="http://www.pythonware.com/products/pil/"
license = "http://www.pythonware.com/products/pil/license.htm"

#########################################################
# Content of the PIL.py module that fakes the namespace #
# It remaps the top level modules as local variables    #
# with the same name as the modules.                    #
#########################################################
PIL_MODULE = """
#Compatibility module for users that do "from PIL import Image".
#Author : Daniel Barbeau, Virtual Plants, INRIA-CIRAD
#License : CeCILL-C
#Year : 2010

import os, sys
import os.path


def my_try_import(f):
    try : return __import__(f)
    except : return None

direc = os.path.dirname(__file__)
files = os.listdir(direc)
modules = [(os.path.splitext(f)[0], my_try_import(os.path.splitext(f)[0])) for f in files if f.endswith(".py")]

x = [eval("sys.modules[__name__].__setattr__(f,m)") for f,m in modules if m is not None]

del os.path
del os
del sys
"""
    
    
####################################
# FINDING THE PIL INSTALLATION DIR #
####################################
try:
    import Image
except:
    print "PIL not found"
    sys.exit(-1)

PIL_DIR = os.path.dirname(Image.__file__)
if not os.path.exists(PIL_DIR):
    print "ERROR: could not find PIL directory :", PIL_DIR 
    sys.exit(-1)

######################################
# Fake PIL namespace module creation #
######################################
pil_mod = open( os.path.join(PIL_DIR,"PIL.py"), "w" )
pil_mod.write(PIL_MODULE)
pil_mod.close()

PIL_DIR = PIL_DIR.replace("\\", "/") #because distutils expects / instead of \\

#####################################################################
# some voodoo to identify the files to copy and where to place them #
#####################################################################
py_files = glob.glob(PIL_DIR+"/*.py")
other_files = glob.glob(PIL_DIR+"/*.pyd")
other_files += glob.glob(PIL_DIR+"/*.pth")
py_modules = []
data_files = []
for f in py_files:
    #because we must represent them as modules we replace slashes by dots.
    file_ = os.path.relpath(f,PIL_DIR).replace("\\","/")
    py_modules.append( file_[:-3] )
for f in other_files:
    file_ = os.path.relpath(f,PIL_DIR).replace("\\","/")
    data_files.append(file_)    

############################
# DON'T LOOK, THIS IS UGLY #
############################
all_copyable_files = py_files + other_files
HERE = os.getcwd()
for f in all_copyable_files : 
    shutil.copy2(f, HERE)
    

#############
# Let's go! #
#############
try:
    setup(name=name,
          version=version,
          description=description,
          author=author,
          author_email=author_email,
          url=url,
          license = license,
          py_modules = py_modules,
          data_files = [("",data_files)],
          zip_safe = False,
          )
          
    egg = glob.glob("dist/*.egg")[0]
    os.rename(egg, egg[:-4]+"-win32.egg")
    
except Exception, e:
    print e
finally:
    for f in all_copyable_files : 
        os.remove(os.path.relpath(f, PIL_DIR))