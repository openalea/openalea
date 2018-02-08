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
"""This module defines the thread manager
The Thread manager provides thread on demand
"""

__license__ = "Cecill-C"
__revision__ = " $Id$ "


from threading import Thread
from Queue import Queue

from openalea.core.singleton import Singleton


class ThreadManager(object):
    """ ThreadManager provides thread on demand """

    __metaclass__ = Singleton

    NUM_THREAD = 4 # Default number of threads

    def __init__(self, num_thread=NUM_THREAD):
        """ Create num_thread Threads """

        self.queue = Queue()

        self.thread_list = []


        for i in xrange(num_thread):
            t = Thread(target=worker, args=(self.queue, ))
            t.setDaemon(True)
            t.start()

            self.thread_list.append(t)

    def add_task(self, func, params):
        """
        Add a task to perform
        :param func: function to call
        :param params : tuple of parameters
        """

        self.queue.put((func, params))

    def clear(self):
        """ clear pending task """

        while(not self.queue.empty()):
            self.queue.get()


def worker(queue):
    """ Thread function """

    while True:
        (func, args) = queue.get()
        apply(func, args)
        queue.task_done()
