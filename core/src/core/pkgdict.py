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
Special Dict with case insensitive key and protected field
"""
__license__= "Cecill-C"
__revision__=" $Id: nocasedict.py 999 2007-12-13 18:17:41Z dufourko $ "




class PackageDict(dict):
    """ 
    Dictionnary with case insensitive key
    This object is able to handle protected entry begining with an '_'
    """

    def __init__(self, *args):
        self.nb_public = None
        dict.__init__(self, *args)


    def lower(self, item):
        try:
            item = item.lower()
        finally:
            return item

    def is_protected(self, item):
        return item.startswith('_')


    def protected(self, item):
        " Return corresponding protected name for item "
        return "_" + item


    def __getitem__(self, item):
        
        item = self.lower(item)

        try:
            return dict.__getitem__(self, item)
        except KeyError:
            # Try to return protected entry
            return dict.__getitem__(self, self.protected(item))

    
    def __setitem__(self, item, y):
        self.nb_public = None
        return dict.__setitem__(self, self.lower(item), y)


    def has_key(self, key):
        
        key = self.lower(key)
        if(dict.has_key(self, key)):
            return True
        else:
            return dict.has_key(self, self.protected(key))
        

    def __delitem__(self, key):
        self.nb_public = None
        return dict.__delitem__(self, self.lower(key))


    def get(self, key, default=None):
        return dict.get(self, self.lower(key), default)


    def iter_public_values(self):
        """ Iterate througth dictionnary value (remove protected value)  """

        for k, v in self.iteritems():
            if(not self.is_protected(k)):
                yield v

    def nb_public_values(self):
        """ Return the number of unprotected values """

        if(self.nb_public is None):
            l = lambda x : not self.is_protected(x)
            ks = filter(l, self.iterkeys())
            self.nb_public = len(ks)

        return self.nb_public
    
