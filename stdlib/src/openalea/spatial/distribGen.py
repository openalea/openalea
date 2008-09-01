# -*- python -*-
#
#       OpenAlea.Core.Library: OpenAlea Core Library module
#
#       Copyright 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Da SILVA David <david.da_silva@cirad.fr>
#                       BOUDON Frederic <frederic.boudon@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#


from openalea.core import *
#from scipy import stats
import random
from math import sqrt

def _testDistance(x, y, xctr, yctr, d):
  """
  Helper function. Test if a given 2D point is inside any cluster centered on points from `ctr` list with `d` as radius.

  :Parameters:
    - `x` : x-axis point value
    - `y` : y-axis point value
    - `ctr` : list of center coordinates as [(x1,y1) .. (xn,yn)]
    - `d` : cluster radius

  :Types:
    - `x` : float
    - `y` : float
    - `ctr` : cople list
    - `d` : float

  :returns: True if the point is inside a cluster, False otherwise
  :returntype: boolean

  """
  if len( xctr ) == 0 :
    return True

  for i in range( len(xctr) ):
    if( (x-xctr[i])**2 + (y-yctr[i])**2 <= d**2 ):
      return True
  return False

def _randomRange(min, max):
  """
  Helper function. Generate a random number within a given range.

  :Parameters:
    - `min` : low bound of the range
    - `max` : hight bound of the range

  :Types:
    - `min` : float
    - `max` : float

  :returns: random value between `min` and `max`
  :returntype: float

  """
  return min + random.random() * ( max - min )

def _minDistPtClstr(x, y, ptX, ptY):
  """
  Helper function. Compute the minimal distance between a given point and the ones represented by in the `ptX` and `ptY` lists.

  :Parameters:
    - `x` : x-axis point value
    - `y` : y-axis point value
    - `ptX` : list of X coordinates
    - `ptY` : list of Y coordinates

  :Types:
    - `x` : float
    - `y` : float
    - `ptX` : list
    - `ptY` : list

  :returns: The minimal distance between (x,y) and a list of points
  :returntype: float

  """
  if len( ptX ) == 0 :
    return 1000000.0

  dmin = (x-ptX[0])**2 + (y-ptY[0])**2
  for i in range( len(ptX) ):
    dtmp = (x-ptX[i])**2 + (y-ptY[i])**2
    if( dtmp <= dmin**2 ):
      dmin = dtmp
  return sqrt(dmin)

def _linearProba(dtest, d):
  """
  Helper function. Simulate a linear probability from 0 (proba=0) to d (proba=1). And test wether the `dtest` value with proba = `dtest`/`d` is kept. 

  :Note: All points with `dtest` > `d` will automatically be kept

  :Parameters:
    - `dtest` : value to test against `d`
    - `d` : limit value above wich all values are ok

  :Types:
    - `dtest` : float
    - `d` : float

  :return: True if the value is kept
  :returntype: boolean

  """
  if random.random() <= 1.0*dtest/d :
    return True
  else : 
    return False


def random_distrib( n = 100, xr = (0,1), yr = (0,1) ):
  assert ( xr[0] < xr[1] and yr[0] < yr[1] and " min value must be lesser than max" )
  x_range = xr
  y_range = yr

  x = [ _randomRange( x_range[0], x_range[1]) for i in range(n) ]
  y = [ _randomRange( y_range[0], y_range[1]) for i in range(n) ]

  return ( x, y ) 



def regular_distrib( n = 100, xr = (0,1), yr = (0,1) ):
  """
  Simulation d'une realisation du processus regulier correspondant a une proba lineaire fonction du rayon caracterisant l'espace disponible par point

  :Parameters:
    - `n` : the number of random points to be generated
    - `xr` : the x range, default is [0,1]
    - `yr` : the y range, default is [0,1]

  :Types:
    - `n` : int
    - `xr` : tuple
    - `yr` : tuple

  :returns: two lists representing coordinates
  :returntype: list

  """
  assert ( xr[0] < xr[1] and yr[0] < yr[1] and " min value must be lesser than max" )
  x_range = xr
  y_range = yr

  dist = sqrt( (xr[1]-xr[0])*(yr[1]-yr[0]) )
  ptX = []
  ptY = []
  NbTry = 0 #count the number of try allowed to find a type2 point

  while( len( ptX ) < n and NbTry < 100 ):

    xtmp = _randomRange( x_range[0], x_range[1] )
    ytmp = _randomRange( y_range[0], y_range[1] )
    NbTry += 1
    min_dist = _minDistPtClstr( xtmp, ytmp, ptX, ptY)

    if _linearProba(min_dist, dist) :
      ptX.append(xtmp)
      ptY.append(ytmp)
      NbTry = 0

  if NbTry >= 100:
    print "Impossible to get all Type2 points with required parameters"
  
  return (ptX, ptY)


