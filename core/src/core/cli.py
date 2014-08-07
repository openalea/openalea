# -*- python -*-
#
#       OpenAlea.Core: OpenAlea Core
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA
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
###############################################################################
"""This module defines the command line interface.
It is composed by a set of functions useable directly in the interpreter
"""

__license__ = "Cecill-C"
__revision__ = " $Id$ "


def init_interpreter(interpreter, session, _locals=None):
    """
    Initialise the interpreter to interact with the openalea system
    (import, variables...)
    """
    # try: interpreter.runsource("from openalea.core.cli import *", hidden=True)
    # except: interpreter.runsource("from openalea.core.cli import *")
    interpreter.locals['session'] = session
    interpreter.locals['pmanager'] = session.pkgmanager
    interpreter.locals['datapool'] = session.datapool
    if(_locals):
        interpreter.locals.update(_locals)


def get_welcome_msg():
    """ Return a welcome message """

    return " session = Session instance.\n"+\
           " pmanager = PackageManager instance.\n"+\
           " datapool = DataPool instance."


def get_datapool_code(data_key):
    """ Return the python code to access to 'data_key' in the datapool """

    return "%s = datapool['%s']" % (data_key, data_key )


def get_node_code(node_id):
    """ Return the python code to access to 'node_id' """

    return "session.ws.actor(%i)" % (node_id, )
