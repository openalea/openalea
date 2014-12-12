# -*- python -*-
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2014 INRIA - CIRAD - INRA
#
#       File author(s): Julien Coste <julien.coste@inria.fr>
#
#       File contributor(s):
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################
__revision__ = ""

import os
from openalea.core.settings import get_project_dir
from openalea.core.path import path
from openalea.deploy.shared_data import shared_data
from openalea import oalab

#GBY Review: this function could go into openalea and also in path method
def symlink(source, link_name):
    """
    os.symlink but with windows support.

    Come from:
    http://stackoverflow.com/questions/6260149/os-symlink-support-in-windows
    """
    os_symlink = getattr(os, "symlink", None)
    if callable(os_symlink):
        try:
            os_symlink(source, link_name)
        except:
            pass
    else:
        import ctypes
        csl = ctypes.windll.kernel32.CreateSymbolicLinkW
        csl.argtypes = (ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint32)
        csl.restype = ctypes.c_ubyte
        flags = 1 if os.path.isdir(source) else 0
        if csl(link_name, source, flags) == 0:
            raise ctypes.WinError()

def create_project_shortcut():
    """
    Create a shortcut/symlink inside project directory to oalab.share directory.
    Permit to access to oalab examples simpler.
    """
    project_dir = get_project_dir()
    project_link_name = path(project_dir)/"oalab_examples"
    if not project_link_name.exists():
        oalab_dir = shared_data(oalab)
        symlink(oalab_dir,project_link_name)
