# -*- python -*-
#
#       OpenAlea.Core 
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
################################################################################
"""System Nodes"""

__license__ = "Cecill-C"
__revision__ = " $Id$ "

from openalea.core import *
from tempfile import TemporaryFile

def system_cmd(str_list):
    """ Execute a system command
    Input : a list of string
    Output : subprocess stdout, stderr
    """

    import subprocess

    return subprocess.Popen(str_list, stdout=subprocess.PIPE).communicate()

def shell_command(cmd, directory):
    """ Execute a command in a shell
    cmd : the command as a string
    dir : the directory where the cmd is executed
    Output : status
    """
    from subprocess import Popen,STDOUT, PIPE

    
    output_stream = TemporaryFile(mode='r+w+b')
    p = Popen(cmd, shell=True, cwd=directory,
        stdin=PIPE, stdout=output_stream, stderr=STDOUT)
    status = p.wait()

    output_stream.seek(0)
    s= output_stream.read()
    output_stream.close()
    return status,s

