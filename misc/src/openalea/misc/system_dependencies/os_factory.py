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

import platform, subprocess, abc, collections

__all__=["get_platform"]

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


get_platform = BaseOsFactory.get_platform #: a shortcut for  BaseOsFactory.get_platform


class OsFactory(BaseOsFactory):
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
        command = self.__distInstaller[:]
        command += " "+ package

        if fake:
            print command
        else:
            subprocess.Popen(command.split(" "))




OsFactory().register("ubuntu", OsInterface("apt-get install", "svn"))
OsFactory().register("fedora", OsInterface("yum install", "svn"))
