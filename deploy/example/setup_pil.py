#!/usr/bin/env python

from setuptools import setup
import os, os.path, glob, sys, distutils.util, shutil

name="PIL"
version="1.1.7"
description="Python Imaging Library"
author="The folks at http://www.pythonware.com/ for the hard work, Daniel Barbeau Vasquez for the egg"
author_email="daniel.barbeau@sophia.inria.fr"
url="http://www.pythonware.com/products/pil/"
license = "http://www.pythonware.com/products/pil/license.htm"

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


def unix_style_join(*args):
    l = len(args)
    if l == 1 : return args[0]
    
    ret = args[0]
    for i in range(1,l-1):
        ret += ("/" if args[i]!="" else "")+ args[i]
    
    if args[l-1] != "":
        ret += ("/" if args[l-2]!="" else "") + args[l-1]
        
    return ret
    
    
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
pyd_files = glob.glob(PIL_DIR+"/*.pyd")
py_modules = []
data_files = []
for f in py_files:
    file_ = os.path.relpath(f,PIL_DIR).replace("\\","/").replace(".py","")      
    py_modules.append( file_ )
for f in pyd_files:
    file_ = os.path.relpath(f,PIL_DIR).replace("\\","/")
    data_files.append(file_)    

############################
# DON'T LOOK, THIS IS UGLY #
############################
all_copyable_files = py_files + pyd_files
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
          
except Exception, e:
    print e
finally:
    for f in all_copyable_files : 
        os.remove(os.path.relpath(f, PIL_DIR))      