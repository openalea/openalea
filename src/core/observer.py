# -*- python -*-
#
#       OpenAlea.Core: OpenAlea Core 
#
#       Copyright or (C) or Copr. 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Christophe Pradal <christophe.prada@cirad.fr>
#                       Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#

__doc__="""
This module defines all the classes for the Observer design Pattern
"""

__license__= "Cecill-C"
__revision__=" $Id$ "

###############################################################################


import weakref



class Observed(object):
    """ Observed Object """

    def __init__(self):

        self.listeners = set()

    def register_listener(self, listener):

        wr = weakref.ref(listener, self.unregister_listener)
        self.listeners.add(wr)
    
    def unregister_listener(self, listener):
        self.listeners.discard(listener)

    def notify_listeners(self, event=None):
        for wr in self.listeners :
            l = wr()
            l.notify(self, event)

    def __del__(self):
        print self.listeners


class AbstractListener(object):
    """ Listener base class """
    
    def initialise (self, observed):
        observed.register_listener(self)

    def notify (self, sender, event=None):
        raise RuntimeError()

    

    

