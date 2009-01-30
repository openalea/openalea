# -*- python -*-
#
#       OpenAlea.Core
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA
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
"""Special Dict with case insensitive key and protected field"""

__license__ = "Cecill-C"
__revision__ = " $Id$ "


def lower(item):
    try:
        item = item.lower()
    finally:
        return item


def is_protected(item):
    """ Return true the item is protected """

    try:
        return item.startswith('#')
    except:
        return False


def protected(item):
    " Return corresponding protected name for item "
    return "#" + item


class PackageDict(dict):
    """
    Dictionnary with case insensitive key
    This object is able to handle protected entry begining with an '#'
    """

    def __init__(self, *args):
        self.nb_public = None
        dict.__init__(self, *args)

    def __getitem__(self, item):
        item = lower(item)

        try:
            return dict.__getitem__(self, item)
        except KeyError:
            # Try to return protected entry
            return dict.__getitem__(self, protected(item))

    def __setitem__(self, item, y):

        # Update nb public key
        if (self.nb_public and
           not self.has_key(item) and
           not is_protected(item)):
            self.nb_public += 1

        return dict.__setitem__(self, lower(item), y)

    def __contains__(self, key):
        return self.has_key(key)

    def has_key(self, key):

        key = lower(key)
        if (dict.has_key(self, key)):
            return True
        else:
            return dict.has_key(self, protected(key))

    def __delitem__(self, key):

        # Update nb public key
        if (self.nb_public and not is_protected(key)):
            self.nb_public -= 1

        return dict.__delitem__(self, lower(key))

    def get(self, key, default=None):
        return dict.get(self, lower(key), default)

    def iter_public_values(self):
        """ Iterate througth dictionnary value (remove protected value)  """

        for k, v in self.iteritems():
            if (not is_protected(k)):
                yield v

    def nb_public_values(self):
        """ Return the number of unprotected values """

        if (self.nb_public is None):
            l = lambda x: not is_protected(x)
            ks = filter(l, self.iterkeys())
            self.nb_public = len(ks)

        return self.nb_public
