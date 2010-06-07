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

import platform, types, warnings, collections
import dependencies, os_factory


def Openalea(_platform=False):
    return Dependency("openalea", _platform)

def VPlants(_platform=False):
    return Dependency("vplants", _platform)

def Alinea(_platform=False):
    return Dependency("alinea", _platform)



class Dependency(object):
    def __init__(self, package, _platform=False):
        self.__canonical_deps = []
        self.__distribution_deps = []
        self.__compensated_deps = []
        self.__distribCls = None
        self.__reverseDisctribDict = None
        self.__solve_dependencies(package, _platform)


    def __str__(self):
        return "canonical->%s\ndistribution->%s\ncompensated->%s"%(str(self.__canonical_deps),
                                                                 str(self.__distribution_deps),
                                                                 str(self.__compensated_deps))

    def packages(self):
        return self.__canonical_deps

    def runtime_distribution_packages(self):
        if( self.__reverseDisctribDict ):
            return [dep for dep  in self.__distribution_deps if self.__reverseDisctribDict[dep][-4:] != "-dev"]
        else:
            return [dep for dep  in self.__distribution_deps if "dev" not in dep]

    def development_distribution_packages(self):
        if( self.__reverseDisctribDict ):
            return [dep for dep  in self.__distribution_deps if self.__reverseDisctribDict[dep][-4:] == "-dev"]
        else:
            return [dep for dep  in self.__distribution_deps if "dev" in dep]

    def egg_packages(self):
        return self.__compensated_deps

    ############################################################
    # Dependency solving and distribution translation follows: #
    ############################################################
    def __solve_dependencies(self, package, _platform=False):
        package_deps = dependencies.canonical_dependencies.get(package, None)
        if not package_deps:
            raise Exception("No such package : " + package)

        if _platform == False:
            _platform = os_factory.Factory.get_platform()
        if _platform == None:
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
                currentPkgChildsList = dependencies.canonical_dependencies.get(currentPkg, None)
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
        self.__distribution_deps = pkgList
        self.__compensated_deps = pkgList

        #de-canonification
        if _platform:
            self.__distribCls = DistributionPackageFactory().create(_platform)
            if self.__distribCls:
                self.__reverseDisctribDict = dict((v,k) for k, v in self.__distribCls.iteritems())
                otherDeps = []
                distribDeps = []
                map(lambda x: otherDeps.append(x) if isinstance(x, EggDependency) else distribDeps.append(x),
                    self.__distribCls.values())
                self.__distribution_deps = distribDeps
                self.__compensated_deps = otherDeps




class DistributionPackageFactory(object):
    __metaclass__ = os_factory.MSingleton
    def __init__(self):
        self.__distPkgs = {}

    def register(self, cls):
        assert isinstance(type(cls), types.TypeType)
        name = cls.__name__
        name = name[:name.find("_PackageNames")].replace("_", " ").lower()
        print "registering:", name
        self.__distPkgs[name] = cls

    def create(self, platform=None, conflictSolve=lambda x: x[0]):
        if platform == None:
            platform = os_factory.Factory.get_platform()

        #We find the right distribution class by intersecting
        #the platform description with the X_X_PackageNames classes
        #whose names are mangled.
        #the correct disctribution class is the one with which the
        #intersection is the largest. If there's equality between two
        #the conflict is solved using the conflictSolve function.
        platform = platform.split(" ")
        maxIntersectionAmount  = 0
        maxIntersectionDistrib = None
        for dist in self.__distPkgs.iterkeys():
            intersections = os_factory.Factory.intersect_platform_names(platform, dist.split(" "))[0]
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

        print "yielding:", maxIntersectionDistrib, "for requested platform:", platform
        cls = self.__distPkgs.get(maxIntersectionDistrib, None)
        if cls: return cls()


class EggDependency(object):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "'EggDependency: " + self.name + "'"

    def __repr__(self):
        return "'EggDependency: " + self.name + "'"

class DistributionPackageNames(dict):
    def __init__(self, **packages):
        dict.__init__(self)
        self.update(packages)
