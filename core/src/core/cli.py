# -*- python -*-
#
#       OpenAlea.Core: OpenAlea Core
#
#       Copyright 2006 INRIA - CIRAD - INRA  
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

__doc__="""
This module defines the command line interface.
It is composed by a set of functions useable directly in the interpreter
"""

__license__= "Cecill-C"
__revision__=" $Id$ "


def init_interpreter(interpreter, session):
    """
    Initialise the interpreter to interact with the openalea system
    (import, variables...)
    """
    interpreter.runsource("from openalea.core.cli import *")
    interpreter.locals['session'] = session
    interpreter.locals['pmanager'] = session.pkgmanager
    interpreter.locals['datapool'] = session.datapool

def get_welcome_msg():
    """ Return a welcome message """

    return " session = Session instance.\n"+\
           " pmanager = PackageManager instance.\n"+\
           " datapool = DataPool instance."



   

    
