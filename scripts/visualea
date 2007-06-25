#!/usr/bin/python

import os, sys
import subprocess

def check_system():
    """ Check system configuration and return environment variables dictionary"""
    
    if("posix" in os.name):

        envv = dict(os.environ)
        try:
            import openalea.config as conf
            
            if(not envv.has_key('LD_LIBRARY_PATH')):
                envv['LD_LIBRARY_PATH'] = "%s"%(conf.lib_dir,)

            elif (not conf.lib_dir in envv['LD_LIBRARY_PATH']) :
                  envv['LD_LIBRARY_PATH'] += ":%s"%(conf.lib_dir,)
                  
        except Exception, e:
            print e

        return envv


if( __name__ == "__main__"):
    envdict = check_system()
    prog_name = os.path.basename(sys.executable)
    
    os.execle(sys.executable, sys.executable, '-c', 'import sys; from openalea.visualea import visualeagui; visualeagui.main(sys.argv)', envdict)

