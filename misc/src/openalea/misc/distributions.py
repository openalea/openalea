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
import dependency

# ------------------ UBUNTU ------------------
class Ubuntu_PackageNames(dependency.DistributionPackageNames):
    def __init__(self):
        d = {"bison-dev" : "bison",
             "boostpython" : "libboost-python",
             "boostpython-dev" : "libboost-python-",
             "cgal" :  "libcgal",
             "cgal-dev" : "libcgal-dev",
             "compiler" : "g++ gfortran",
             "flex-dev" : "flex",
             "glut" : "libglut",
             "glut-dev" : "libglut-dev",
             "matplotlib" : "python-matplotlib",
             "numpy" : "python-numpy",
             "pyqt4" : "python-qt4",
             "pyqt4-dev" : "python-qt4-dev",
             "qhull" : "libqhull",
             "qhull-dev" : "libqhull-dev",
             "scipy" : "python-scipy",
             "svn-dev" : "subversion",
             }
        dependency.DistributionPackageNames.__init__(self, **d)

class Ubuntu_Karmic_PackageNames(Ubuntu_PackageNames):
    def __init__(self):
        Ubuntu_PackageNames.__init__(self)
        self["boostpython"] = dependency.EggDependency("boostpython")

dependency.DistributionPackageFactory().register(Ubuntu_PackageNames)
dependency.DistributionPackageFactory().register(Ubuntu_Karmic_PackageNames)

# ------------------ FEDORA ------------------
class Fedora_PackageNames(dependency.DistributionPackageNames):
    def __init__(self):
        d = {"bison-dev" : "bison-devel",
             "boostpython" : "boost-python",
             "boostpython-dev" : "boost-devel",
             "cgal" :  "CGAL",
             "cgal-dev" : "CGAL-devel",
             "compiler" : "gcc-c++ gcc-gfortran",
             "flex-dev" : "flex",
             "glut" : "freeglut",
             "glut-dev" : "freeglut-devel",
             "matplotlib" : "python-matplotlib",
             "numpy" : "numpy",
             "pyqt4" : "PyQt4",
             "pyqt4-dev" : "PyQt4-devel",
             "qhull" : "qhull",
             "qhull-dev" : "qhull-dev",
             "scipy" : "scipy",
             "svn-dev" : "subversion",
             }
        dependency.DistributionPackageNames.__init__(self, **d)


dependency.DistributionPackageFactory().register(Fedora_PackageNames)



