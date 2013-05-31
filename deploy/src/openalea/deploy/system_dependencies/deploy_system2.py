# -*- python -*-
#
#       openalea.deploy.platform_install
#
#       Copyright 2006-2012 INRIA - CIRAD - INRA
#
#       File author(s): Daniel Barbeau
#       File Contributors(s):
#                             - your name heredeploy/src/openalea/deploy/system_dependencies/deploy_system2.py
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

from dependency_builder import MSingleton, BaseBuilder, BuildEnvironment, BE
from dependency_builder import create_metabuilder, build_epilog
from dependency_builder import options_metabuilders, options_common, options_gforge
from dependency_builder import exe_ext, makedirs, download, download_egg, setuptools, openalea_deploy
from collections import deque, OrderedDict
import argparse
import platform
import subprocess
import sys
import urlparse
from os.path import join as pj, isdir, splitext



# --------------------------------------------------------------------------- #
class MPlatformAPI(MSingleton):
    apis = {}
    def __init__(cls, name, bases, dic):
        MSingleton.__init__(cls, name, bases, dic)
        if object not in bases:
            #print "adding", cls
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

    @classmethod
    def install_packages(cls, *packages):
        # we build a chain of responsability
        first = cls.get()
        c_o_r = [first]
        c_o_r += [api_cls for api_cls in cls.apis.itervalues() \
                  if api_cls!=first and \
                  not issubclass(api_cls, NativePackageAPI)] #because this should be "first"
        
        print c_o_r
        action_men = OrderedDict()
        
        to_inst = packages[:]
        while( len(to_inst) and len(c_o_r)):
            api = c_o_r.pop(0)()
            handled, to_inst = api.decanonify(*to_inst)
            action_men[api] = handled

        print "The packages will be installed:"
        for api, handled in action_men.iteritems():
            print "\t - using", api.__class__.__name__, "for"
            for h in handled:
                print "\t\t", h

        if len(to_inst):
            print "Will NOT install these (couldn't find any way to install them) :"
            for p in to_inst:
                print "\t", p
                
        if not BE.options.get("yes_to_all") and raw_input("Do you want to proceed? (y/n):").lower() != "y":
            return False

        for api, handled in action_men.iteritems():
            apiName = api.__class__.__name__
            print "Using", apiName
            if not BE.options.get("yes_to_all") and BE.options.get("confirm_each") and raw_input("Install the %s group? (y/n):"%apiName).lower()=="n":
                continue
            if api.install_packages(*handled) == False:
                return False
        return True

class DepSpec(object):
    pass
        
class Egg(DepSpec):
    def __init__(self, spec):
        self.spec = spec
    def __str__(self):
        return self.spec        
    def __repr__(self):
        return repr(self.spec)
    def __hash__(self):
        return hash(self.spec)
    def __eq__(self, other):
        return self.spec.__eq__(other.spec)    
    def __ne__(self, other):
        return self.spec.__ne__(other.spec)
        
class WinInst(DepSpec): #for exes and msi
    def __init__(self, url, ez_name=None):
        self.url = url
        self.ez_name = ez_name or urlparse.urlsplit(url).path.split("/")[-1]
    def __str__(self):        
        if BE.verbose:
            return self.url+ " => " + self.ez_name
        else:
            return self.ez_name
    def __repr__(self):
        return "WinInst(" + repr(self.url) + ", " + repr(self.ez_name) + ")"
    def __hash__(self):
        return hash(self.ez_name)
    def __eq__(self, other):
        return self.ez_name.__eq__(other.ez_name)    
    def __ne__(self, other):
        return self.spec.__ne__(other.ez_name)

class NA(object):
    """Use this in a packagemap:
    {"glut":NA} means that for this particular
    dependency will be delegated to another PlatformAPI."""    
    pass

class Ignore(object):
    """Use this in a packagemap:
    {"glut":Ignore} means that for this particular
    dependency no error will be raised i.e. doesn't need to be installed."""    
    pass

    
class PlatformAPI(object):
    
    __metaclass__ = MPlatformAPI
        
    packagemap = None
    
    handled_decanofied_types = set([str])

    def __init__(self):
        # A map to translate from canonical name
        # to distribution name.
        deps = get_all_deps()
        self.packagemap = dict.fromkeys( deps, NA )       

    def update(self, other):
        self.packagemap.update(other)    
    
    def install_packages( self, *packages ):
        raise NotImplementedError
        
    def decanonify( self, *packages ):
        handled = set()#[]
        not_handled = set()
        for pkg in packages:
            deca_list = self.packagemap[pkg]
            #make everything a list
            if isinstance(deca_list, str):
                deca_list = deca_list.split(" ")
            elif isinstance(deca_list, DepSpec):
                deca_list = [deca_list]
            elif isinstance(deca_list, list):
                pass
            elif deca_list==Ignore:
                print "Info: ignoring", pkg
                continue
            elif deca_list==NA:
                print "Info: Delegating", pkg
                not_handled.add(pkg)
                continue
            else:
                raise Exception("Bad dependency type: %s is %s. The package must be added to this platform's package map."%(pkg, deca_list.__name__))
            for deca in deca_list:
                if set([deca, type(deca)]) or set(self.handled_decanofied_types):
                    handled.add(deca)
                else:
                    not_handled.add(pkg)
        return list(handled), list(not_handled)
        

