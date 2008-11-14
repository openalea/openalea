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


__doc__=""" Data Nodes """
__license__= "Cecill-C"
__revision__=" $Id: $ "

from os.path import join
from openalea.core import *


def py_set(list_elt):
    '''
    Build an unordered sequence of unique element.
    '''
    return (set(list_elt),)

def py_clear(set_):
    '''
    Remove all elements from this set.
    '''
    set1 = set_.copy()
    set1.clear()
    return (set1, )

def py_add(set_, elt):
    ''' Add an element to a set. '''
    set_.add(elt)
    return (set_,)

def py_difference(set1, set2):
    ''' Return the difference of two sets as a new sets. '''
    return (set1.difference(set2),)

def py_intersection(set1, set2):
    ''' Return the intersection of two sets as a new sets. '''
    return set1.intersection(set2),

def py_issubset(set1, set2):
    ''' Report whether another set contains this set. '''
    return set1.issubset(set2), 

def py_issuperset(set1, set2):
    ''' Report whether this set contains another set. '''
    return set1.issuperset(set2), 

def py_symmetric_difference(set1, set2):
    ''' Return the symmetric difference of two sets as a new set. '''
    return set1.symmetric_difference(set2), 

def py_union(set1, set2):
    ''' Return the union of two sets as a new set. '''
    return set1.union(set2), 

def py_update(set1, set2):
    ''' Update a set with the union of set1 and set2. '''
    set_ = set1.copy()
    set_.update(set2),
    return set_,
