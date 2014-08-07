# -*- coding: utf-8 -*-
# -*- python -*-
#
#       OpenAlea.Core
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA
#
#       File author(s): Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#                       Christophe Pradal <christophe.prada@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################
"""This module defines the singleton metaclass"""

__license__ = "Cecill-C"
__revision__ = " $Id$ "


class Singleton(type):
    """ Singleton Metaclass """

    def __init__(cls, name, bases, dic):
        super(Singleton, cls).__init__(name, bases, dic)
        cls.instance=None

    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance=super(Singleton, cls).__call__(*args, **kw)
        return cls.instance


import weakref
class ProxySingleton(Singleton):
    """ Singleton Metaclass which returns a proxy """

    def __call__(cls, *args, **kw):
        return weakref.proxy(Singleton.__call__(cls, *args, **kw))
