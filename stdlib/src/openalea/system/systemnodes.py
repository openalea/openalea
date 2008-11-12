# -*- python -*-
#
#       OpenAlea.Core 
#
#       Copyright 2006-2007 INRIA - CIRAD - INRA  
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
################################################################################

__doc__="""
System Nodes
"""

__license__= "Cecill-C"
__revision__=" $Id: systemnodes.py 1137 2008-02-01 09:25:46Z dufourko $ "


from openalea.core import *
        

def system_cmd(str_list):
    """ Execute a system command
    Input : a list of string
    Output : subprocess stdout, stderr
    """

    import subprocess

    return subprocess.Popen(str_list, stdout=subprocess.PIPE).communicate()
