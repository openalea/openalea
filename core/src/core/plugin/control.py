# -*- coding: utf-8 -*-
# -*- python -*-
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2014 INRIA
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

"""

Control - Advanced
==================

Widget
------

For a complete explanation of code to write for each function, or to create a class
from scratch, please have a look to :class:`~IControlWidget` and example after.

To create a class for standard QWidget, you can copy/paste this code

.. code-block:: python
    :filename: mypackage/plugins/widgets.py
    :linenos:

    from openalea.oalab.gui.control.widget import AbstractQtControlWidget
    class XyzControlWidget(AbstractQtControlWidget):
        def __init__(self):
            AbstractQtControlWidget.__init__(self)
            self.value_changed_signal = 'qt signal' # for example 'valueChanged()', 'currentTextChanged()', ...

        def reset(self, value=None, **kwargs):
            if value is None:
                self.setValue(REAL_VALUE)
            self.setC1(kwargs.get('constraint1', DEFAULT_CONSTRAINT1))

        def setValue(self, value):
            raise NotImplementedError

        def value(self):
            raise NotImplementedError

Widget selector
---------------

.. code-block:: python
    :filename: mypackage/plugins/selectors.py
    :linenos:

    class XyzControlWidgetSelector(object):
        def __init__(self):
            pass

        @classmethod
        def edit(cls, control, shape=None):
            if shape == 'responsive':
                from mypackage.plugins.widgets import XyzControlWidget
                widget = XyzControlWidget()
                widget.tune()
                return widget

        @classmethod
        def view(self, control, shape=None):
            return None

        @classmethod
        def create(cls, shape=None):
            return None

        @classmethod
        def snapshot(cls, control, shape=None):
            return None

        @classmethod
        def paint(cls, control, painter, rectangle, option=None):
            return None

        @classmethod
        def edit_constraints(cls):
            return None



 Plugin
 ------

Here plugin is exactly the same as simple approach, except that it returns
XyzControlWidgetSelector instead of XyzControlWidget.

.. code-block:: python

     from openalea.oalab.plugin.control import ControlWidgetSelectorPlugin
     from openalea.deploy.shared_data import shared_data

     class PluginXyzWidgetSelector(ControlWidgetSelectorPlugin):

         controls = ['IXyz'] # Interface name like IInt
         edit_shape = ['responsive']
         name = 'XyzWidgetSelector'

         @classmethod
         def load(cls):
             from mypackage.plugins.selectors import XyzControlWidgetSelector
             return XyzControlWidgetSelector

.. seealso::

    See IInt example for real case





IInt control widget
-------------------

All Qt sliders define "value" and "setValue" methods directly compatible with IInt (int),
so there is almost nothing to do:

We will use these widgets depending on context:
    - QDial for responsive, large and small shapes
    - QSlider for vline
    - QSpinBox for hline

.. literalinclude:: ../../../openalea-src/oalab/src/openalea/oalab/plugins/controls/widgets.py
    :linenos:
    :pyobject: AbstractIntWidget

.. literalinclude:: ../../../openalea-src/oalab/src/openalea/oalab/plugins/controls/widgets.py
    :linenos:
    :pyobject: IntDial

.. literalinclude:: ../../../openalea-src/oalab/src/openalea/oalab/plugins/controls/widgets.py
    :linenos:
    :pyobject: IntSpinBox

.. literalinclude:: ../../../openalea-src/oalab/src/openalea/oalab/plugins/controls/widgets.py
    :linenos:
    :pyobject: IntSimpleSlider

We define also a widget to edit constraints

.. literalinclude:: ../../../openalea-src/oalab/src/openalea/oalab/plugins/controls/constraints.py
    :linenos:
    :pyobject: IntConstraintWidget

Now, lets define widget selector to group all classes together :

.. literalinclude:: ../../../openalea-src/oalab/src/openalea/oalab/plugins/controls/selectors.py
    :linenos:
    :emphasize-lines: 11
    :pyobject: IntWidgetSelector

You can notice in line 11, instruction to set widget to fit to vline shape.

And finally, lets define plugin that links to it.

.. literalinclude:: ../../../openalea-src/oalab/src/openalea/oalab/plugins/controls/__init__.py
    :linenos:
    :pyobject: PluginIntWidgetSelector

.. warning::

    All classes can be defined in same file **excepted last one**.
    PluginIntWidgetSelector must be defined in a separated file to allow to load only description.

Glossary
========

.. glossary::

    create mode
        Users want to create a control from scratch.
        In other words, it can be considered as "write-only" widget.

    view mode
        Users want to visualize a control. If control value changes, users may want to see changes.
        In other words, it can be considered as a "read-only" with option to enable :term:`auto-read mode`.

    edit mode
        Users want to edit a control. If control value changes, users may want to reload changes.
        Users may want theirs changes to be applied dynamically or not.
        In other words, it can be considered as a "read/write" widget with options to enable both :term:`auto-read mode` mode and :term:`auto-apply mode`.

    auto-read mode
        If widget has auto-read mode enabled: if value changes, view is automatically refreshed to display new value.

    auto-apply mode
        If widget has auto-apply mode enabled: each time users modify data in the view, changes are automatically applied to object being edited.

    control shape
        shape supported by a control editor or viewer:

        - hline: widget fits well in an horizontal line for example in a cell in a table or spreadsheet, in a 200x20px widget, ...
        - vline: widget fits well in a vertical line, for example in 20x200px widget
        - small: widget fits well in a small squared widget (100x100 px to 300x300 px)
        - large: widget fits well in large space (> 300x300 px)
        - responsive: widget can fit well in all shapes and sizes. Hardest to create but easiest to use.


Details
=======

.. autoclass:: openalea.oalab.plugins.control.IConstraintWidget
    :members:

.. autoclass:: openalea.oalab.plugins.control.IControlWidget
    :members:

.. autoclass:: openalea.oalab.plugins.control.IWidgetSelector
    :members:



.. autoclass:: openalea.oalab.plugins.control.ControlWidgetSelectorPlugin
    :members:


"""

