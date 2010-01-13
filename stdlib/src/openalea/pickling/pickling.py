# -*- python -*-
#
#       OpenAlea.StdLib
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA  
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################
""" Python Nodes """


__license__ = "Cecill-C"
__revision__ = " $Id$"

from openalea.core import *
import cPickle

def py_load( file_path ):
  f = open( file_path, 'r' )
  data = []
  try:
    while(1):
      data.append(cPickle.load(f))

  except EOFError :
      f.close()

  if len(data) > 1:
    return data,
  else:
    return data[0],

def py_dump( data, file_path, append=False ):
  if append :
    f = open( file_path, 'a' )
  else:
    f = open( file_path, 'w' )

  cPickle.dump( data, f )
  f.close()

