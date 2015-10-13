# -*- python -*-
#
#       OpenAlea.Core
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA
#
#       File author(s): Jerome Chopard <revesansparole@gmail.com>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite: http://openalea.gforge.inria.fr
#
###############################################################################
""" This module provide an implementation of a way
to store data exchanged between nodes of a dataflow.
"""

__license__ = "Cecill-C"
__revision__ = " $Id$ "


class DataflowState(object):
    """ Store outputs of node and provide a way to access them
    """
    def __init__(self, dataflow):
        """ constructor

        args:
            - dataflow (Dataflow)
        """
        self._dataflow = dataflow
        self._state = {}

    def clear(self):
        """Clear state
        """
        self._state.clear()

    def reinit(self):
        """ Remove all data stored except for the one
        associated to lonely input ports.
        """
        df = self._dataflow

        # save state
        save = dict((pid, dat) for pid, dat in self._state.items()
                    if df.is_in_port(pid) and df.nb_connections(pid) == 0)

        # clear
        self.clear()

        # resume state
        self._state.update(save)

    def is_ready_for_evaluation(self):
        """ Test wether the state contains enough information
        to evaluate the associated dataflow.

        Simply check that each lonely input port has
        some data attached to it.
        """
        df = self._dataflow
        state = self._state

        return all([pid in state for pid in df.in_ports()
                    if df.nb_connections(pid) == 0])

    def is_valid(self):
        """ Test wether all data have been computed
        """
        df = self._dataflow
        state = self._state

        if not self.is_ready_for_evaluation():
            return False

        # check that all nodes have been evaluated
        if not all([pid in state for pid in df.out_ports()]):
            return False

        return True

    def cmp_port_priority(self, pid1, pid2):
        """ Compare port priority.

        Compare first x position of actors
        then use pids"""
        df = self._dataflow

        try:
            node1 = df.actor(df.vertex(pid1))
        except KeyError:
            return cmp(pid1, pid2)

        try:
            node2 = df.actor(df.vertex(pid2))
        except KeyError:
            return cmp(pid1, pid2)

        p1 = node1.get_ad_hoc_dict().get_metadata('position')[0]
        p2 = node2.get_ad_hoc_dict().get_metadata('position')[0]

        ret = cmp(p1, p2)
        if ret != 0:
            return ret

        return cmp(pid1, pid2)

    def get_data(self, pid):
        """ Retrieve data associated with a port.

        If pid is an output port, retrieve single item of data
        if pid is an input port, retrieve data on all output
        ports connected to this port and return a list of it
        or a single item if only one port connected

        args:
            - pid (pid): id of port either in or out
        """
        df = self._dataflow
        state = self._state

        if pid in state:  # either out_port or lonely in_port
            return state[pid]
        elif df.is_out_port(pid):
            raise KeyError("value not set for this port")
        else:
            npids = list(df.connected_ports(pid))
            if len(npids) == 0:
                raise KeyError("lonely in_port not set")
            elif len(npids) == 1:
                return self.get_data(npids[0])
            else:
                npids.sort(self.cmp_port_priority)
                return [self.get_data(pid) for pid in npids]

    def set_data(self, pid, data):
        """ Store data on a port.

        This function does not test that the port is an output port

        args:
            - pid (pid): id of port
            - data (any)
        """
        self._state[pid] = data
