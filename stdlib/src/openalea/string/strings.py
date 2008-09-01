# -*- python -*-
#
#       OpenAlea.StdLib
#
#       Copyright 2006 - 2008 INRIA - CIRAD - INRA  
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################


__doc__=""" String manipulation """
__license__= "Cecill-C"
__revision__=" $Id$ "

#from openalea.core import *

# File name manipulation

def str_split(string, char):
    """
Split a String
In 0 : a String
In 1 : The split character 
Out :  The splitted string
    """

    return (string.split(char),)


def str_join(list, char):
    """
Join a list
In 0 : A list of String
In 1 : The join character 
Out :  The joinned string
    """

    return (char.join(list),)

def str_strip(string, chars):
    """
    Return a copy of the string with leading and trailing whitespace removed.
    """
    return (string.strip(chars),)

