# -*- python -*-
# -*- coding: utf-8 -*-
#
#       IdGenerator : graph package
#
#       Copyright  or Copr. 2006 - 2011 INRIA - CIRAD - INRA
#
#       File author(s): Jerome Chopard <jerome.chopard@sophia.inria.fr>
#                       Fred Theveny <theveny@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       VPlants WebSite : https://gforge.inria.fr/projects/vplants/
################################################################################

__doc__="""
This module provide a generator for id numbers
"""

__license__= "Cecill-C"
__revision__=" $Id: id_generator.py 9206 2010-07-02 01:12:52Z agpr $ "

class IdMaxGenerator(object) :
    def __init__ (self) :
        self._id_max = 0

    def get_id (self, id = None) :
        if id is None :
            ret = self._id_max
            self._id_max += 1
            return ret
        else :
            if id < self._id_max :
                raise IndexError("id %d already used" % id)
            self._id_max = max(self._id_max,id+1)
            return id

    def release_id (self, id) :
        pass

    def clear (self) :
        """ Reset the generator.
        """
        self._id_max = 0

class IdSetGenerator(object) :
    def __init__ (self) :
        self._id_max = 0
        self._available_ids = set()

    def get_id (self, id = None) :
        if id is None :
            if len(self._available_ids) == 0 :
                ret = self._id_max
                self._id_max += 1
                return ret
            else :
                return self._available_ids.pop()
        else :
            if id >= self._id_max :
                self._available_ids.update(xrange(self._id_max,id))
                self._id_max = id+1
                return id
            else :
                try :
                    self._available_ids.remove(id)
                    return id
                except KeyError :
                    raise IndexError("id %d already used" % id)

    def release_id (self, id) :
        if id > self._id_max :
            raise IndexError("id out of range")
        elif id in self._available_ids :
            raise IndexError("id already not used")
        else :
            self._available_ids.add(id)

    def clear (self) :
        """ Reset the generator.
        """
        self._id_max = 0
        self._available_ids = set()

class IdGenerator (IdSetGenerator) :
    pass

class IdListGenerator(object) :
    def __init__ (self) :
        self._id_max=0
        self._id_list=[]

    def get_id (self, id=None) :
        if id is None :
            if len(self._id_list)==0 :
                ret=self._id_max
                self._id_max+=1
                return ret
            else :
                return self._id_list.pop()
        else :
            if id>=self._id_max :
                self._id_list.extend(range(self._id_max,id))
                self._id_max=id+1
                return id
            else :
                try :
                    ind=self._id_list.index(id)
                    del self._id_list[ind]
                    return id
                except ValueError :
                    raise IndexError("id %d already used" % id)

    def release_id (self, id) :
        if id>self._id_max :
            raise IndexError("id out of range")
        elif id in self._id_list :
            raise IndexError("id already not used")
        else :
            self._id_list.append(id)

    def clear (self) :
        self._id_max=0
        self._id_list=[]
