# -*- python -*-
# -*- coding: utf8 -*-
#
#       OpenAlea.OALab
#
#       Copyright 2014 INRIA - CIRAD - INRA
#
#       File author(s): Julien Coste <julien.coste@inria.fr>
#                       Guillaume Baty <guillaume.baty@inria.fr>
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

A Model is an object that can be run.
It is generally used to define algorithms or process.

A model has inputs, outputs and an internal state.
Inputs and outputs are used to allow communication between environnement and models and between models.
Internal state is used by the model itself but cannot be reached from outside.
This internal step is generally used when user want to execute model step by step, 
each step depending on previous one.

To define model instructions, you need to define at least "step" instructions.
To do that, you can use:
    - :meth:`~IModel.set_step_code`
To use a Model, you also need to define set_code method that is able to extract inputs, outpus and step, init, ... 
from given source code.

Animate notification are not yet implemented.

To reset internal state, use :meth:`~openalea.core.model.IModel.init` method.
To run one step, use :meth:`~openalea.core.model.IModel.step` method.

Two convenience methods, see :meth:`~openalea.core.model.IModel.run` and "call"
can be used to reset internal state and run a given number of step (one by default)

By default, functions are generated for "init", "run" and "animate"
"""

from ast import literal_eval
from copy import copy


class IModel(object):
    dtype = None
    mimetype = None

    def __init__(self, **kwds):
        """
        keywords:
            - name: model name
        """

    def __call__(self, *args, **kwargs):
        """
        Equivalent to :meth:`~openalea.core.model.IModel.run`.
        """

    def run(self, *args, **kwargs):
        """
        Init model and run "nstep" step(s).
        """
        raise NotImplementedError

    def init(self, *args, **kwargs):
        """
        Reset internal state, fill namespace and run "init code" if defined.
        """
        raise NotImplementedError

    def step(self, *args, **kwargs):
        """
        run "step code" if defined.
        """
        raise NotImplementedError

    def stop(self, *args, **kwargs):
        """
        Stop execution.
        """
        raise NotImplementedError

    def animate(self, *args, **kwargs):
        """
        Like run but send notification at each step.
        """
        raise NotImplementedError

    def set_code(self, code):
        """
        extract and set inputs, outputs and functions from code.
        For example, if "code" is::

            '''
            input = a, b:int=5
            output = c
            '''
            def step():
                c = a+b

        you can extract input, output and step function.
        So, 
        m = Model("m1")
        m.set_code(code)

        is equivalent to

        m = Model("m1")
        m.set_func_code("step", "c=a+b")
        m.inputs_info = [InputObj('a'), InputObj('b:int=5')]
        m.outputs_info = [OutputObj('c')]
        """

    def set_func_code(self, fname, code):
        """
        :param fname: function name: "step", "init", "animate", ...
        :param code: python source code
        """

    def set_step_code(self, code):
        """
        convenience method equivalent to set_func_code("step", code)
        """


class Model(object):
    icon = ''

    def __init__(self, name=None, **kwds):
        from openalea.core.service.ipython import interpreter
        self.interp = interpreter()

        self.inputs_info = []
        self.outputs_info = []

        self.name = name

        self._ns = {}
        self._code = {}
        self._initial_code = ''

        self.outputs = []
        code = kwds.pop('code', None)
        if code:
            self.set_code(code)

    def __copy__(self):
        m = self.__class__(name=self.name)
        m.inputs_info = list(self.inputs_info)
        m.outputs_info = list(self.outputs_info)
        for fname, code in self._code.iteritems():
            m.set_func_code(fname, code)
        return m

    def set_code(self, code):
        self.set_step_code(code)

    def set_func_code(self, fname, code):
        self._code[fname] = code

    def set_step_code(self, code):
        self.set_func_code('step', code)

    def init(self, *args, **kwds):
        # Save default namespace
        old_ns = copy(self.interp.user_ns)

        # Create a new namespace with
        #  - interpreter namespace
        #  - initial namespace given by user (namespace keyword)
        #  - passed variables
        # Then, replace input variable names with right values
        initial_ns = kwds.pop('namespace', {})

        global_ns = {}
        global_ns.update(old_ns)
        global_ns.update(initial_ns)
        global_ns.update(kwds)
        global_ns['this'] = self

        kwargs = self.inputs_from_ns(self.inputs_info, global_ns, *args, **kwds)
        global_ns.update(kwargs)

        self._ns = global_ns

        self.interp.user_ns.clear()
        self.interp.user_ns.update(self._ns)

        # Run init code
        if 'init' in self._code:
            self.interp.shell.run_code(self._code['init'])

        # add vars defined in init function
        for k in self.interp.user_ns:
            if k not in self._ns:
                self._ns[k] = self.interp.user_ns[k]

        # Restore original namespace
        self.interp.user_ns.clear()
        self.interp.user_ns.update(old_ns)

        return self.output_from_ns(self._ns)

    def __call__(self, *args, **kwds):
        return self.run(*args, **kwds)

    def _exec(self, fname='step'):
        # Save namespace
        old_ns = {}
        old_ns.update(self.interp.user_ns)
        self.interp.user_ns.clear()
        self.interp.user_ns.update(self._ns)

        # Run code
        if fname in self._code:
            self.interp.shell.run_code(self._code[fname])
        outputs = self.output_from_ns(self.interp.user_ns)

        self.interp.user_ns.clear()
        self.interp.user_ns.update(old_ns)

        self.outputs = outputs
        return outputs

    def run_code(self, code, namespace):
        # Save namespace
        ns = {}
        ns.update(namespace)
        old_ns = self.interp.user_ns
        self.interp.user_ns = ns
        self.interp.run_cell(code)
        self.interp.user_ns = old_ns

        final_ns = {}
        for key in ns:
            if key in old_ns:
                continue
            final_ns[key] = ns[key]
        return final_ns

    def execute(self, code):
        self.set_func_code('selection', code)
        outputs = self._exec('selection')
        del self._code['selection']
        return outputs

    def step(self):
        return self._exec('step')

    def animate(self, *args, **kwds):
        if 'animate' in self._code:
            return self._exec('animate')
        else:
            nstep = kwds.pop('nstep', 1)
            self.init(*args, **kwds)
            out = []
            for i in range(nstep):
                out = self.step()
                # refresh world
            return out

    def run(self, *args, **kwds):
        if 'run' in self._code:
            return self._exec('run')
        else:
            nstep = kwds.pop('nstep', 1)
            self.init(*args, **kwds)
            out = []
            for i in range(nstep):
                out = self.step()
            return out

    def eval_value(self, value):
        return literal_eval(value)

    def inputs_from_ns(self, inputs, ns, *args, **kwargs):
        kwds = {}
        if inputs is None:
            return kwds
        for i, inp in enumerate(inputs):
            name = inp.name
            default = inp.default
            try:
                kwds[name] = args[i]
            except IndexError:
                if name in kwargs:
                    kwds[name] = kwargs[name]
                else:
                    if default is not None:
                        kwds[name] = self.eval_value(default)
                    elif name in ns:
                        kwds[name] = ns[name]
                    else:
                        pass
        return kwds

    def output_from_ns(self, namespace):
        """
        Get outputs from namespace and set them inside self.outputs

        :param namespace: dict where the model will search the outputs
        """
        outputs = []
        if self.outputs_info:
            if len(self.outputs_info) > 0:
                for outp in self.outputs_info:
                    if outp.name in namespace:
                        outputs.append(namespace[outp.name])
                        self._ns[outp.name] = namespace[outp.name]
        if len(outputs) == 0:
            return None
        elif len(outputs) == 1:
            return outputs[0]
        else:
            return outputs

    def get_documentation(self):
        """
        :return: a string with the documentation of the model
        """
        return ''

    @property
    def step_code(self):
        return self._code['step']

    @step_code.setter
    def step_code(self, code):
        self._code['step'] = code

    def _set_code(self, code):
        self.set_code(code)

    def repr_code(self):
        raise NotImplementedError

    code = property(fset=_set_code)


class PythonModel(Model):
    dtype = 'Python'
    mimetype = 'text/x-python'

    def __init__(self, **kwargs):
        Model.__init__(self, **kwargs)

    def get_documentation(self):
        """
        :return: a string with the documentation of the model
        """
        try:
            return self._doc
        except AttributeError:
            return ''

    def repr_code(self):
        try:
            return self._initial_code
        except AttributeError:
            code = '"""\n'
            if self.inputs_info:
                code += 'input = %s\n' % (', '.join([inp.repr_code() for inp in self.inputs_info]))
            if self.outputs_info:
                code += 'output = %s\n' % (', '.join([out.repr_code() for out in self.outputs_info]))
            code += '"""\n'
            if 'step' in self._code:
                code += self._code['step'] + '\n'
            for fname in ['init', 'run', 'animate', 'stop']:
                if fname in self._code:
                    code += 'def %s():\n' % fname
                    for l in self._code[fname].split('\n'):
                        code += '    ' + l
                    code += '\n'
            return code

    def set_code(self, code):
        from openalea.oalab.model.parse import parse_docstring, get_docstring, extract_functions
        self._initial_code = code
        model, self.inputs_info, self.outputs_info = parse_docstring(code)
        funcs = extract_functions(code)
        self.set_step_code(code)

        for fname in ['init', 'run', 'animate']:
            if fname in funcs:
                self.set_func_code(fname, funcs[fname])

        self._doc = get_docstring(code)
