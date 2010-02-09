# -*- python -*-
#
#       OpenAlea.Core
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA
#
#       File author(s): Daniel Barbeau <daniel.barbeau@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

__license__ = "Cecill-C"
__revision__ = " $Id$ "


from openalea.core import observer
import types

class MetaDataDict(observer.Observed):
    """Attach meta data of a graphical representation
    of a graph component. This metadata can be 
    used to customize the appearance of the node."""
    def __init__(self, slots=None):
        observer.Observed.__init__(self)
        self._metaValues = {}
        self._metaTypes = {}

        if(slots):
            if( isinstance(slots, self.__class__) ):
                self.update(slots)
            else:
                for name, value in slots.iteritems():
                    if (isinstance(value, tuple) or isinstance(value, list)) and \
                       len(value) == 2  and isinstance(value[0],type):

                        typ, val = value
                    else:
                        typ =  type(value) if value is not None else None
                        val = value
                    self.add_metadata(name, typ )
                    self.set_metadata(name, val)
                    
    def update(self, other):
        self._metaValues = other._metaValues.copy()
        self._metaTypes = other._metaTypes.copy()    

    def __repr__(self):
        if(not len(self._metaValues)): return "{}"
        keys = set(self._metaTypes)-set(self._metaValues)
        d = self._metaValues.copy()
        for k in keys:
            d[k] = None
        return repr(d)

    def __len__(self):
        return len(self._metaTypes)

    def add_metadata(self, key, valType, notify=True):
        """Creates a new entry in the meta data registry.
        The data to set will be of the given 'valType' type."""

        if key in self._metaTypes :
            raise Exception("This key already exists : " + key)

        self._metaTypes[key] = valType
        if(notify):
            self.notify_listeners(("metadata_added", key, valType))
        return

    def remove_metadata(self, key, valType=None, notify=True):
        """Removes an entry in the meta data registry."""

        if key not in self._metaTypes :
            raise Exception("This key doesn't exists : " + key)

        if valType and (self._metaTypes[key] != valType): raise Exception("Type mismatch.")
           
        del self._metaTypes[key]
        del self._metaValues[key]
        if(notify):
            self.notify_listeners(("metadata_removed", key, valType))
        return        
        
    def set_metadata(self, key, value, notify=True):
        """Sets the value of a meta data."""
        if value is None : return 
        if key not in self._metaTypes :
            raise Exception("This key does not exist : " + key)

        if key in self._metaTypes and type(value) != self._metaTypes[key] :
            print(self.__class__, "set_metadata : Unexpected value type", key, 
                  " : ", type(value),
                  " assuming duck-typing")

        self._metaValues[key] = value
        valType = self._metaTypes[key]
        if(notify): 
            self.notify_listeners(("metadata_changed", key, value, valType))
        return
    
    def get_metadata(self, key):
        """Gets the value of a meta data."""
        if key not in self._metaTypes :
            raise Exception("This key does not exist : " + key)
        return  self._metaValues.get(key)

    def simulate_full_data_change(self):
        for k in self._metaValues.keys():
            valType = self._metaTypes[k]
            value = self._metaValues[k]
            self.notify_listeners(("metadata_changed", k, value, valType))

    def __str__(self):
        return self.__repr__()
        
