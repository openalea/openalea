# -*- python -*-
#
#       OpenAlea.Core.Library: OpenAlea Core Library module
#
#       Copyright 2006 INRIA - CIRAD - INRA  
#
#       File author(s): BOUDON Frederic <frederic.boudon@cirad.fr>
#                       Da SILVA David <david.da_silva@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#


from openalea.core import *
from scipy import stats
import random


def random_distrib( n = 10, xr = (0,1), yr = (0,1) ):
  x_range = xr
  y_range = xr

  x = [ random.uniform( x_range[0], x_range[1]) for i in range(n) ]
  y = [ random.uniform( y_range[0], y_range[1]) for i in range(n) ]

  return [ (x[i],y[i]) for i in range(n) ]

def regular_distrib( n = 10, xr = (0,1), yr = (0,1) ):
  pass

def neman_scott__distrib( n = 10, xr = (0,1), yr = (0,1) ):
  pass

def gibbs_distrib( n = 10, xr = (0,1), yr = (0,1) ):
  pass


def spatial_distrib( n=10, xrange=(0,1), yrange=(0,1), type='Random', params = None):
  if type == 'Random':
    return (random_distrib( n, xrange, yrange),)
  elif type == 'Regular':
    print 'regular not implemented'
  elif type == 'Neman Scott':
    print 'Neman Scott not implemented'
  elif type == 'Gibbs':
    print 'Gibbs not implemented'

  
