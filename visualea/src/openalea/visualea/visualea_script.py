#!/usr/bin/python

# -*- python -*-
#
#       OpenAlea.Visualea: OpenAlea graphical user interface
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA  
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
################################################################################
"""Wrapper to start Visualea with correct environment variables"""

__license__ = "CeCILL v2"
__revision__ = " $Id$"

import os, sys


def check_system_setuptools():
    """
    Check system configuration and return environment variables dictionary
    This function need OpenAlea.Deploy
    """

    from openalea.deploy import check_system
    envv = dict(os.environ)
    res = check_system()
    envv.update(res)

    return envv



def start_gui():
    """todo"""
    try:
        envdict = check_system_setuptools()

    except Exception, e:
        envdict = os.environ
        print e

    if sys.platform.lower().startswith('win'):
        os.execle(sys.executable, sys.executable, "-c", 
                  '"import sys; from openalea.visualea import visualeagui;sys.argv+='+str(sys.argv)+';visualeagui.main(sys.argv)"',
                  envdict)
    else:
        os.execle(sys.executable, sys.executable, "-c",
                  'import sys; from openalea.visualea import visualeagui;sys.argv+='+str(sys.argv)+';visualeagui.main(sys.argv)',
                  envdict)
        
        
        
if( __name__ == "__main__"):
    start_gui()
    
