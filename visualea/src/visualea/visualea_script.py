#!/usr/bin/python

# -*- python -*-
#
#       OpenAlea.Visualea: OpenAlea graphical user interface
#
#       Copyright 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#                       Christophe Pradal <christophe.prada@cirad.fr>
#
#       Distributed under the CeCILL v2 License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL_V2-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#

__doc__ = """
Wrapper to start Visualea with correct environment variables
"""

__license__ = "CeCILL v2"
__revision__ =" $Id: visualeagui.py 606 2007-06-25 12:55:41Z dufourko $"




import os, sys


def check_system_setuptools():
    """
    Check system configuration and return environment variables dictionary
    This function need OpenAlea.Deploy
    """

    envv = dict(os.environ)

    try:
        from openalea.deploy import get_all_lib_dirs

        if(("posix" in os.name) and ("linux" in sys.platform.lower())):

            confstr = ':'.join(get_all_lib_dirs('openalea'))
            
            if(not envv.has_key('LD_LIBRARY_PATH')):
                envv['LD_LIBRARY_PATH'] = "%s"%(confstr,)
            else:
                envv['LD_LIBRARY_PATH'] += ":%s"%(confstr,)
                

        elif("win" in sys.platform.lower()):

            confstr = ';'.join(get_all_lib_dirs('openalea'))

            if(not envv.has_key('PATH')):
                envv['PATH'] = "%s"%(confstr,)
            else:
                envv['PATH'] += ";%s"%(confstr,)
                  
    except Exception, e:
        print e

    return envv


def check_system():
    """
    Check system configuration and return environment variables dictionary
    This function need OpenAlea.Config
    """

    envv = dict(os.environ)
        
    if(("posix" in os.name) and ("linux" in sys.platform.lower())):

        try:
            import openalea.config as conf
            
            if(not envv.has_key('LD_LIBRARY_PATH')):
                envv['LD_LIBRARY_PATH'] = "%s"%(conf.lib_dir,)

            elif(not conf.lib_dir in envv['LD_LIBRARY_PATH']):
                envv['LD_LIBRARY_PATH'] += ":%s"%(conf.lib_dir,)
                
        except Exception, e:
            print e

    elif("win" in sys.platform.lower()):

        try:
            import openalea.config as conf
            
            if(not envv.has_key('PATH')):
                envv['PATH'] = "%s"%(conf.lib_dir,)

            elif(not conf.lib_dir in envv['PATH']):
                envv['PATH'] += ";%s"%(conf.lib_dir,)
                  
        except Exception, e:
            print e

    return envv


def start_gui():

    try:
        import openalea.deploy
        envdict = check_system_setuptools()

    except ImportError:
        envdict = check_system()

    if('win' in sys.platform.lower()):
        os.execle(sys.executable, sys.executable, '-c',
                  '"import sys; from openalea.visualea import visualeagui; visualeagui.main(sys.argv)"',
                  envdict)
    else:
        os.execle(sys.executable, sys.executable, '-c',
                  'import sys; from openalea.visualea import visualeagui; visualeagui.main(sys.argv)',
                  envdict)

        

if( __name__ == "__main__"):
    start_gui()
    
