
from dependency_builder import MSingleton, Tool, BaseBuilder, BuildEnvironment
from dependency_builder import create_metabuilder, build_epilog
from dependency_builder import options_metabuilders, options_common, options_gforge
from collections import deque, OrderedDict
import argparse
import platform
import subprocess
import sys
from os.path import join as pj



# --------------------------------------------------------------------------- #
class MPlatformAPI(MSingleton):
    apis = {}
    def __init__(cls, name, bases, dic):
        MSingleton.__init__(cls, name, bases, dic)
        if object not in bases:
            print "adding", cls
            MPlatformAPI.apis[name.lower()] = cls
    @classmethod
    def get(cls, item=None):
        if item is None:
            item = MPlatformAPI.get_platform_name()
        item = cls.intersect_and_solve(item, cls.apis.keys(), sep="_")
        item = item or "EggPackageAPI".lower()
        return MPlatformAPI.apis[item]
    @classmethod
    def get_platform_name(cls):
        """Creates a string out of the current platform with names seperated by whitespaces:
        ex: "fedora 13 goddard" or "ubuntu 9.10 karmic"."""
        _platform = None
        system = platform.system().lower()
        if system == "linux":
            dist, number, name = platform.linux_distribution()
            _platform = dist.lower() + " " + number.lower() + " " + name.lower()
        elif system == "windows":
            dist, host, name, number, proc, procinfo = platform.uname()
            _platform = dist.lower() + " " + number.lower() + " " + name.lower() + " "+ proc.lower()
        else:
            warnings.warn("Currently unhandled system : " + system + ". Implement me please.")
        return _platform        
    @classmethod
    def intersect_platform_names(cls, requestedPlatformNames, availablePlatformNames):
       """Find intersection between platformName and packageList subdictionnary keys.
       ex : ["fedora", "13", "goddard"] and ["fedora", "ubuntu"]
       returns (["fedora"]), [("13", "goddard"])"""

       requestedPlatformNames = set(requestedPlatformNames)
       availablePlatformNames = set(availablePlatformNames)
       return requestedPlatformNames&availablePlatformNames, requestedPlatformNames-availablePlatformNames
    @classmethod
    def intersect_and_solve(cls, platform, candidates, conflictSolve=lambda x: x[0], sep=" "):
        """ Given a platform name from BaseOsFactory.get_platform() or similar, and
        candidate names (ex: ["fedora 13 goddard", "ubuntu 9.10 karmic"]), this method
        will return the largest intersection of both lists and use conflictSolve to
        resolve conflicts when there are several intersections with the same number
        of items."""

        assert platform is not None
        #We find the right distribution class by intersecting
        #the platform description with the X_X_PackageNames classes
        #whose names are mangled.
        #the correct disctribution class is the one with which the
        #intersection is the largest. If there's equality between two
        #the conflict is solved using the conflictSolve function.
        platform = platform.split(" ")
        maxIntersectionAmount  = 0
        maxIntersectionDistrib = None
        for dist in candidates:
            intersections = cls.intersect_platform_names(platform, dist.split(sep))[0]
            numInters = len(intersections)
            if numInters > maxIntersectionAmount:
                maxIntersectionAmount = numInters
                maxIntersectionDistrib = dist
            elif numInters == maxIntersectionAmount and numInters > 0:
                if isinstance(maxIntersectionDistrib, list):
                    maxIntersectionDistrib.append(dist)
                elif maxIntersectionDistrib is not None:
                    maxIntersectionDistrib = [maxIntersectionDistrib, dist]
                else:
                    maxIntersectionDistrib = dist
        if isinstance(maxIntersectionDistrib, list):
            maxIntersectionDistrib = conflictSolve(maxIntersectionDistrib)
        return maxIntersectionDistrib
        
        
        
class FromEgg(object):
    """Use this in a packagemap:
    {"bison":FromEgg} means that for this particular
    dependency we will try to install it with an egg."""    
    pass        
class NA(object):
    """Use this in a packagemap:
    {"glut":NA} means that for this particular
    dependency we will not install anything."""    
    pass

    
