from openalea.oalab.model.parse import InputObj, OutputObj
from openalea.core.model import Model

import copy

from openalea.core.control.manager import ControlManager
cm = ControlManager()


def namespace(ns_global, ns_local):
    # Move to runner class (model manager or ParadigmEditor)

    namespace = {}
    namespace.update(ns_global)
    namespace.update(ns_local)
    namespace.update(cm.namespace())

    return namespace


class ModelManager(object):

    def __init__(self):
        self._items = {}

    def __call__(self, name):
        model = copy.copy(self._items[name])
        model._global_ns.update(namespace(globals(), locals()))
        return model

    def register(self, model):
        self._items[model.name] = model


def test_copy():
    m = Model(name='m1')
    m.set_step_code('c=a+b')
    m.inputs_info = [InputObj('a'), InputObj('b')]
    m.outputs_info = [OutputObj('c')]

    m2 = copy.copy(m)
    assert m is not m2
    assert m.step_code == m2.step_code
    assert [inp.name for inp in m2.inputs_info] == ['a', 'b']
    assert [out.name for out in m2.outputs_info] == ['c']


def test_output():
    step_code = 'c=a+b'

    m = Model('sum')
    m.inputs_info = [InputObj('a'), InputObj('b')]
    m.outputs_info = [OutputObj('c')]
    m.step_code = step_code

    assert m.run(a=1, b=2) == 3


def test_steps():
    step_code = 'a += 10'

    m = Model('sum')
    m.inputs_info = [InputObj('a=0')]
    m.outputs_info = [OutputObj('a')]
    m.step_code = step_code

    assert m.run() == 10
    assert m.run(nstep=10) == 100


def test_global_and_control():
    m1 = Model('IOFullyDefined')
    m1.inputs_info = [InputObj('a=0'), InputObj('b=0')]
    m1.outputs_info = [OutputObj('c')]
    m1.set_step_code('c=a+b')

    m2 = Model('IOWithoutDefault')
    m2.inputs_info = [InputObj('a'), InputObj('b')]
    m2.outputs_info = [OutputObj('c')]
    m2.set_step_code('c=a+b')

    m3 = Model('NoIO')
    m3.outputs_info = [OutputObj('c')]
    m3.set_step_code('c=a+b')

    ms1 = Model('CheckModelCall')
    ms1.outputs_info = [OutputObj('c')]

    mm = ModelManager()
    mm.register(m1)
    mm.register(m2)
    mm.register(m3)

    from openalea.core.service.control import new_control
    new_control('a', 'IInt', 10)
    a = 123456789
    ns = namespace(globals(), locals())
    ns['Model'] = mm

    ms1.set_step_code('m = Model("IOFullyDefined")\nc = m.run()')
    assert ms1.run(namespace=ns) == 0
    ms1.set_step_code('m = Model("IOFullyDefined")\na=44\nc = m.run(b=22)')
    assert ms1.run(namespace=ns) == 22
    ms1.set_step_code('m = Model("IOFullyDefined")\na=44\nc = m.run(a=11, b=22)')
    assert ms1.run(namespace=ns) == 33
    ms1.set_step_code('m = Model("IOFullyDefined")\na=44\nc = m.run(a)')
    assert ms1.run(namespace=ns) == 44

    assert m1.run() == 0  # 0
    assert m2.run(1, 2) == 3  # 3
    assert m2.run(2, b=3) == 5  # 5
    assert m2.run(a=3, b=4) == 7  # 7

    # a, b not defined, use default a=0, b=0. Do not use global a because a is not a free variable
    assert m1.run(namespace=ns) == 0
    # m2.run(namespace=ns)  # FAIL, b not defined
    # m3.run(namespace=ns)  # FAIL, b not defined

    assert m1.run(1, 2, namespace=ns) == 3  # 3
    assert m2.run(2, b=3, namespace=ns) == 5  # 5
    assert m2.run(a=3, b=4, namespace=ns) == 7  # 7
    assert m3.run(a=3, b=4, namespace=ns) == 7  # 7

    b = 20
    ns = namespace(globals(), locals())
    ns['Model'] = mm

    ms1.set_step_code('m = Model("IOWithoutDefault")\nc = m.run()')
    assert ms1.run(namespace=ns) == 30  # 30 free variables a, b use global var a, b
    ms1.set_step_code('m = Model("IOWithoutDefault")\na=456\nc = m.run(a=11, b=22)')
    assert ms1.run(namespace=ns) == 33  # 33
    ms1.set_step_code('m = Model("IOWithoutDefault")\na=33\nc = m.run(b=22)')
    assert ms1.run(namespace=ns) == 32  # 32 a use control value
    ms1.set_step_code('m = Model("IOWithoutDefault")\na=44\nc = m.run(a)')
    assert ms1.run(namespace=ns) == 64  # 64

    assert m1.run() == 0  # 0
    assert m2.run(1, 2) == 3  # 3
    assert m2.run(2, b=3) == 5  # 5
    assert m2.run(a=3, b=4) == 7  # 7

    assert m1.run(namespace=ns) == 0  # Do not use global a or b because a and b are not free variables
    assert m2.run(namespace=ns) == 30  # 30
    assert m3.run(namespace=ns) == 30  # 30

    assert m1.run(1, 2, namespace=ns) == 3  # 3
    assert m2.run(2, b=3, namespace=ns) == 5  # 5
    assert m2.run(a=3, b=4, namespace=ns) == 7  # 7
    assert m3.run(a=3, b=4, namespace=ns) == 7  # 7

    cm.clear()