class BaseEggPackageAPI(PlatformAPI, object):
    handled_decanofied_types = set([Egg])
    def install_packages(self, *packages):
        inst = openalea_deploy().get_path()
        if inst:
            if BE.options.get("gforge"):
                inst = pj(inst, "alea_install%s -g"%exe_ext)
            else:
                inst = pj(inst, "alea_install%s "%exe_ext)
        else:
            inst = setuptools().get_path()
            if inst:
                inst = pj(inst, "easy_install%s"%exe_ext)
            else:
                return False
                
        if not BE.options.get("no_sudo_easy_install"):
            inst = "sudo " + inst

        tempdir = BE.options.get("dldir")
        if not isdir(tempdir):
            makedirs(tempdir)        
        for pkg in packages:
            # first download:
            if not download_egg(pkg.spec, tempdir):
                return False
            if BE.options.get("dl_only"):
                print "skipping installation"
                continue
            cmd = inst + " -i "+ tempdir + " " + pkg.spec
            print cmd            
            if subprocess.call(cmd, shell=True):
                return False
        return True
        

class NativePackageAPI(PlatformAPI, object):
    """This API uses the distributions installation
    system (yum, apt-get), and can delegate to EggPackageAPI"""

    # shell command to install a package
    install_cmd = None
    
    def install_packages(self, *packages): 
        cmd = self.install_cmd + " " + " ".join(packages)
        print cmd
        if subprocess.call( cmd, shell=True ):
            return False
        return True        


class BaseWindowsPackageAPI(NativePackageAPI):
    handled_decanofied_types = set([WinInst])
    
    def install_packages(self, *packages):
        tempdir = BE.options.get("dldir")
        if not isdir(tempdir):
            makedirs(tempdir)
        for pkg in packages:
            assert isinstance(pkg, WinInst)
            # First we download to pkg_pth, then we install
            pkg_pth = pj(tempdir, pkg.ez_name)
            if not download(pkg.url, pkg.ez_name, pkg_pth):
                return False
            if BE.options.get("dl_only"):
                print "skipping installation"
                continue
            name, ext = splitext(pkg.ez_name.lower())
            if ext == ".exe":
                if subprocess.call(pkg_pth, shell=True):
                    return False
            elif ext == ".msi":
                if subprocess.call("msiexec /i "+pkg_pth):
                    return False
            else:
                print "trying to install %s but found no way to do so."%pkg_pth
        return True   
           
        
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
                if currentPkg != package:
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
def get_all_deps():
    return [ dep for deps in get_canonical_dependency_tree().itervalues() for dep in deps \
            if dep not in ("openalea", "vplants", "alinea") ]
            
def get_canonical_dependency_tree():
    """Returns a copy of the dependency tree"""
    return __canonical_dependencies.copy()