class PlatformAPI(object):
    
    __metaclass__ = MPlatformAPI
        
    packagemap = None
    
    def __init__(self):
        # A map to translate from canonical name
        # to distribution name.
        self.packagemap = {}

    def update(self, other):
        self.packagemap.update(other)    
    
    def install_packages( self, *packages ):
        raise NotImplementedError
        
    def decanonify( self, *packages ):
        return dict( (pkg,self.packagemap[pkg]) for pkg in packages \
                      if self.packagemap[pkg] != NA)
        

class BaseEggPackageAPI(PlatformAPI, object):
    def install_packages(self, *packages):
        inst = openalea_deploy().get_path()
        if inst:
            inst = pj(inst, "alea_install.exe -g")
        else:
            inst = setuptools().get_path()
            if inst:
                inst = pj(inst, "easy_install.exe")
            else:
                return False
        deca = self.decanonify(*packages)
        pkgs = set( pkg for cano, pkg in deca.iteritems() )        
        for pkg in pkgs:
            cmd = inst + " " + pkg
            print cmd
            if subprocess.call(cmd):
                return False
        
class NativePackageAPI(PlatformAPI, object):
    """This API uses the distributions installation
    system (yum, apt-get), and can delegate to EggPackageAPI"""


    # shell command to install a package
    install_cmd = None
    
    def install_packages(self, *packages):
        deca = self.decanonify(*packages)
        eggs = []
        pkgs = []
        for (pkg, dec) in deca.iteritems():
            append_to = eggs if dec==FromEgg else pkgs
            append_to.append(pkg)
        
        if subprocess.call( self.install_cmd + " " + " ".join(pkgs) ):
            return False
        
        return EggPackageAPI().install_packages(*eggs)
        

        
def get_dependencies(package):
        dep_tree = get_canonical_dependency_tree()
        
        package_deps = dep_tree.get(package, None)
        if not package_deps:
            raise Exception("No such package : " + package)

        # non recursive dependency browsing, Euler tour.
        pkgList          = set()
        ancestors        = deque()
        childs           = deque()
        currentPkg       = package
        currentPkgChilds = package_deps.__iter__()
        while currentPkg:
            hasChilds = True
            child     = None
            try: child = currentPkgChilds.next()
            except: hasChilds = False
            if hasChilds:
                ancestors.append(currentPkg)
                childs.append(currentPkgChilds)
                currentPkg = child
                currentPkgChildsList = dep_tree.get(currentPkg, None)
                if currentPkgChildsList:
                    currentPkgChilds = currentPkgChildsList.__iter__()
                else:
                    currentPkgChilds = None
            else:
                if currentPkg != package and currentPkg not in dep_tree:
                    pkgList.add(currentPkg)
                    if len(ancestors) >= 1:
                        currentPkg = ancestors.pop()
                        currentPkgChilds = childs.pop()
                    else:
                        currentPkg = None #stops the loop
                else:
                    currentPkg = None

        return list(pkgList)
        
        
    
# --------------------------------------------------------------------------- #
def get_canonical_dependency_tree():
    """Returns a copy of the dependency tree"""
    return __canonical_dependencies.copy()

# -- our dependency tree --
__canonical_dependencies = {
    "openalea" : ["pyqt4", "numpy", "scipy", "matplotlib", 
                  "pyqscintilla", "setuptools", "pil", "soappy"],
    "vplants"  : [  "ann-dev",
                    "bison-dev",
                    "boostmath",
                    "boostmath-dev",
                    "boostpython",
                    "boostpython-dev",
                    "cgal",
                    "cgal-dev",
                    "compilers-dev",
                    "flex-dev",
                    "glut",
                    "glut-dev",
                    "nose-dev",
                    "openalea",
                    "pyopengl",
                    "pyqt4",
                    "pyqt4-dev",
                    "qhull",
                    "qhull-dev",
                    "readline",
                    "readline-dev",
                    "rpy2",
                    "scons-dev",
                    "sip4-dev",
                    "svn-dev",
                    ],
    "alinea"   : ["vplants", "openalea"]
}




