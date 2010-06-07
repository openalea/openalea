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

import platform

class MSingleton(type):
    instances = {}
    def __call__(cls, *args, **kwargs):
        return MSingleton.instances.setdefault(cls, type.__call__(cls, *args, **kwargs))

class Factory(object):
    __metaclass__ = MSingleton

    def __init__(self):
        self.__oses = {}

    def create(self, osname):
        return self.__oses[osname]

    def register(self, osname, osinterface):
        self.__oses[osname] = osinterface

    def get_platforms(self):
        return self.__oses.keys()

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

class OsInterface(object):
    def __init__(self, distIntallerCmd, svnCommand):
        self.__distInstaller = distIntallerCmd
        self.__svnCommand = svnCommand

    def distributionInstallation(self, packages):
        for i in packages:
            print self.__distInstaller, i


Factory().register("ubuntu", OsInterface("apt-get install ", "svn"))
Factory().register("fedora", OsInterface("yum install ", "svn"))
