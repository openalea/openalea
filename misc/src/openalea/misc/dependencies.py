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


canonical_dependencies = {
    "openalea" : ["pyqt4", "numpy", "scipy", "matplotlib", "svn-dev"],
    "vplants"  : ["openalea", "pyqt4", "boostpython", "qhull", "cgal", "glut",
                  "pyqt4-dev", "sip4-dev", "qhull-dev",
                  "cgal-dev", "boostpython-dev", "glut-dev",
                  "compilers", "bison-dev", "flex-dev"],
    "alinea"   : ["vplants", "openalea"]
}



