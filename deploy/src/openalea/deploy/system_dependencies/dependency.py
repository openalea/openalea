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
#############################################################################

############################################################
# THIS MODULE IS DEPRECATED, USE DEPLOY_SYSTEM2.PY INSTEAD #
############################################################

import platform, types, warnings, collections, subprocess, abc


__all__ =  ["get_platform"]
__all__ += ["DependencySolver", "BaseDependency", "EggDependency", "InstallerDependency"]
__all__ += ["deploy_runtime_dependencies", "deploy_development_dependencies"]



# --------------------
# -- High level api --
# --------------------
def deploy_runtime_dependencies(software, osname, fake):
    theOs = OsInterfaceFactory().create(osname)
    dependencies = DependencySolver(software, osname)
    theOs.install_packages(dependencies.runtime_distribution_packages(), fake)


def deploy_development_dependencies(software, osname, fake):
    theOs = OsInterfaceFactory().create(osname)
    dependencies = DependencySolver(software, osname)
    theOs.install_packages(dependencies.development_distribution_packages(), fake)

def get_platform():
    return BaseOsFactory.get_platform()

# --------------------------------
# -- Operating system Factories --
# --------------------------------
class MSingleton(type):
    """Metaclass that makes the class that uses it a singleton"""
    instances = {}
    def __call__(cls, *args, **kwargs):
        return MSingleton.instances.setdefault(cls, type.__call__(cls, *args, **kwargs))



class BaseOsFactory(object):
    """Base class for foactories that create objects depending on the operating system"""
    __metaclass__ = MSingleton

    @classmethod
    def get_platform(cls):
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
    def intersect_and_solve(cls, platform, candidates, conflictSolve=lambda x: x[0]):
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
            intersections = cls.intersect_platform_names(platform, dist.split(" "))[0]
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



class OsInterfaceFactory(BaseOsFactory):
    """ Factory class that manages OsInterfaces. """
    def __init__(self):
        self.__oses = {}

    def create(self, osname):
        osname = self.intersect_and_solve(osname, self.get_platforms())
        return self.__oses.get(osname, None)

    def register(self, osname, osinterface):
        self.__oses[osname] = osinterface

    def get_platforms(self):
        return self.__oses.keys()



class OsInterface(object):
    """ Class whose instances define various system operations
    such as svn, yum/apt/..., etc..."""
    def __init__(self, distIntallerCmd, svnCommand):
        self.__distInstaller = distIntallerCmd
        self.__svnCommand = svnCommand

    def install_packages(self, packages, fake, batch=True):
        """ Install a list of packages that are instances of
        BaseDependency or subclasses. If batch is true
        will try to issue one single system installer command for
        all packages, instead of one per package. """
        if not issubclass(packages.__class__, collections.Iterable):
            packages = [packages]
        if batch:
            pkgnames = ""
            for p in packages:
                if p.is_base():
                    pkgnames += p.distrib_name() + " "
            self.package_install(pkgnames, fake)
        else:
            for p in packages:
                p.install(self, fake)

    def package_install(self, package, fake):
        """ Install package using the system's installer """
        command = self.__distInstaller[:]
        command += " "+ package

        if fake:
            print command
        else:
            subprocess.call(command.strip().split(" "))



# ---------------------------
# -- Dependency management --
# ---------------------------
class DistributionPackageFactory(BaseOsFactory):
    """ A factory that creates DistributionPackageNames
    properly according to the platform """
    def __init__(self):
        self.__distPkgs = {}

    def register(self, cls):
        assert isinstance(type(cls), types.TypeType)
        name = cls.__name__
        name = name[:name.find("_PackageNames")].replace("_", " ").lower()
        print "registering:", name
        self.__distPkgs[name] = cls

    def create(self, platform=None, conflictSolve=lambda x: x[0]):
        assert platform is not None
        maxIntersectionDistrib = self.intersect_and_solve(platform, self.__distPkgs.keys(), conflictSolve)
        cls = self.__distPkgs.get(maxIntersectionDistrib, None)
        if cls: return cls()



