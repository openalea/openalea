
# This file allow to use openalea packages without installing them.

print "toto"
import os
import openalea
from distutils.sysconfig import get_python_lib

openalea_dir= os.path.join(get_python_lib(),'openalea')

pkg_dirs = [ "core/src",
             "visualea/src",
             "catalog/src",
             "distx",
             "sconsx/src",
             openalea_dir
             ]

 
for subdir in  pkg_dirs:    
    for p in __path__:
        newpath = os.path.join(p, os.path.normpath(subdir))
 
        if(os.path.isdir(newpath)):
            __path__.append( newpath )
            

try:
    import vplants
    __path__ += vplants.__path__
except:
    pass


del get_python_lib
del openalea_dir
