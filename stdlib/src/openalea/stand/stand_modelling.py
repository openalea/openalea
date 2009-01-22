# -*- python -*-
#
#       OpenAlea.Core.Library: OpenAlea Core Library module
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA  
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


#------------ Associating spatial distribution ------------------#

def position_mapping( objList = [], ptX = [], ptY =[] ):
  assert ( len(objList) == len(ptX) and len(objList) == len(ptY) and "coordinates and objects should have the same length" ) 
  
  for i in range( len( objList ) ) :
    objList[i].posX = ptX[i]
    objList[i].posY = ptY[i]

  return (objList, )

def best_position_mapping( objList = [], pts_distrib = [] ):
  pass

def best_position_mapping_with_radius_deform( objList = [], pts_distrib = [] ):
  pass

def gibbs( objList = [], pts_distrib = [] ):
  pass

def stand_positioner( objList = [], ptX = [], ptY = [], type='Position mapping (PM)', params = None):
  if type == 'Position mapping (PM)':
    return position_mapping(objList, ptX, ptY)
  elif type == 'Best PM':
    print 'Best Position mapping not implemented'
  elif type == 'Best PM with radius deformation':
    print 'Best PM with radius deformation not implemented'
  elif type == 'Gibbs':
    print 'Gibbs not implemented'


#---------------- Associating geometry --------------------------#

def stand_dresser(objList = [], dresser = None) :
  scene =[]
  if dresser != None :
    for obj in objList :
      shList = dresser.__call__(obj)
      for sh in shList :
        scene.append(sh)
  else :
    raise "No Dresser"
  return (scene, )
