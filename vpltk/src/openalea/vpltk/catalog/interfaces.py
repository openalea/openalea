# -*- python -*-
#
#       Plugin System for vpltk
# 
#       OpenAlea.VPLTk: Virtual Plants Lab Toolkit
#
#       Copyright 2013 INRIA - CIRAD - INRA
#
#       File author(s): Guillaume Baty <guillaume.baty@inria.fr>
#
#       File contributor(s):
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

from openalea.vpltk.catalog.interface import IInterface


class IRegister(IInterface):
    """
    dictionary of adapters
    """

class ICatalog(IInterface):
    """
    ICatalog is a meta plugin manager.
    It is used to discover all plugins and especially interfaces.

    Properties :

        * plugin_types = ('wralea', 'plugin', 'adapters', 'interfaces')
        * groups : list all entry_point groups found on this system
        * managers : list of PluginManager currently used. 
          At launch, only plugin manager (generic place) and interface manager
          are defined.
    """

    def interface(self, name):
        """
        Returns interface class associated to name
        """


    def interface_id(self, interface):
        """
        Returns name of "interface" class
        """


    def interfaces(self, obj=None):
        """
        Returns list of all interface names.
        If obj is defined, returns list of names of interfaces implemented by this object.
        """


    def is_implementation(self, obj, interface):
        """
        Returns True if obj implements interface.

        :param interface: Interface class or name
        """

    def factories(self, interfaces=None, name=None, tags=None, exclude_tags=None):
        """
        Returns all factories matching given criteria.
        exclude_tags: if tags is not specified, scan all tags except one defined in exclude_tags
        """

    def factory(self, interfaces=None, name=None, tags=None, exclude_tags=None):
        """
        Returns first factory matching given criteria.
        """

    def create_service(self, object_factory, *args, **kargs):
        """
        Create a service from object_factory. If object_factory is None, returns None.
        If this factory is called for the first time, instantiate it with args and kargs.
        Else, use previous instance.
        """

    def service(self, interfaces=None, name=None, tags=None, exclude_tags=None, args=None, kargs=None):
        """
        Returns first service matching given criteria.
        """

    def services(self, interfaces=None, name=None, tags=None, exclude_tags=None, args=None, kargs=None):
        """
        Returns all services matching given criteria.
        """