def test_global_and_control_it():
    from openalea.core.service.control import new_control

    m1 = Model('IterateIOFullyDefined')
    m1.inputs_info = [InputObj('a=0')]
    m1.outputs_info = [OutputObj('a')]
    m1.set_step_code('a+=1')

    m2 = Model('IterateIOWithoutDefault')
    m2.inputs_info = [InputObj('a')]
    m2.outputs_info = [OutputObj('a')]
    m2.set_step_code('a+=1')

    m3 = Model('IterateNoIO')
    m3.outputs_info = [OutputObj('a')]
    m3.set_step_code('a+=1')

    m4 = Model('IterateNoIO')
    m4.set_step_code('a+=1')

    ms1 = Model('IterateCheckModelCall')
    ms1.outputs_info = [OutputObj('c')]

    mm = ModelManager()
    mm.register(m1)
    mm.register(m2)
    mm.register(m3)

    new_control('a', 'IInt', 10)
    a = 123456789
    ns = namespace(globals(), locals())
    ns['Model'] = mm

    nstep = 3

    ms1.set_step_code('m = Model("IterateIOFullyDefined")\nc = m.run()')
    assert ms1.run(namespace=ns, nstep=nstep) == 1
    ms1.set_step_code('m = Model("IterateIOFullyDefined")\nc = m.run(nstep=3)')
    assert ms1.run(namespace=ns, nstep=nstep) == (0 + 3)

    assert m1.run(nstep=nstep) == (0 + nstep)
    assert m2.run(1, nstep=nstep) == (1 + nstep)
    assert m2.run(a=2, nstep=nstep) == (2 + nstep)

    # a, b not defined, use default a=0, b=0. Do not use global a because a is not a free variable
    assert m1.run(namespace=ns, nstep=nstep) == (0 + nstep)
    # m2.run(namespace=ns)  # FAIL, b not defined
    # m3.run(namespace=ns)  # FAIL, b not defined

    assert m1.run(1, namespace=ns, nstep=nstep) == (1 + nstep)
    assert m2.run(2, namespace=ns, nstep=nstep) == (2 + nstep)
    assert m2.run(a=10, namespace=ns, nstep=nstep) == (10 + nstep)
    assert m3.run(a=10, namespace=ns, nstep=nstep) == (10 + nstep)

    cm.clear()

code = """
model1 = Model("m1")
model2 = Model("m1")

model1.run() # m1=1
model2.run() # m2=1

model1.step() # m1=2, m2=1
model1.step() # m1=3, m2=1
m1 = model1.step() # m1=4, m2=1
m2 = model2.step() # m1=4, m2=2
"""


def test_multiple_call():
    """
    Check each model instance has is own namespace
    """
    model1 = Model('m1')
    model1.inputs_info = [InputObj('a=0')]
    model1.outputs_info = [OutputObj('a')]
    model1.set_step_code('a+=1')

    model2 = Model('m2')
    model2.outputs_info = [OutputObj('m1'), OutputObj('m2')]
    model2.set_step_code(code)

    mm = ModelManager()
    mm.register(model1)

    ns = dict(Model=mm)

    m1, m2 = model2.run(namespace=ns)
    assert m1 == 4
    assert m2 == 2

cm.clear()