# -- our dependency tree --
__canonical_dependencies = {
    "rpy2"   : ["r"],
    "soappy" : ["fpconst", "wstools"], 
    "openalea" : ["pyqt4", "numpy", "scipy", "matplotlib", 
                  "pyqscintilla", "setuptools", "pil", "soappy", "pylsm", "pylibtiff"],
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
                    "gnuplot",
                    "nose-dev",
                    "networkx",
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

if "win32" in sys.platform:
    __canonical_dependencies["openalea"].append("pywin32")


#################################################
# -------------- Distributions ---------------- #
#################################################
class EggPackageAPI(BaseEggPackageAPI):
    def __init__(self):
        BaseEggPackageAPI.__init__(self)
        self.update({"ann-dev" : Egg("ann"),
                     "bison-dev" : Egg("bisonflex==2.4.1_2.5.35"),
                     "boost-dev" : Egg("boost"),
                     "boostmath" : Egg("boost"),
                     "boostmath-dev" : Egg("boost"),
                     "boostpython" : Egg("boost"),
                     "boostpython-dev" : Egg("boost"),
                     "cgal" :  Egg("cgal"),
                     "cgal-dev" : Egg("cgal"),
                     "compilers-dev" : Egg("mingw==5.1.4_4b"),
                     "flex-dev" : Egg("bisonflex==2.4.1_2.5.35"),
                     "fpconst" : Egg("fpconst==0.7.2"),
                     "glut" : NA,
                     "glut-dev" : NA,
                     "gnuplot" : Egg("gnuplot"),
                     "matplotlib" : Egg("matplotlib"),
                     "networkx" : Egg("networkx"),
                     "nose-dev" : Egg("nose"),
                     "numpy" : Egg("numpy"),
                     "pil" : Egg("PIL"),
                     "pylsm" : Egg("pylsm"),
                     "pyopengl": Egg("pyopengl"),
                     "pyqt4" : [Egg("qt4"), Egg("pyqglviewer")],
                     "pyqt4-dev" : Egg("qt4_dev"),
                     "pyqscintilla" : Egg("qt4"),
                     "qhull" : Egg("qhull"),
                     "qhull-dev" : Egg("qhull"),
                     "readline": Egg("mingw_rt==5.1.4_4b"),
                     "readline-dev": Egg("mingw==5.1.4_4b"),
                     "rpy2" : Egg("rpy2"),
                     "setuptools" : NA,
                     "sip4-dev" : Egg("qt4_dev"),
                     "scipy" : Egg("scipy"),
                     "scons-dev" : Egg("scons"),
                     "soappy" : Egg("soappy"),
                     "svn-dev" : NA,
                     "wstools" : Egg("wstools==0.3"),
             })
             
class Ubuntu(NativePackageAPI):
    install_cmd = "sudo apt-get install"

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
                     "networkx": "python-networkx",
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
                     "sip4-dev" : "python-sip4",
                     "scons-dev" :  "scons",
                     "soappy" : "python-soappy",
                     "svn-dev" : "subversion",
                     "wstools": Ignore,
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
        Ubuntu_Natty.__init__(self)
        self.update({
                     "boostmath" : "libboost-math1.46.1",
                     "boostmath-dev" : "libboost-math-dev",
                     "boostpython-dev" : "libboost-python-dev",
                     "boostpython" : "libboost-python1.46.1",
                     "cgal" :  "libcgal7",
        })
        
class Ubuntu_Precise(Ubuntu_Oneiric):
    def __init__(self):
        Ubuntu_Oneiric.__init__(self)
        self.update({
                     "boostmath" : "libboost-math1.48.0",
                     "boostmath-dev" : "libboost-math1.48-dev libboost1.48-dev",
                     "boostpython" : "libboost-python1.48.0",
                     "boostpython-dev" : "libboost-python1.48-dev",
                     "cgal" :  "libcgal8",
        })


class Fedora(NativePackageAPI):
    install_cmd = "sudo yum install"
    
    def __init__(self):
        NativePackageAPI.__init__(self)
        self.update({"ann-dev": NA,
                     "bison-dev" : "bison-devel",
                     "boostmath" : "boost-math",
                     "boostmath-dev" : "boost-devel",
                     "boostpython" : "boost-python",
                     "boostpython-dev" : "boost-devel",
                     "cgal" :  "CGAL",
                     "cgal-dev" : "CGAL-devel",
                     "compilers-dev" : "gcc-c++ gcc-gfortran",
                     "flex-dev" : "flex flex-static",
                     "fpconst" : "python-fpconst",
                     "glut" : "freeglut",
                     "glut-dev" : "freeglut-devel",
                     "gnuplot": "gnuplot",
                     "matplotlib" : "python-matplotlib",
                     "networkx" : "python-networkx",
                     "nose-dev" : "python-nose",
                     "numpy" : "numpy",
                     "pil" : "python-imaging",
                     "pyopengl":"PyOpenGL",
                     "pyqt4" : "PyQt4",
                     "pyqt4-dev" : "PyQt4-devel",
                     "pyqscintilla" : "qscintilla-python",
                     "qhull" : "qhull",
                     "qhull-dev" : "qhull-devel qhull-dev", #probably to handle ancient naming
                     "readline": "readline",
                     "readline-dev": "readline-devel readline",
                     "rpy2" : "rpy",
                     "setuptools" : "python-setuptools",
                     "scipy" : "scipy",
                     "sip4-dev" : "sip-devel",
                     "scons-dev" :  "scons",
                     "soappy" : "SOAPpy",
                     "svn-dev" : "subversion",
                     "wstools": Ignore
             })
             
class Fedora_16(Fedora):
    def __init__(self):
        Fedora.__init__(self)
        self.update({"ann-dev": "ann-devel"})


class Windows(BaseWindowsPackageAPI):
    def __init__(self):
        BaseWindowsPackageAPI.__init__(self)
        self.update({
                     "python" : WinInst("http://python.org/ftp/python/2.7.2/python-2.7.2.msi"),
                     "pywin32" : WinInst("http://freefr.dl.sourceforge.net/project/pywin32/pywin32/Build%20217/pywin32-217.win32-py2.7.exe"),
                     "matplotlib" : WinInst("http://freefr.dl.sourceforge.net/project/matplotlib/matplotlib/matplotlib-1.1.0/matplotlib-1.1.0.win32-py2.7.exe"),
                     "numpy" : WinInst("http://freefr.dl.sourceforge.net/project/numpy/NumPy/1.6.1/numpy-1.6.1-win32-superpack-python2.7.exe"),
                     "pil" : WinInst("http://effbot.org/media/downloads/PIL-1.1.7.win32-py2.7.exe"),
                     "pyopengl": WinInst("http://pypi.python.org/packages/any/P/PyOpenGL/PyOpenGL-3.0.1.win32.exe#md5=513cc194af65af4c5a640cf9a1bd8462"),
                     "r": WinInst("http://mirror.ibcp.fr/pub/CRAN/bin/windows/base/old/2.14.2/R-2.14.2-win.exe"),
                     "setuptools" : WinInst("http://pypi.python.org/packages/2.7/s/setuptools/setuptools-0.6c11.win32-py2.7.exe#md5=57e1e64f6b7c7f1d2eddfc9746bbaf20"),
                     "scipy" : WinInst("http://freefr.dl.sourceforge.net/project/scipy/scipy/0.10.1/scipy-0.10.1-win32-superpack-python2.7.exe"),
                     "svn-dev" : WinInst("http://freefr.dl.sourceforge.net/project/win32svn/1.6.9/Setup-Subversion-1.6.9.msi")
             })


             
#################################################
# ----------- Main and Friends ---------------- #
#################################################
# This is how we interface with the dependency_builder
# infrastructure.

MDeploy = create_metabuilder("deploy")

class BaseDepBuilder(BaseBuilder, object):
    __metaclass__  = MDeploy
    # Task management:
    all_tasks      = OrderedDict([("i",("_install",True)),                                  
                                 ])
    # Only execute these tasks:
    supported_tasks = "".join(all_tasks.keys())
    
    required_tools = [setuptools, openalea_deploy]
    
    def _install(self):    
        pkg = self.options["package"]
        all_pkgs = get_all_deps()
        dependencies = get_dependencies(pkg)
        for to_skip in self.options["skip_inst"]:
            print "removing", to_skip, "from dependencies"
            assert to_skip in all_pkgs
            dependencies.remove(to_skip)
        
        #split dependencies into dev and rt
        rt  = []
        dev = []
        for dep in dependencies:
            append_to = dev if dep.endswith("-dev") else rt
            append_to.append(dep)
        
        to_inst = [] if self.options["no_rt"] else rt
        to_inst += [] if self.options["no_dev"] else dev
        
        try:
            to_inst.remove("openalea")
        except:
            pass
        try:
            to_inst.remove("vplants")
        except:
            pass
        try:
            to_inst.remove("alinea")
        except:
            pass            
        print "Will install dependencies for", MPlatformAPI.get_platform_name()

        return MPlatformAPI.install_packages(*to_inst)
        
class DepBuilder(BaseDepBuilder):
    pass
        
        
def options_installer(parser):
    g = parser.add_argument_group("System deploy options")
    g.add_argument("--confirm-each", action="store_true", 
                   help="User must confirm each group of packages to install. default=False")
    g.add_argument("--dldir" , default="system_deploy2_temp",
                   help="Directory where downloads will be stored, if any.")
    g.add_argument("--no-rt",  action="store_true", 
                   help="Do not install runtime dependencies.")
    g.add_argument("--no-dev",  action="store_true",
                   help="Do not install development dependencies.")
    g.add_argument("--dl-only", "-x", action="store_true", 
                   help="Download dependencies but do not install them.")
    g.add_argument("--yes-to-all", "-y", action="store_true",
                   help="Download dependencies but do not install them.")    
    g.add_argument("--skip-inst", default="",
                   help="name of packages to download but not to install (comma seperated).")
    g.add_argument("--no-sudo-easy-install", action="store_false",
                   help="Don't use sudo to install with easy-install (use this with virtualenv).")
    g.add_argument("package", default="openalea", choices=["openalea", "vplants", "alinea"], 
                   help="The package to install dependencies for.")
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

    args.skip_inst = args.skip_inst.split(",") if args.skip_inst != "" else []
    options = vars(args)
    options["tools"] = tools
    options["pass_path"]=True
    env = BuildEnvironment()
    env.set_options(options)
    env.set_metabuilders(metabuilders)
    return env.build()


    

if __name__ ==  "__main__":
    sys.exit( main() == False )
