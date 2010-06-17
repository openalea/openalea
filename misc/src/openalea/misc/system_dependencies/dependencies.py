# -*- python -*-
#
#       VirtualPlant's buildbot continuous integration scripts.
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA
#
#       File author(s): Daniel Barbeau <daniel.barbeau@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
###############################################################################

"""
In this file we describe the dependencies of various projects which
can reference other projects from the same dict

This file is read by dependency.py using get_canonincal_dependencies().
"""


__all__=["get_canonincal_dependencies"]

canonical_dependencies = {
    "openalea" : ["pyqt4", "numpy", "scipy", "matplotlib", "svn-dev"],
    "vplants"  : ["openalea", "pyqt4", "boostpython", "qhull", "cgal", "glut",
                  "pyqt4-dev", "sip4-dev", "qhull-dev",
                  "cgal-dev", "boostpython-dev", "glut-dev",
                  "compilers", "bison-dev", "flex-dev"],
    "alinea"   : ["vplants", "openalea"]
}


def get_canonincal_dependencies():
    """ Returns a copy of the dependency tree """
    return canonical_dependencies.copy()
