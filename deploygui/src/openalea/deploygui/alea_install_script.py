#!/usr/bin/python

# -*- python -*-
#
#       OpenAlea.DeployGui: OpenAlea installation frontend
#
#       Copyright 2006-2007 INRIA - CIRAD - INRA  
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
"""Main Module for installation graphical frontend"""

__license__ = "CeCILL v2"
__revision__ = " $Id:  $"
url =  "http://openalea.gforge.inria.fr"

import sys, os



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


def main(args=None):
    """
    Start the GUI to install packages.
    If the GUI use QT and a new version of QT has been installed, we need to start a new process
    which setup the environment (shared libs and so on).

    On darwin, for instance, the sudo command do not propagate the environment variables.
    So to update the env variables dynamically, we restart a new python process with the OpenAlea environment.
    """
    if args is None:
        args = []
    #status = main_app(args)

    envdict = check_system_setuptools()

    if sys.platform.lower().startswith('win'):
        status = os.execle(sys.executable, sys.executable, "-c", 
                  '"import sys; from openalea.deploygui import alea_install_gui;sys.argv="'+str(args)+'";alea_install_gui.main_app(sys.argv)"',
                  envdict)
    else:
        status = os.execle(sys.executable, sys.executable, "-c",
                  'import sys; from openalea.deploygui import alea_install_gui;sys.argv='+str(args)+';alea_install_gui.main_app(sys.argv)',
                  envdict)


    print "Update environment"

    if sys.platform.lower().startswith('win'):
        os.execl(sys.executable, sys.executable, '-c',
                  '"from openalea.deploy.command import set_env; set_env()"')
    else:
        os.execl(sys.executable, sys.executable, '-c',
                  'from openalea.deploy.command import set_env; set_env()')

    return status

if __name__ == "__main__":
    main(sys.argv)
    
