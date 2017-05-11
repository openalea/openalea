# -*- coding: utf-8 -*-
# -*- python -*-
#
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2015 INRIA - CIRAD - INRA
#
#       File author(s): Guillaume Baty <guillaume.baty@inria.fr>
#
#       File contributor(s): Guillaume Cerutti <guillaume.cerutti@inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

from openalea.core.service.plugin import plugins
from openalea.core.singleton import Singleton


class WorldAdderManager(object):
    __metaclass__ = Singleton

    def __init__(self):
    	self._world_listeners = []

    def init(self):
    	self._world_listeners = []

    	for plugin in plugins('oalab.world'):
    		world_handler = plugin.implementation()
    		world_handler.initialize()
    		self._world_listeners.append(world_handler)