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


# -- our dependency tree --

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


# -- Registering Dependency tree --
dependency.DependencySolver.set_dependency_tree(get_canonincal_dependencies())


# -- Registering DitributionPackage translators --
dependency.DistributionPackageFactory().register(Ubuntu_PackageNames)
dependency.DistributionPackageFactory().register(Ubuntu_Karmic_PackageNames)
dependency.DistributionPackageFactory().register(Fedora_PackageNames)


# -- Registering Operating System interfaces
dependency.OsInterfaceFactory().register("ubuntu", dependency.OsInterface("apt-get install", "svn"))
dependency.OsInterfaceFactory().register("fedora", dependency.OsInterface("yum install", "svn"))
