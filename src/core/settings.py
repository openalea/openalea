# -*- python -*-
#
#       OpenAlea.Core: OpenAlea Core
#
#       Copyright or (C) or Copr. 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#                       Christophe Pradal <christophe.prada@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#


__doc__="""
Setting class retrieve and set user configuration
"""

__license__= "Cecill-C"
__revision__=" $Id$ "


import os, sys
from ConfigParser import SafeConfigParser
from singleton import Singleton

# [pkgmanager]
# path = '.', '/home/user/directory'


class Settings(object):
    """ Retrieve and set user configuration """

    __metaclass__ = Singleton

    def __init__(self):
        self.parser = SafeConfigParser()
        
        filename = 'openalea.cfg'
        home = get_openalea_home_dir()
        self.configfile = os.path.join(home,filename)
        
        self.parser.read([self.configfile])


    def write_to_disk(self):
        f = open(self.configfile, 'w')
        self.parser.write(f)
        f.close()


    def get(self, section, option):
        
        return self.parser.get(section, option)

    def set(self, section, option, value):
        if(not self.parser.has_section(section)):
            self.parser.add_section(section)

        self.parser.set(section, option, value)

        


################################################################################
# Directories functions
################################################################################

def get_default_home_dir() :
    
    """ Return the home directory (valid on linux and windows) """
    if sys.platform != 'win32' :
        return os.path.expanduser( '~' )

    def valid(path) :
        if path and os.path.isdir(path) :
            return True
        return False
    
    def env(name) :
        return os.environ.get( name, '' )

    homeDir = env( 'USERPROFILE' )
    if not valid(homeDir) :
        homeDir = env( 'HOME' )
    elif not valid(homeDir) :
        homeDir = '%s%s' % (env('HOMEDRIVE'),env('HOMEPATH'))
    elif not valid(homeDir) :
        homeDir = env( 'SYSTEMDRIVE' )
    elif not valid(homeDir) :
        homeDir = 'C:\\'

    if homeDir and (not homeDir.endswith('\\')) :
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



def get_userpkg_dir(name='wralea'):
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