from openalea.core.interface import IInterface


class ControlWidgetSelectorPlugin(object):
    """

    """

    controls = []
    name = 'ControlWidget'
    icon_path = None

    edit_shape = [] # ['hline', 'vline', 'small', 'large', 'responsive']
    view_shape = [] # ['hline', 'vline', 'small', 'large', 'responsive']
    create_shape = [] # ['hline', 'vline', 'small', 'large', 'responsive']
    paint = False

    @classmethod
    def load(cls):
        raise NotImplementedError




class IControlWidget(IInterface):
    """
    An IControlWidget is a
    """

    def __init__(self):
        """
        """

    def reset(self, value=None, *kargs):
        """
        Reset widget to default values.
        """

    def set(self, control):
        """
        Use control to preset widget.
        Starts to listen to control events and read control's values
        """

    def apply(self, control):
        """
        Update control with widget values.
        """

    def read(self, control):
        """
        Update widget with control values
        """

    def notify(self, sender, event):
        """
        Method called when Observed control changes.
        Generally, when control send an event "ValueChanged", we want to
        refresh widget with new value.
        """

    def autoread(self, control, auto=True):
        """
        Enable auto-read mode on given control.
        Important, control passed to autoread and autoapply can be identical or different.
        For example if you want to refresh view if a template changes and apply it automatically to your current control.
        """

    def autoapply(self, control, auto=True):
        """
        Enable auto-apply mode on given control
        """

    def on_value_changed(self, *args, **kwargs):
        """
        Method called when value changed.
        This method generally read control and refresh view if :term:`auto-read mode` is enabled.
        """

    def setValue(self, value):
        """
        Change widget value.
        If your class derivates from an third-party widget, it is sometime necessary
        to adapt control value type to widget supported type.
        Example unicode to QString in pyqt API v1.
        """

    def value(self, interface=None):
        """
        Returns widget value.
        If your class derivates from an third-party widget, it is sometime necessary
        to adapt widget value type to control type.
        If widget supports more than one interface, returned value depends on given interface.
        If none, returns widget preferred type.
        """




class IWidgetSelector(IInterface):
    def __init__(self):
        pass

    @classmethod
    def edit(cls, control, shape=None):
        """
        Returns an instance of IControlWidget that modifies control in place.
        Control can be updated continuously or on explicit user action
        (click on apply button for instance)
        """

    @classmethod
    def view(cls, control, shape=None):
        """
        Returns an instance of IControlWidget that view control.
        This function never modify control.
        If you finally want to modify it, you can call "apply" explicitly.
        """

    @classmethod
    def create(cls, shape=None):
        """
        Returns an instance of IControlWidget that can generate controls.
        """

    @classmethod
    def snapshot(cls, control, shape=None):
        """
        Returns a widget representing control
        """

    @classmethod
    def paint(cls, control, painter, rectangle, option=None):
        """
        Paints widget using painter.
        This function never modify control.
        """

    @classmethod
    def edit_constraints(cls):
        """
        Returns a widget to edit constraints.
        This widget must respect :class:`~IConstraintWidget` interface.
        """
        return None

class IConstraintWidget(IInterface):
    def constraints(self, interface=None):
        """
        Returns a dict "constraint name" -> "value"
        """


