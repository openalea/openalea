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
    "openalea" : ["pyqt4", "numpy", "scipy", "matplotlib", "pyqscintilla"],
    "vplants"  : ["openalea", "pyqt4", "boostpython", "qhull", "cgal", "glut",
                  "pyqt4-dev", "sip4-dev", "qhull-dev", "pyopengl",
                  "cgal-dev", "boostpython-dev", "glut-dev", "readline", "readline-dev",
                  "compilers-dev", "bison-dev", "flex-dev", "svn-dev", "scons-dev"],
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
             "boostpython-dev" : "libboost-python-dev",
             "cgal" :  "libcgal3",
             "cgal-dev" : "libcgal-dev",
             "compilers-dev" : "g++ gfortran",
             "flex-dev" : "flex",
             "glut" : "freeglut3",
             "glut-dev" : "freeglut3-dev",
             "matplotlib" : "python-matplotlib",
             "numpy" : "python-numpy",
             "pyopengl":"python-opengl",
             "pyqt4" : "python-qt4",
             "pyqt4-dev" : "python-qt4-dev",
             "pyqscintilla" : "python-qscintilla2",
             "qhull" : "libqhull5",
             "qhull-dev" : "libqhull-dev",
             "readline": "readline-common",
             "readline-dev": "libreadline-dev",
             "sip4-dev" : "python-sip4",
             "scipy" : "python-scipy",
             "scons-dev" :  "scons",
             "svn-dev" : "subversion",
             }
        dependency.DistributionPackageNames.__init__(self, **d)

class Ubuntu_Karmic_PackageNames(Ubuntu_PackageNames):
    def __init__(self):
        Ubuntu_PackageNames.__init__(self)
        self["boostpython"] = dependency.EggDependency("boostpython")

class Ubuntu_Lucid_PackageNames(Ubuntu_PackageNames):
    def __init__(self):
        Ubuntu_PackageNames.__init__(self)
        self.update({
             "boostpython" : "libboost-python1.40.0",
             "boostpython-dev" : "libboost-python1.40-dev",
             "cgal" :  "libcgal4",
             "sip4-dev":"python-sip-dev",             
        })

# ------------------ FEDORA ------------------
class Fedora_PackageNames(dependency.DistributionPackageNames):
    def __init__(self):
        d = {"bison-dev" : "bison-devel",
             "boostpython" : "boost-python",
             "boostpython-dev" : "boost-devel",
             "cgal" :  "CGAL",
             "cgal-dev" : "CGAL-devel",
             "compilers-dev" : "gcc-c++ gcc-gfortran",
             "flex-dev" : "flex",
             "glut" : "freeglut",
             "glut-dev" : "freeglut-devel",
             "matplotlib" : "python-matplotlib",
             "numpy" : "numpy",
             "pyopengl":"PyOpenGL",
             "pyqt4" : "PyQt4",
             "pyqt4-dev" : "PyQt4-devel",
             "pyqscintilla" : "qscintilla-python",
             "qhull" : "qhull",
             "qhull-dev" : "qhull-dev",
             "readline": "readline",
             "readline-dev": "readline-devel readline",
             "scipy" : "scipy",
             "sip4-dev" : "sip-devel",
             "scons-dev" :  "scons",
             "svn-dev" : "subversion",
             }
        dependency.DistributionPackageNames.__init__(self, **d)


# -- Registering Dependency tree --
dependency.DependencySolver.set_dependency_tree(get_canonincal_dependencies())


# -- Registering DitributionPackage translators --
dependency.DistributionPackageFactory().register(Ubuntu_PackageNames)
dependency.DistributionPackageFactory().register(Ubuntu_Karmic_PackageNames)
dependency.DistributionPackageFactory().register(Ubuntu_Lucid_PackageNames)
dependency.DistributionPackageFactory().register(Fedora_PackageNames)


# -- Registering Operating System interfaces
dependency.OsInterfaceFactory().register("ubuntu", dependency.OsInterface("apt-get install", "svn"))
dependency.OsInterfaceFactory().register("fedora", dependency.OsInterface("yum install", "svn"))
