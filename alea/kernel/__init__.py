"""
Kernel package contains Package Manager and Worflow plus utilities. 
"""

import os
from os.path import join
print __path__
__path__[0]=join(__path__[0],'src')
del join
del os

import datastore, node, package, signal, top_sort
