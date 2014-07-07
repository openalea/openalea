# -*- coding: utf-8 -*-
# -*- python -*-
#
#       OpenAlea.Core
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA
#
#       File author(s): Christophe Pradal <christophe.prada@cirad.fr>
#                       Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################
"""Setting class retrieve and set user configuration"""

__license__ = "Cecill-C"
__revision__ = " $Id$ "


import os
import sys
import platform
from ConfigParser import SafeConfigParser, NoSectionError, NoOptionError
from openalea.core.singleton import Singleton, ProxySingleton
from openalea.core import logger

# [pkgmanager]
# path = '.', '/home/user/directory'


settingsLogger = logger.get_logger(__name__)


##############################################################################
# Directories functions
##############################################################################


def get_default_home_dir():
    """ Return the home directory (valid on linux and windows) """

    if sys.platform != 'win32':
        return os.path.expanduser('~')

    def valid(path):
        if path and os.path.isdir(path):
            return True
        return False

    def env(name):
        return os.environ.get(name, '')

    homeDir = env('USERPROFILE')
    if not valid(homeDir):
        homeDir = env('HOME')
    elif not valid(homeDir):
        homeDir = '%s%s' % (env('HOMEDRIVE'), env('HOMEPATH'))
    elif not valid(homeDir):
        homeDir = env('SYSTEMDRIVE')
    elif not valid(homeDir):
        homeDir = 'C:\\'

    if homeDir and (not homeDir.endswith('\\')):
        homeDir += '\\'

    return homeDir


def get_openalea_home_dir(name='.openalea'):
    """
    Return the openalea home dirextory
    If it doesn't exist, create it
    """

    home = get_default_home_dir()

    aleahome = os.path.join(home, name)
    if(not os.path.exists(aleahome)):
        os.mkdir(aleahome)

    return aleahome

def get_openalea_tmp_dir(name='.openalea'):
    """
    Return the openalea *temporary project* directory
    If it doesn't exist, create it
    """

    projdir = get_project_dir()
    aleatmp = os.path.join(projdir, 'temp')

    if(not os.path.exists(aleatmp)):
        os.makedirs(aleatmp)

    return aleatmp

def get_project_dir(name='projects'):
    """
    Get default directory (the place where the projects will be created).
    If it doesn't exist, create it
    """

    if platform.system() == 'Linux':
        name2 = '.openalea'
    else:
        name2 = '_openalea'
    aleahome = get_openalea_home_dir(name=name2)
    projecthome = os.path.join(aleahome, name)
    if(not os.path.exists(projecthome)):
        os.mkdir(projecthome)

    return projecthome

def get_userpkg_dir(name='user_pkg'):
    """
    Get user package directory (the place where are the
    wralea.py files).
    If it doesn't exist, create it
    """

    aleahome = get_openalea_home_dir()
    wraleahome = os.path.join(aleahome, name)
    if(not os.path.exists(wraleahome)):
        os.mkdir(wraleahome)

    return wraleahome



####################
# Settings classes #
####################
class Settings(object, SafeConfigParser):
    """ Retrieve and set user configuration """

    __metaclass__ = ProxySingleton
    __notset__ = "NotSet"

    def __init__(self):
        object.__init__(self)
        SafeConfigParser.__init__(self)

        self.__sectionHandlers = {}

        filename = 'openalea.cfg'
        home = get_openalea_home_dir()
        self.configfile = os.path.join(home, filename)

        self.read()

        # the following must be deleted
        if not self.has_section("AutoAddedConfItems"):
            self.add_section("AutoAddedConfItems")

    def __del__(self):
        self.write()

    def read(self):
        """Overriden method to read the configuration
        from Openalea's default configuration file"""
        settingsLogger.debug("Reading configuration file from " + self.configfile)
        SafeConfigParser.read(self, [self.configfile])

    def write(self):
        """Overriden method to write the configuration
        to Openalea's default configuration file"""
        settingsLogger.debug("Writing configuration file to " + self.configfile)
        where = open(self.configfile, "w")
        SafeConfigParser.write(self, where)
        where.close()

    def add_section_update_handler(self, section, handler):
        if section not in self.__sectionHandlers:
            self.__sectionHandlers[section]=handler
        else:
            raise Exception("Section already has handler")

    def add_option(self, section, option, value=__notset__):
        option = option.lower().replace(" ", "_")
        SafeConfigParser.set(self, section, option, value)

    def get(self, section, option):
        option = option.lower().replace(" ", "_")
        return SafeConfigParser.get(self, section, option)

    def set(self, section, option, value):
        """Set the value of an option within a section. Both must exist"""
        if not self.has_section(section):
            self.add_section(section)
            SafeConfigParser.set(self, "AutoAddedConfItems", section, str(True))
        if self.has_option("AutoAddedConfItems", section):
            settingsLogger.warning("Automatic addition of sections will be discarded by the end of the next release cycle (0.10 or 1.0) : " + section)

        # mangle option name:
        option = option.lower().replace(" ", "_")

        longname = section+"."+option
        if not self.has_option(section, option):
            SafeConfigParser.set(self, "AutoAddedConfItems", longname, str(True))
        if self.has_option("AutoAddedConfItems", longname):
            settingsLogger.warning("Automatic addition of options will be discarded by the end of the next release cycle (0.10 or 1.0) : " + longname)
            #raise NoOptionError(option, section)


        SafeConfigParser.set(self, section, option, value)
        handler = self.__sectionHandlers.get(section)
        if handler:
            handler.update_settings(self.items(section))

    exists = SafeConfigParser.has_section

