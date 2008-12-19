# -*- python -*-
#
#       OpenAlea.StdLib
#
#       Copyright 2006 - 2008 INRIA - CIRAD - INRA
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
    Helper function. Test if a given 2D point is inside any cluster centered on
    points from `ctr` list with `d` as radius.

    :param x: x-axis point value
    :param y: y-axis point value
    :param xctr: list of center coordinates as [(x1,y1) .. (xn,yn)]
    :param yctr: list of center coordinates as [(x1,y1) .. (xn,yn)]
    :param d: cluster radius

    :type x: float
    :type y: float
    :type xctr: cople list
    :type yctr: cople list
    :type d: float

    :returns: True if the point is inside a cluster, False otherwise
    :rtype: boolean
    """
    if len(xctr)==0:
        return True

    for i in range(len(xctr)):
        if((x-xctr[i])**2 + (y-yctr[i])**2 <= d**2):
            return True
    return False


def _randomRange(min, max):
    """
    Helper function. Generate a random number within a given range.

    :param min: low bound of the range
    :param max: high bound of the range

    :type min: float
    :type max: float

    :returns: random value between `min` and `max`
    :rtype: float

    """
    return min + random.random() * (max - min)


def _minDistPtClstr(x, y, ptX, ptY):
    """
    Helper function. Compute the minimal distance between a given point and
    the ones represented by in the `ptX` and `ptY` lists.

    :param x: x-axis point value
    :param y: y-axis point value
    :param ptX: list of X coordinates
    :param ptY: list of Y coordinates

    :type x:float
    :type y:float
    :type ptX:float
    :type ptY:float

    :returns: The minimal distance between (x,y) and a list of points
    :rtype: float

    """
    if len(ptX)==0:
        return 1000000.0

    dmin = (x-ptX[0])**2 + (y-ptY[0])**2
    for i in range(len(ptX)):
        dtmp = (x-ptX[i])**2 + (y-ptY[i])**2
        if(dtmp <= dmin**2):
            dmin = dtmp
    return sqrt(dmin)


def _linearProba(dtest, d):
    """
    Helper function. Simulate a linear probability from 0 (proba=0) to
    d (proba=1). And test wether the `dtest` value with proba=
    `dtest`/`d` is kept.

    :Note: All points with `dtest` > `d` will automatically be kept

    :param dtest: value to test against `d`
    :param d: limit value above wich all values are ok

    :type dtest: float
    :type d: float

    :return: True if the value is kept
    :rtype: boolean

    """
    if random.random() <= 1.0*dtest/d:
        return True
    else:
        return False


def random_distrib(n=100, xr=(0, 1), yr=(0, 1)):
    assert(xr[0] < xr[1] and yr[0] < yr[1] and
        " min value must be lesser than max")
    x_range = xr
    y_range = yr

    x = [_randomRange(x_range[0], x_range[1]) for i in range(n)]
    y = [_randomRange(y_range[0], y_range[1]) for i in range(n)]

    return (x, y)


def regular_distrib(n =100, xr=(0, 1), yr=(0, 1)):
    """
    Simulation d'une realisation du processus regulier correspondant a une
    proba lineaire fonction du rayon caracterisant l'espace disponible par
    point

    :param n: the number of random points to be generated
    :param xr: the x range, default is [0,1]
    :param yr: the y range, default is [0,1]

    :type n: int
    :type xr: tuple
    :type yr: tuple

    :returns: two lists representing coordinates
    :rtype: list

    """
    assert (xr[0] < xr[1] and yr[0] < yr[1] and
        " min value must be lesser than max")
    x_range = xr
    y_range = yr

    dist = sqrt((xr[1]-xr[0])*(yr[1]-yr[0]))
    ptX = []
    ptY = []
    NbTry = 0 #count the number of try allowed to find a type2 point

    while(len(ptX) < n and NbTry < 100):

        xtmp = _randomRange(x_range[0], x_range[1])
        ytmp = _randomRange(y_range[0], y_range[1])
        NbTry += 1
        min_dist = _minDistPtClstr(xtmp, ytmp, ptX, ptY)

        if _linearProba(min_dist, dist):
            ptX.append(xtmp)
            ptY.append(ytmp)
            NbTry = 0

    if NbTry >= 100:
        print "Impossible to get all Type2 points with required parameters"

    return (ptX, ptY)


def neman_scott__distrib(n=100, xr=(0, 1), yr=(0, 1), **kwds):
    """
    simulation d'une realisation du processus de type Neman Scott
    (Nb Agregats, Rayon Agregats)
    """

    assert (xr[0] < xr[1] and yr[0] < yr[1] and
        " min value must be lesser than max")
    x_range = xr
    y_range = yr

    nb_cluster = kwds.get('cluster', 5)
    cl_radius = kwds.get('cluster_radius', 0.1)

    x_cl, y_cl = random_distrib(nb_cluster, x_range, y_range)
    ptX = []
    ptY = []

    while(len(ptX) < n):
        xtmp = _randomRange(x_range[0], x_range[1])
        ytmp = _randomRange(y_range[0], y_range[1])

        if _testDistance(xtmp, ytmp, x_cl, y_cl, cl_radius):
            ptX.append(xtmp)
            ptY.append(ytmp)

    return (ptX, ptY)


def gibbs_distrib(n=10, xr=(0, 1), yr=(0, 1)):
    pass


def spatial_distrib(n=100, xrange=(0, 1), yrange=(0, 1), type='Random',
        params=None):
    if type=='Random':
        return random_distrib(n, xrange, yrange)
    elif type=='Regular':
        return regular_distrib(n, xrange, yrange)
    elif type=='Neman Scott':
        return neman_scott__distrib(n, xrange, yrange, **params)
    elif type=='Gibbs':
        pass


def domain(xmin, xmax, ymin, ymax, scale):
    return ((xmin*scale, xmax*scale), (ymin*scale, ymax*scale)),


def random_distribution(n=10):
    x = [random.random() for i in range(n)]
    y = [random.random() for i in range(n)]
    return x, y


def regular_distribution(n=10):
    dist = 1./n
    ptX = []
    ptY = []
    NbTry = 0 #count the number of try allowed to find a type2 point

    while(len(ptX) < n and NbTry < 100):

        xtmp = random.random()
        ytmp = random.random()
        NbTry += 1
        min_dist = _minDistPtClstr(xtmp, ytmp, ptX, ptY)

        if _linearProba(min_dist, dist):
            ptX.append(xtmp)
            ptY.append(ytmp)
            NbTry = 0

    if NbTry >= 100:
        print "Impossible to get all Type2 points with required parameters"

    return ptX, ptY


class basic_distrib(Node):
    """
    Basic distribution(type) -> distribution func
    :input: Type of the function.
    :output: function that generates distribution.
    """

    distr_func = {"Random": random_distribution,
                  "Regular": regular_distribution, }

    def __init__(self):

        Node.__init__(self)

        funs= self.distr_func.keys()
        funs.sort()
        self.add_input(name="Type", interface=IEnumStr(funs), value=funs[0])
        self.add_output(name="Distribution", interface=None)

    def __call__(self, inputs):
        func_name= self.get_input("Type")
        f = self.distr_func[func_name]
        self.set_caption(func_name)

        return f


def neman_scott__distribution(n=10, cl_nbr=2, cl_radius=0.2):
    """
    simulation d'une realisation du processus de type Neman Scott
    (Nb Agregats, Rayon Agregats)
    """

    x_cl, y_cl = random_distrib(cl_nbr)
    ptX = []
    ptY =[]

    while(len(ptX) < n):
        xtmp = random.random()
        ytmp = random.random()

        if _testDistance(xtmp, ytmp, x_cl, y_cl, cl_radius):
            ptX.append(xtmp)
            ptY.append(ytmp)

    return ptX, ptY


class aggregative_distrib(Node):
    """
    Basic distribution(type) -> distribution func

    .. :param input: Type of the function.
    .. :param output: function that generates distribution.

    """

    distr_func= {"NemanScott": neman_scott__distribution, }

    def __init__(self):

        Node.__init__(self)

        funs= self.distr_func.keys()
        funs.sort()
        self.add_input(name="Type", interface=IEnumStr(funs), value=funs[0])
        self.add_input(name="Cluster number", interface=IInt(min=1), value=2)
        self.add_input(name="Cluster radius", interface=IFloat(0.01, 1, 0.01),
            value=0.2)
        self.add_output(name="Distribution", interface=None)

    def __call__(self, inputs):
        func_name= self.get_input("Type")
        cluster_nb = self.get_input("Cluster number")
        cluster_rd= self.get_input("Cluster radius")
        f = self.distr_func[func_name]
        self.set_caption(func_name)

        return lambda n: neman_scott__distribution(n, cluster_nb, cluster_rd)


def scale(seq, min, max):
    mm = max-min
    return [min+x*mm for x in seq]


def random2D(n, distrib_func, domain):
    if not distrib_func:
        return

    x, y = distrib_func(n)

    if domain:
        (xmin, xmax), (ymin, ymax) = domain
        x = scale(x, xmin, xmax)
        y = scale(y, ymin, ymax)

    return x, y