# -- Decanonification and handling special package types like eggs --
class DistributionPackageNames(dict):
    """Base class for per-OS decanonification"""
    def __init__(self, **packages):
        dict.__init__(self)
        self.update(packages)
    def update(self, other):
        ks, vs = zip(*other.iteritems())
        other = dict(zip(ks,map(lambda x: BaseDependency(x) if isinstance(x,str) else x,
                                vs)))
        dict.update(self, other)



class BaseDependency(object):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.__class__.__name__ + " " + self.name
    def __repr__(self):
        return str(self)
    def install(self, osInterface, fake):
        osInterface.package_install(self.name, fake)
    def is_base(self):return True
    def distrib_name(self):
        return self.name



class EggDependency(BaseDependency):
    def __init__(self, name):
        BaseDependency.__init__(self, name)
    def install(self, osInterface, fake):
        raise NotImplementedError
    def is_base(self):return False
    def distrib_name(self):
        return ""



class InstallerDependency(BaseDependency):
    def __init__(self, name, path):
        BaseDependency.__init__(self, name)
        self.path = path
    def __str__(self):
        return BaseDependency.__str__(self) + ":" + self.path
    def install(self, osInterface, fake):
        raise NotImplementedError
    def is_base(self):return False
    def distrib_name(self):
        return ""



class DependencySolver(object):
    __dep_tree__ = {}

    @classmethod
    def set_dependency_tree(cls, tree):
        cls.__dep_tree__ = tree

    def __init__(self, package, _platform=False):
        self.__canonical_deps = []
        self.__distribution_deps = []
        self.__translation = {}
        self.__solve_dependencies(package, _platform)

    def __str__(self):
        return "canonical->%s\ndistribution->%s\ncompensated->%s"%(str(self.__canonical_deps),
                                                                 str(self.__translation.values()),
                                                                 str(self.other_packages()))

    def packages(self):
        return self.__canonical_deps

    def runtime_distribution_packages(self):
        return [dep for canoDep, dep in self.__translation.iteritems() if canoDep[-4:] != "-dev"]

    def development_distribution_packages(self):
        return [dep for canoDep, dep in self.__translation.iteritems() if canoDep[-4:] == "-dev"]

    def other_packages(self):
        return [dep for canoDep, dep in self.__translation.iteritems() if not dep.is_base()]

    ############################################################
    # Dependency solving and distribution translation follows: #
    ############################################################
    def __solve_dependencies(self, package, _platform=False):
        assert _platform is not None
        package_deps = self.__dep_tree__.get(package, None)
        if not package_deps:
            raise Exception("No such package : " + package)

        if _platform == False:
            warnings.warn("No dependency de-canonification")

        # non recursive dependency browsing, Euler tour.
        pkgList = set()
        ancestors = collections.deque()
        childs = collections.deque()
        currentPkg = package
        currentPkgChilds = package_deps.__iter__()
        while currentPkg:
            hasChilds = True
            child = None
            try: child = currentPkgChilds.next()
            except: hasChilds = False
            if hasChilds:
                ancestors.append(currentPkg)
                childs.append(currentPkgChilds)
                currentPkg = child
                currentPkgChildsList = self.__dep_tree__.get(currentPkg, None)
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

        pkgList = list(pkgList)
        self.__canonical_deps = pkgList

        #de-canonification
        if _platform:
            distribCls = DistributionPackageFactory().create(_platform)
            if distribCls:
                for pkg in self.__canonical_deps:
                    if pkg not in self.__dep_tree__:
                        self.__translation[pkg] = distribCls[pkg]
        else:
            print "No decanonification"






# -- shortcuts for Openalea, VPlants and Alinea --
def Openalea(_platform=False):
    return DependencySolver("openalea", _platform)

def VPlants(_platform=False):
    return DependencySolver("vplants", _platform)

def Alinea(_platform=False):
    return DependencySolver("alinea", _platform)

