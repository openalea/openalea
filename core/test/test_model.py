import copy

from openalea.core.model import Model
from openalea.core.service.control import clear_controls, control_namespace
from openalea.core.service.project import create_project
from openalea.oalab.model.parse import InputObj, OutputObj


project = create_project('unittest', '/tmp/notwritable')


def register_model(model):
    project.add('model', model)


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

    register_model(m1)
    register_model(m2)
    register_model(m3)

    from openalea.core.service.control import new_control
    new_control('a', 'IInt', 10)
    a = 123456789
    ns = {}
    ns.update(control_namespace())
    ns['Model'] = project.get_runnable_model

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
    ns = locals()
    ns.update(control_namespace())
    ns['Model'] = project.get_runnable_model

    ms1.set_step_code('m = Model("IOWithoutDefault")\nc = m.run()')
    assert ms1.run(namespace=ns) == 30  # 30 free variables a, b. use global var a, b
    ms1.set_step_code('m = Model("IOWithoutDefault")\na=456\nc = m.run(a=11, b=22)')
    assert ms1.run(namespace=ns) == 33  # 33
    ms1.set_step_code('m = Model("IOWithoutDefault")\nc = m.run(b=22)')
    assert ms1.run(namespace=ns) == 32  # 32 a use control value, b set explicitly
    ms1.set_step_code('m = Model("IOWithoutDefault")\na=33\nc = m.run(b=22)')
    assert ms1.run(namespace=ns) == 55  # 55 a use parent model value, b set explicitly
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

    clear_controls()


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

    register_model(m1)
    register_model(m2)
    register_model(m3)

    new_control('a', 'IInt', 10)
    a = 123456789
    ns = {}
    ns.update(control_namespace())
    ns['Model'] = project.get_runnable_model

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

    clear_controls()

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

    project.add("model", model1)
    ns = {}
    ns['Model'] = project.get_runnable_model

    m1, m2 = project.run_model(model2, namespace=ns)
    assert m1 == 4
    assert m2 == 2


def test_parse_code():
    code = '''
"""
input = a,b
output = c
"""
c = a+b
'''
    from openalea.core.model import PythonModel

    m1 = PythonModel(name='m1', code=code)
    m2 = PythonModel(name='m2')

    m2.code = code

    m3 = PythonModel(name='m3')
    m3.set_code(code)

    assert m1.run(a=1, b=2) == 3
    assert m2.run(a=2, b=3) == 5
    assert m3.run(a=3, b=4) == 7

    m1 = PythonModel(name='ModelWithoutDoc')
    assert m1.get_documentation() == ''

    m1 = PythonModel(name='ModelWithDoc', code=code)
    assert m1.get_documentation()


def test_clean_ns():
    from openalea.core.model import PythonModel
    from openalea.core.service.ipython import interpreter
    interp = interpreter()
    interp.user_ns['ipython_ns'] = 1

    model = PythonModel(name='clean')
    model.outputs_info = [OutputObj('ns')]
    model.inputs_info = [InputObj('a=0'), InputObj('b')]
    model.set_step_code('local_to_model=1\nns = dir()')

    initial_ns = dict(initial_ns=1)
    model_local_ns = model(namespace=initial_ns, b=1)
    model_varname = ['a', 'b', 'local_to_model']
    for varname in model_varname:
        assert varname in model_local_ns
    for varname in model_varname:
        assert varname not in interp.user_ns
    assert 'ipython_ns' in interp.user_ns


def test_in_function():
    code = """
'''
output=out
'''
a=1
def f():
    return(a)

out = f()
"""
    from openalea.core.model import PythonModel
    model = PythonModel(name='func')
    model.set_code(code)
    assert model.init() == 1
