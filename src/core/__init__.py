from external import *

import os, sys

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



def get_wralea_home_dir(name='wralea'):
    """
    Return the openalea wralea home dirextory
    If it doesn't exist, create it
    """

    aleahome = get_openalea_home_dir()
    wraleahome = os.path.join(aleahome, name)
    if(not os.path.exists(wraleahome)):
        os.mkdir(wraleahome)

    return wraleahome

