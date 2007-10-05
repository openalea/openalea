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


def position_mapping( objList = [], pts_distrib = [] ):
  assert len(objList) == len(pts_distrib)
  
  for i in range( len( objList ) ) :
    ojb[i].x = pts_distrib[i][0]
    ojb[i].y = pts_distrib[i][1]

  return objList

def best_position_mapping( objList = [], pts_distrib = [] ):
  pass

def best_position_mapping_with_radius_deform( objList = [], pts_distrib = [] ):
  pass

def gibbs( objList = [], pts_distrib = [] ):
  pass

def stand_positioner( objList = [], pts_distrib = [], type='Position mapping', params = None):
  if type == 'Position mapping (PM)':
    return (position_mapping(objList, pts_distrib), )
  elif type == 'Best PM':
    print 'Best Position mapping not implemented'
  elif type == 'Best PM with radius deformation':
    print 'Best PM with radius deformation not implemented'
  elif type == 'Gibbs':
    print 'Gibbs not implemented'

  
