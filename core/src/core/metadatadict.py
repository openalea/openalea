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

from openalea.core import observer
import types

class MetaDataDict(observer.Observed):
    """Attach meta data to a graphical representation
    of a GraphView component. This metadata can be 
    used to customize the appearance of the node."""
    def __init__(self):
        observer.Observed.__init__(self)
        self._metas = {}
        return

    def add_metadata(self, key, valType, notify=True):
        """Creates a new entry in the meta data registry.
        The data to set will be of the given 'type' type."""
        assert type(valType) == types.TypeType

        if key in self._metas :
            raise Exception("This key already exists : " + key)

        self._metas[key] = [valType, None]
        if(notify):
            self.notify_listeners(("MetaDataAdded", key, valType))
        return

    def set_metadata(self, key, value, notify=True):
        """Sets the value of a meta data."""
        if key not in self._metas :
            raise Exception("This key does not exist : " + key)

        if( type(value) != self._metas[key][0] ) :
            print(self.__class__, "set_metadata : Unexpected value type", key, 
                  " : ", type(value),
                  " assuming duck-typing")

        self._metas[key][1] = value
        valType = self._metas[key][0]
        if(notify): 
            self.notify_listeners(("MetaDataChanged", key, value, valType))
        return
    
    def get_metadata(self, key):
        """Gets the value of a meta data."""
        if key not in self._metas :
            raise Exception("This key does not exist : " + key)
        
        return self._metas[key][1]

    def simulate_full_data_change(self):
        for k in self._metas.keys():
            value = self._metas[k][1]
            valType = self._metas[k][0]
            self.notify_listeners(("MetaDataChanged", k, value, valType))

    def __str__(self):
        return self._metas.__str__()
        
