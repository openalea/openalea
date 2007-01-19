# This file allow to use openalea packages without installing them.


import os
import openalea
 
pkg_dirs = [ "core/trunk/src",
             "visualea/trunk/src",
             "library/trunk/src",
             "/usr/lib/python2.4/site-packages/openalea/"
             ]

 
for subdir in  pkg_dirs:
    
    for p in __path__:
        newpath = os.path.join(p, os.path.normpath(subdir))
 
        if(os.path.isdir(newpath)):
            __path__.append( newpath )
            break
