# -*- python -*-
# -*- coding: utf8 -*-
#
#       OpenAlea.OALab
#
#       Copyright 2014 INRIA - CIRAD - INRA
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

""" Control

"""
from openalea.core.observer import Observed
from openalea.core.service.interface import (new_interface,
                                             interface_default_value)


class Control(Observed):

    """
    A Control is an observable variable with
      - name
      - interface
      - constraints on values
    """

    def __init__(self, name, interface=None, value=None, widget=None,
                 constraints=None, **kwds):
        """
        :param name: Control name
        :type name: basestring
        :param interface: Interface name or class
        :type interface: basestring or
                         :class:`openalea.core.interface.IInterface`
        :param value: value to initialise control
                      [Default: use interface default value].
        :type value: value compatible with interface
        :param widget: name of preferred widget [Default: undefined]
        :type widget: basestring
        :param constraints: constraints to set to interface.
                            See Interface documentation [Def: no constraints]
        :type constraints: :obj:`dict`
        """
        Observed.__init__(self)

        self.name = name
        self.widget = widget

        if constraints is None:
            constraints = {}
        self._interface = new_interface(interface, value, **constraints)

        self._value = value
        if value is None:
            self._value = interface_default_value(self._interface)

        self._label = kwds.get('label', None)
        self._default_value = kwds.get('default', self._value)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self is other
        else:
            return self.value == other

    def __repr__(self):
        kargs = dict(
            interface=self._interface,
            name=self.name,
            value=self._value,
        )
        return 'Control(%(name)r, %(interface)r, value=%(value)r)' % kargs

    def __json__(self):
        from openalea.core.service.serialization import serialize
        return {
            'name': self.name,
            'interface': repr(self.interface),
            'value': serialize(self._value, fmt='json'),
            'widget': self.widget
        }

    def notify_change(self):
        """
        Send value_changed event
        """
        self.notify_listeners(('value_changed', self._value))

    def rename(self, name):
        """
        :param name: new name
        :type name: basestring
        """
        self.name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name
        self.notify_listeners(('name_changed', self._name))

    @property
    def label(self):
        if self._label is None:
            return self._name
        else:
            return self._label

    @property
    def default(self):
        return self._default_value

    @property
    def value(self):
        return self._value

    @property
    def identifier(self):
        return str(id(self))

    @value.setter
    def value(self, value):
        self.set_value(value)

    def set_value(self, value):
        """
        TODO: CPL: To discuss !!!!
        Deepcopy or not ?
        Currently, standard python behaviour:
        copy for non mutable else reference
        """
        try:
            if value != self._value:
                self._value = value
                self.notify_change()
        except ValueError:
            # Case of equality comparison is not defined
            if value is not self._value:
                self._value = value
                self.notify_change()

    @property
    def interface(self):
        return self._interface

    def reset(self):
        self.value = interface_default_value(self._interface)

    # Tries to behave like Node and InputNode
    def __getitem__(self, key):
        if key == 'name':
            return self.name
        else:
            raise KeyError(key)

    def get_input_port(self, name=None):
        return self

    def set_input(self, key, val=None, notify=True):
        self.value = val

    def get_label(self):
        return self.name
