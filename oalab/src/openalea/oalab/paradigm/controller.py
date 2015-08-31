# -*- python -*-
#
#       OpenAlea.OALab: Multi-Paradigm GUI
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

from openalea.core.service.data import DataFactory
from openalea.core.service.model import ModelFactory, to_model
from openalea.core.service.control import control_namespace
from openalea.core.data import Data
from openalea.core.model import Model
from openalea.core.service.run import namespace


def check_mutually_exclusive(kwds, name1, name2):
    param1 = kwds.pop(name1, None)
    param2 = kwds.pop(name2, None)
    if param1 and param2:
        raise ValueError('%s and %s are mutually exclusive' % (name1, name2))
    elif param1:
        return True, param1
    elif param2:
        return False, param2
    else:
        return None, None


class ParadigmController(object):
    default_name = unicode
    default_file_name = unicode
    pattern = unicode
    extension = unicode
    icon = unicode
    mimetype_model = unicode
    mimetype_data = unicode

    def __init__(self, **kwds):
        self.parent = kwds.pop('parent', None)
        self._widget = None

        mode_name, name_value = check_mutually_exclusive(kwds, 'name', 'filepath')
        mode_model, model_value = check_mutually_exclusive(kwds, 'model', 'data')
        _, code = check_mutually_exclusive(kwds, 'code', 'content')

        if name_value and model_value:
            raise ValueError('model/data and filename/name/content/code are mutually exclusive')

        if mode_name or mode_model:
            self._type = Model
        else:
            self._type = Data

        if name_value and self._type == Model:
            self._obj = ModelFactory(name=name_value, mimetype=self.mimetype_model, code=code)
        elif name_value and self._type == Data:
            self._obj = DataFactory(path=name_value, mimetype=self.mimetype_data, default_content=code)
        elif model_value:
            self._obj = model_value
        else:
            self._obj = ModelFactory(name='NewModel', mimetype=self.mimetype_model)
            self._type = Model

        if self._type == Model:
            self._model = self._obj
        else:
            self._model = to_model(self._obj)

    def read(self):
        if self._widget is None:
            return
        content = self.value()
        self.set_widget_value(content)

    def apply(self):
        if self._widget is None:
            return
        content = self.widget_value()
        self.set_value(content)

    def widget_value(self):
        raise NotImplementedError

    def value(self):
        if self._type == Model:
            content = self._obj.repr_code()
        else:
            content = self._obj.read()
        return content

    def set_widget_value(self, value):
        raise NotImplementedError

    def set_value(self, value):
        if self._type == Model:
            self._obj.set_code(value)
        else:
            self._obj.content = value
            if self._model:
                self._model.set_code(value)

    def runnable(self):
        return self._model is not None

    def _get_model(self):
        return self._model

    model = property(fget=_get_model)

    def execute(self):
        raise NotImplementedError

    def namespace(self, model, **kwargs):
        return namespace(model, **kwargs)

    def run(self, *args, **kwargs):
        if self.runnable():
            self.apply()
            return self.model.run(*args, **self.namespace(self.model, **kwargs))

    def step(self, nstep=1):
        if self.runnable():
            self.apply()
            return self.model.step(nstep=nstep)

    def stop(self):
        if self.runnable():
            return self.model.stop()

    def animate(self, *args, **kwargs):
        if self.runnable():
            self.apply()
            return self.model.animate(*args, **self.namespace(self.model, **kwargs))

    def init(self, *args, **kwargs):
        if self.runnable():
            self.apply()
            return self.model.init(*args, **self.namespace(self.model, **kwargs))

    def widget(self):
        """
        :return: the edition widget
        """
        return self._widget

    name = property(fget=lambda self: self._obj.name)
