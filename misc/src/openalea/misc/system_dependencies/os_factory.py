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

import platform, subprocess

__all__=["get_platform"]

class MSingleton(type):
    instances = {}
    def __call__(cls, *args, **kwargs):
        return MSingleton.instances.setdefault(cls, type.__call__(cls, *args, **kwargs))


class BaseOsFactory(object):
    @classmethod
    def get_platform(cls):
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
       """Find intersection between platformName and packageList subdictionnary keys."""
       requestedPlatformNames = set(requestedPlatformNames)
       availablePlatformNames = set(availablePlatformNames)
       return requestedPlatformNames&availablePlatformNames, requestedPlatformNames-availablePlatformNames

    @classmethod
    def intersect_and_solve(cls, platform, candidates, conflictSolve=lambda x: x[0]):
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


get_platform = BaseOsFactory.get_platform


class Factory(BaseOsFactory):
    __metaclass__ = MSingleton

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
    def __init__(self, distIntallerCmd, svnCommand):
        self.__distInstaller = distIntallerCmd
        self.__svnCommand = svnCommand

    def distributionInstallation(self, packages, fake):
        command = "" +  self.__distInstaller
        for i in packages:
            command += " "+i

        if fake:
            print command
        else:
            subprocess.Popen(command.split(" "))



Factory().register("ubuntu", OsInterface("apt-get install", "svn"))
Factory().register("fedora", OsInterface("yum install", "svn"))
