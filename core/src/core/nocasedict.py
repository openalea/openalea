# -*- python -*-
#
#       OpenAlea.Core
#
#       Copyright 2006-2007 INRIA - CIRAD - INRA  
#
#       File author(s): Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

__doc__="""
NoCaseDict is a python dictionnary with case insensitive key 
"""
__license__= "Cecill-C"
__revision__=" $Id$ "


class NoCaseDict(dict):
    """ Dictionnary case insensitive"""

    def convert_item(self, item):
        try:
            item = item.lower()
        finally:
            return item

    def __getitem__(self, item):
        return dict.__getitem__(self, self.convert_item(item))

    
    def __setitem__(self, item, y):
        return dict.__setitem__(self, self.convert_item(item), y)


    def has_key(self, key):
        return dict.has_key(self, self.convert_item(key))


    def __delitem__(self, key):
        return dict.__delitem__(self, self.convert_item(key))


    def get(self, key, default=None):
        return dict.get(self, self.convert_item(key), default)
