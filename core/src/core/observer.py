#   -*- python -*-
#
#         OpenAlea.Core
#
#         Copyright 2006-2009 INRIA - CIRAD - INRA
#
#         File author(s): Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#                         Christophe Pradal <christophe.prada@cirad.fr>
#
#         Distributed under the Cecill-C License.
#         See accompanying file LICENSE.txt or copy at
#             http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#         OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################
"""This module defines all the classes for the Observer design Pattern"""

__license__ = "Cecill-C"
__revision__ = " $Id$ "

try:
    import openalea.grapheditor
    graphobserver = True
except ImportError, e:
    print "NOT using graph editor observer", e
    graphobserver = False

###############################################################################

if graphobserver:
    from openalea.grapheditor.observer import *
else:
   import weakref
   from collections import deque


   class Observed(object):
       """ Observed Object """

       def __init__(self):

           self.listeners = set()
           self.__isNotifying = False
           self.__postNotifs = [] #calls to execute after a notication is done
           self.__exclusive = None

       def register_listener(self, listener):
           """ Add listener to list of listeners.
           If the observed is currently notifying, the registration
           is delayed until it finishes."""
           if(not self.__isNotifying):
               wr = weakref.ref(listener, self.unregister_listener)
               self.listeners.add(wr)
           else:
               def push_listener_after():
                   self.register_listener(listener)
               self.__postNotifs.append(push_listener_after)

       def unregister_listener(self, listener):
           """ Remove listener from the list of listeners """
           if(not self.__isNotifying):
               if isinstance(listener, weakref.ref):
                   self.listeners.discard(listener)
               else:
                   toDiscard = None
                   for lis in self.listeners:
                       if lis() == listener:
                           toDiscard = lis
                           break
                   self.listeners.discard(toDiscard)
           else:
               def discard_listener_after():
                   self.unregister_listener(listener)
               self.__postNotifs.append(discard_listener_after)

       def transfer_listeners(self, newObs):
           """Takes all this observed's listeners, unregisters them
           from itself and registers them to the newObs, calling
           listener.change_observed if implemented"""
           self.__isNotifying = True
           for lis in self.listeners:
               self.unregister_listener(lis)
               newObs.register_listener(lis())
               lis().change_observed(self, newObs)
           self.__isNotifying = False

       def exclusive_command(self, who, command, *args, **kargs):
           """Executes a call "command" and if it triggers any
           signal from this observed object along the way, "who" will
           be the only one to be notified"""
           ln = [i() for i in self.listeners]
           if who not in ln:
               raise Exception("Observed.exclusive : " + str(who) + " is not registered")

           self.__exclusive = who
           command(*args, **kargs)
           self.__exclusive = None

       def notify_listeners(self, event=None):
           """
           Send a notification to all listeners

           :param event: an object to pass to the notify function
           """

           self.__isNotifying = True

           #If an exclusive handler is set let's only
           #notify that one.
           if(self.__exclusive):
               self.__exclusive.call_notify(self, event)
           else:
               toDelete = []
               for ref in self.listeners:
                   obs = ref()
                   if(obs is None):
                       toDelete.append(ref)
                       continue
                   if(not obs.is_notification_locked()):
                       try:
                           obs.call_notify(self, event)
                       except Exception, e:
                           print "Warning :", str(self), "notification of", str(obs), "failed", e

               for dead in toDelete:
                   self.listeners.discard(dead)

           self.__isNotifying = False
           self.post_notification()

       def post_notification(self):
           for action in self.__postNotifs:
               action()
           self.__postNotifs = []

       def __getstate__(self):
           """ Pickle function """
           odict = self.__dict__.copy()
           odict['listeners'] = set()
           return odict

   class AbstractListener(object):
       """ Listener base class """

       notify_lock = None

       def __init__(self):
           self.__deaf = False
           self.__eventQueue = None

       def initialise(self, observed):
           """ Register self as a listener to observed """
           assert observed != None
           observed.register_listener(self)
           if (self.notify_lock == None):
               self.notify_lock = list()

       def change_observed(self, old, new):
           return

       def is_notification_locked(self):
           return self.notify_lock != None and len(self.notify_lock)>0

       def deaf(self, setDeaf=True):
           self.__deaf=setDeaf

       def queue_call_notifications(self, call, *args, **kwargs):
           """ Runs a call and queues notifications coming from that call
           to this listener. Once the call is finished, queued notifications
           are processed FIFO."""
           self.__eventQueue = deque()
           call(*args, **kwargs)
           self.__process_queued_calls()

       def __process_queued_calls(self):
           queue = deque(self.__eventQueue)
           self.__eventQueue = None
           for e in queue:
               self.call_notify(e[0], e[1])

       def call_notify(self, sender, event=None):
           """
           Basic implementation call directly notify function
           Sub class can override this method to implement different call strategy
           (like signal slot)
           """
           #if we are running a call with delayed event delivery
           #we queue the events:
           if self.__eventQueue is not None :
               self.__eventQueue.append((sender, event))
           elif not self.__deaf:
               self.notify(sender, event)

       def notify(self, sender, event=None):
           """
           This function is called by observed objects

           :param sender: the observed object which send notification
           :param event: the data associated to the notification
           """
           raise NotImplementedError()


   # Decorator function to protect an AbstractListener against notification


   def lock_notify(method):

       def wrapped(self, *args, **kwargs):

           if(self.notify_lock == None):
               self.notify_lock = list()
           self.notify_lock.append(True)
           try:
               result = method(self, *args, **kwargs)
           finally:
               self.notify_lock.pop()

           return result


       return wrapped