#################################################
# -------------- Distributions ---------------- #
#################################################
class EggPackageAPI(BaseEggPackageAPI):
    def __init__(self):
        BaseEggPackageAPI.__init__(self)
        self.update({"ann-dev" : "ann",
                     "bison-dev" : "bisonflex==2.4.1_2.5.35",
                     "boost-dev" : "boost",
                     "boostmath" : "boost",
                     "boostmath-dev" : "boost",
                     "boostpython" : "boost",
                     "boostpython-dev" : "boost",
                     "cgal" :  NA,
                     "cgal-dev" : NA,
                     "compilers-dev" : "mingw==5.1.4_4",
                     "flex-dev" : "bisonflex==2.4.1_2.5.35",
                     "glut" : NA,
                     "glut-dev" : NA,
                     "matplotlib" : "matplotlib",
                     "nose-dev" : "nose",
                     "numpy" : "numpy",
                     "pil" : "PIL",
                     "pyopengl":"pyopengl",
                     "pyqt4" : "qt4",
                     "pyqt4-dev" : "qt4_dev",
                     "pyqscintilla" : "qt4",
                     "qhull" : "qhull",
                     "qhull-dev" : "qhull",
                     "readline": "mingw_rt==5.1.4_4",
                     "readline-dev": "mingw==5.1.4_4",
                     "rpy2" : "rpy2",
                     "setuptools" : NA,
                     "sip4-dev" : "qt4_dev",
                     "scipy" : "scipy",
                     "scons-dev" :  "scons",
                     "soappy" : "soappy",
                     "svn-dev" : NA,
             })
        
class Ubuntu(NativePackageAPI):
    install_cmd = "apt-get install"

    def __init__(self):
        NativePackageAPI.__init__(self)
        self.update({"bison-dev" : "bison",
                     "boost-dev" : "libboost-dev",
                     "boostmath" : "libboost-math",
                     "boostmath-dev" : "libboost-math-dev",
                     "boostpython" : "libboost-python",
                     "boostpython-dev" : "libboost-python-dev",
                     "cgal" :  "libcgal3",
                     "cgal-dev" : "libcgal-dev",
                     "compilers-dev" : "g++ gfortran",
                     "flex-dev" : "flex",
                     "glut" : "freeglut3",
                     "glut-dev" : "freeglut3-dev",
                     "matplotlib" : "python-matplotlib",
                     "nose-dev" : "python-nose",
                     "numpy" : "python-numpy",
                     "pil" : "python-imaging",
                     "pyopengl":"python-opengl",
                     "pyqt4" : "python-qt4 python-qt4-gl",
                     "pyqt4-dev" : "python-qt4-dev libqt4-opengl-dev",
                     "pyqscintilla" : "python-qscintilla2",
                     "qhull" : "libqhull5",
                     "qhull-dev" : "libqhull-dev",
                     "readline": "readline-common",
                     "readline-dev": "libreadline-dev",
                     "rpy2" : "python-rpy2",
                     "setuptools" : "python-setuptools",
                     "sip4-dev" : "python-sip4",
                     "scipy" : "python-scipy",
                     "scons-dev" :  "scons",
                     "soappy" : "python-soappy",
                     "svn-dev" : "subversion",
             })

class Ubuntu_Karmic(Ubuntu):
    def __init__(self):
        Ubuntu.__init__(self)
        self.update({
                     "boostmath" : "libboost-math1.38.0",
                     "boostmath-dev" : "libboost-math1.38-dev libboost1.38-dev",
                     "boostpython" : "libboost-python1.38.0",
                     "boostpython-dev" : "libboost-python1.38-dev",
        })

class Ubuntu_Lucid(Ubuntu):
    def __init__(self):
        Ubuntu.__init__(self)
        self.update({
                     "boostmath" : "libboost-math",
                     "boostmath-dev" : "libboost-math-dev",
                     "boostpython" : "libboost-python",
                     "boostpython-dev" : "libboost-python-dev",
                     "cgal" :  "libcgal4",
                     "sip4-dev":"python-sip-dev",
        })

class Ubuntu_Natty(Ubuntu_Lucid):
    def __init__(self):
        Ubuntu_Lucid.__init__(self)
        self.update({
                     "boostmath" : "libboost-math1.42.0",
                     "boostpython" : "libboost-python1.42.0",
                     "cgal" :  "libcgal5",
        })

class Ubuntu_Oneiric(Ubuntu_Natty):
    def __init__(self):
        Ubuntu_Lucid.__init__(self)
        self.update({
                     "boostmath" : "libboost-math1.46.1",
                     "boostmath-dev" : "libboost-math-dev",
                     "boostpython-dev" : "libboost-python-dev",
                     "boostpython" : "libboost-python1.46.1",
                     "cgal" :  "libcgal7",
        })

