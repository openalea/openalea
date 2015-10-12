# -*- python -*-
#
#       OpenAlea.Core
#
#       Copyright 2006-2015 INRIA - CIRAD - INRA
#
#       File author(s): Christophe Pradal <christophe.prada@cirad.fr>
#                       Guillaume Baty <guillaume.baty@inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################
""" Abstract Factory classes and methods.

A Factory build Functor (Nodes or Pluggings) from its description.
Factories instantiates Functors.
"""

__license__ = "Cecill-C"


class AbstractFactory(object):

    """
    Abstract Factory is Factory base class.

    :Properties:
        - name
        - metainfo

        - module
        - distribution (aka egg name) 
    """

    mimetype = "openalea/factory"

    #package = property(get_pkg, set_pkg)

    def is_valid(self):
        """
        Return True if the factory is valid
        else raise an exception
        """
        return True

    def instantiate(self, call_stack=[]):
        """ Return a node instance

        :param call_stack: the list of NodeFactory id already in call stack
            (in order to avoir infinite recursion)
        """
        raise NotImplementedError()

    def __call__(self, *args, **kwds):
        return self.instantiate()
