# -*- python -*-
#
#       OpenAlea.StdLib
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################
""" File manipulation """

__license__ = "Cecill-C"
__revision__ = " $Id: files.py 2713 2010-08-09 09:43:18Z cokelaer $ "

import os

from openalea.core import *
from openalea.core.path import path

# File name manipulation

# doc generator
def doc(f_with_doc):
    def add_doc(f):
        f.__doc__ = f_with_doc.__doc__
        return f
    return add_doc

@doc(os.path.abspath)
def py_abspath(p): return path(p).abspath(),

py_basename=path.basename
@doc(path.basename)
def py_basename(p): return path(p).basename(),

@doc(path.bytes)
def py_bytes(p):
    p=path(p)
    return p.bytes(),

@doc(os.chmod)
def py_chmod(p, mode):
    path(p).chmod(mode)
    return path(p),

@doc(os.chown)
def py_chown(p, uid, gid):
    path(p).chown(uid,gid)
    return path(p),

@doc(path.copy)
def py_copy(src, dst):
    p=path(src)
    p.copy(dst)
    return p,
