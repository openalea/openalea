# -*- python -*-
#
#       OpenAlea.Core
#
#       Copyright 2011 INRIA - CIRAD - INRA
#
#       File author(s): Daniel BARBEAU <daniel.barbeau@inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################
""" This file contains fixes for shared library location under different
oses"""

__license__ = "Cecill-C"
__revision__ = " $Id$ "


import os
import os.path
import sys
from ctypes import util as ctutil


def find_library(name):
    """Similar to ctypes.util.find_library except that on posixes that
    are not darwin, besides using ldconfig, gcc and objdump, it also
    browses the LD_LIBRARY_PATH."""
    libname = ctutil.find_library(name)
    if not libname:
        if os.name == "posix" and sys.platform != "darwin":
            lddirs = os.environ.get("LD_LIBRARY_PATH", "")
            lddirs = lddirs.split(":")
            libs   = [f for d in lddirs if os.path.exists(d) for f in os.listdir(d)]
            candidateName = "lib"+name+".so"
            for lname in libs:
                if candidateName in lname and not lname.endswith("egm"):
                    libname = lname
                    break
    return libname