def neman_scott__distrib( n = 100, xr = (0,1), yr = (0,1), **kwds ):
  """
  simulation d'une realisation du processus de type Neman Scott (Nb Agregats, Rayon Agregats)
  """

  assert ( xr[0] < xr[1] and yr[0] < yr[1] and " min value must be lesser than max" )
  x_range = xr
  y_range = yr

  nb_cluster = kwds.get( 'cluster', 5)
  cl_radius = kwds.get( 'cluster_radius', 0.1)

  x_cl, y_cl = random_distrib( nb_cluster, x_range, y_range )
  ptX = []
  ptY =[]

  while( len(ptX) < n ):
    xtmp = _randomRange( x_range[0], x_range[1] )
    ytmp = _randomRange( y_range[0], y_range[1] )
    
    if _testDistance(xtmp, ytmp, x_cl, y_cl, cl_radius):
      ptX.append( xtmp )
      ptY.append( ytmp )
  
  return (ptX, ptY)


def gibbs_distrib( n = 10, xr = (0,1), yr = (0,1) ):
  pass



def spatial_distrib( n=100, xrange=(0,1), yrange=(0,1), type='Random', params = None):
  if type == 'Random':
    return random_distrib( n, xrange, yrange)
  elif type == 'Regular':
    return regular_distrib( n, xrange, yrange)
  elif type == 'Neman Scott':
    return neman_scott__distrib( n, xrange, yrange, **params)
  elif type == 'Gibbs':
    pass
    
#======================================================================#

def domain(xmin, xmax, ymin, ymax, scale):
  return ((xmin*scale, xmax*scale), (ymin*scale, ymax*scale)),
  
def random_distribution(n =10):
  x = [ random.random() for i in range(n) ]
  y = [ random.random() for i in range(n) ]
  return x, y

def regular_distribution(n=10):
  dist = 1./n
  ptX = []
  ptY = []
  NbTry = 0 #count the number of try allowed to find a type2 point

  while( len( ptX ) < n and NbTry < 100 ):

    xtmp = random.random()
    ytmp = random.random()
    NbTry += 1
    min_dist = _minDistPtClstr( xtmp, ytmp, ptX, ptY)

    if _linearProba(min_dist, dist) :
      ptX.append(xtmp)
      ptY.append(ytmp)
      NbTry = 0

  if NbTry >= 100:
    print "Impossible to get all Type2 points with required parameters"
  
  return ptX, ptY

class basic_distrib( Node ):
    """
    Basic distribution(type) -> distribution func
    Input:
        Type of the function.
    Output:
        function that generates distribution.
    """
    
    distr_func= { "Random" : random_distribution,
                  "Regular" : regular_distribution,
              } 
    
    def __init__(self):
    
        Node.__init__(self)

        funs= self.distr_func.keys()
        funs.sort()
        self.add_input( name = "Type", interface = IEnumStr(funs), value = funs[0]) 
        self.add_output( name = "Distribution", interface = None)

    def __call__(self, inputs):
        func_name= self.get_input("Type")
        f = self.distr_func[func_name]
        self.set_caption(func_name)

        return f

def neman_scott__distribution( n =10, cl_nbr = 2, cl_radius = 0.2 ):
  """
  simulation d'une realisation du processus de type Neman Scott (Nb Agregats, Rayon Agregats)
  """

  x_cl, y_cl = random_distrib( cl_nbr )
  ptX = []
  ptY =[]

  while( len(ptX) < n ):
    xtmp = random.random()
    ytmp = random.random()
    
    if _testDistance(xtmp, ytmp, x_cl, y_cl, cl_radius):
      ptX.append( xtmp )
      ptY.append( ytmp )
  
  return ptX, ptY


class aggregative_distrib( Node ):
    """
    Basic distribution(type) -> distribution func
    Input:
        Type of the function.
    Output:
        function that generates distribution.
    """
    
    distr_func= { "NemanScott" : neman_scott__distribution,
                } 
    
    def __init__(self):
    
        Node.__init__(self)

        funs= self.distr_func.keys()
        funs.sort()
        self.add_input( name = "Type", interface = IEnumStr(funs), value = funs[0]) 
        self.add_input( name = "Cluster number", interface = IInt(min=1), value = 2) 
        self.add_input( name = "Cluster radius", interface = IFloat(0.01, 1, 0.01), value = 0.2) 
        self.add_output( name = "Distribution", interface = None)

    def __call__(self, inputs):
        func_name= self.get_input("Type")
        cluster_nb = self.get_input("Cluster number")
        cluster_rd= self.get_input("Cluster radius")
        f = self.distr_func[func_name]
        self.set_caption(func_name)

        return lambda n : neman_scott__distribution(n, cluster_nb, cluster_rd)


def scale (seq, min, max):
  mm = max-min
  return [ min+x*mm for x in seq] 

def random2D(n , distrib_func, domain):
  if not distrib_func:
    return

  x, y = distrib_func(n)
  
  if domain:
    (xmin, xmax), (ymin, ymax) = domain
    x = scale(x, xmin, xmax)
    y = scale(y, ymin, ymax)
  
  return x,y

  
  
  