class Fedora(NativePackageAPI):
    install_cmd = "yum install"
    
    def __init__(self):
        NativePackageAPI.__init__(self)
        self.update({"bison-dev" : "bison-devel",
                     "boostmath" : "boost-math",
                     "boostmath-dev" : "boost-devel",
                     "boostpython" : "boost-python",
                     "boostpython-dev" : "boost-devel",
                     "cgal" :  "CGAL",
                     "cgal-dev" : "CGAL-devel",
                     "compilers-dev" : "gcc-c++ gcc-gfortran",
                     "flex-dev" : "flex flex-static",
                     "glut" : "freeglut",
                     "glut-dev" : "freeglut-devel",
                     "matplotlib" : "python-matplotlib",
                     "nose-dev" : "python-nose",
                     "numpy" : "numpy",
                     "pil" : "python-imaging",
                     "pyopengl":"PyOpenGL",
                     "pyqt4" : "PyQt4",
                     "pyqt4-dev" : "PyQt4-devel",
                     "pyqscintilla" : "qscintilla-python",
                     "qhull" : "qhull",
                     "qhull-dev" : "qhull-devel qhull-dev",
                     "readline": "readline",
                     "readline-dev": "readline-devel readline",
                     "rpy2" : "rpy",
                     "setuptools" : "python-setuptools",
                     "scipy" : "scipy",
                     "sip4-dev" : "sip-devel",
                     "scons-dev" :  "scons",
                     "soappy" : "SOAPpy",
                     "svn-dev" : "subversion",
             })
             
             
#################################################
# ----------- Main and Friends ---------------- #
#################################################
# This is how we interface with the dependency_builder
# infrastructure.

MDeploy = create_metabuilder("deploy")

class setuptools(Tool):
    installable    = False
    exe            = "easy_install.exe"
    default_paths  = [ Tool.PyExecPaths ]

class openalea_deploy(Tool):
    installable    = False
    exe            = "alea_install.exe"
    default_paths  = [ Tool.PyExecPaths ]

class BaseDepBuilder(BaseBuilder, object):
    __metaclass__  = MDeploy
    # Task management:
    all_tasks      = OrderedDict([("i",("_install",True)),                                  
                                 ])
    # Only execute these tasks:
    supported_tasks = "".join(all_tasks.keys())
    
    required_tools = [setuptools, openalea_deploy]
    
    def _install(self):
        pf = MPlatformAPI.get()()
        pkg = self.options["package"]
        dependencies = get_dependencies(pkg)
        
        #split dependencies into dev and rt
        rt  = []
        dev = []
        for dep in dependencies:
            append_to = dev if dep.endswith("-dev") else rt
            append_to.append(dep)
        
        to_inst = [] if self.options["no_rt"] else rt
        to_inst += [] if self.options["no_dev"] else dev

        print "Will now install", to_inst
        
        pf.install_packages(*to_inst)
        return True
        
class DepBuilder(BaseDepBuilder):
    pass
        
        
def options_installer(parser):
    g = parser.add_argument_group("System deploy options")
    g.add_argument("--no-rt",  action="store_const", default=False, const=True, 
                   help="Do not install runtime dependencies.")
    g.add_argument("--no-dev",  action="store_const", default=False, const=True, 
                   help="Do not install development dependencies.")
    g.add_argument("package", default="openalea", choices=["openalea", "vplants", "alinea"], 
                   help="Do not install development dependencies.")
    return parser
    
def parse_arguments(metabuilders):
    parser = argparse.ArgumentParser(description="Install Openalea dependencies",
                                     epilog=build_epilog(metabuilders, dep_build_end=False),
                                     formatter_class=argparse.RawDescriptionHelpFormatter,)
                                     
    parser, tools = options_metabuilders( options_gforge(options_common(parser)),
                                          metabuilders )
    parser = options_installer(parser)
                                         
    return parser.parse_args(), tools
        
def main():                                                
    metabuilders = [MDeploy]
    args, tools = parse_arguments(metabuilders)

    options = vars(args)
    options["tools"] = tools
    env = BuildEnvironment()
    env.set_options(options)
    env.set_metabuilders(metabuilders)
    return env.build()


    

if __name__ ==  "__main__":
    sys.exit( main() == False )