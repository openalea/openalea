from openalea.core.signature2 import sign_inputs, sign_outputs
from openalea.core.interface import *

def f():
    pass
f.__inputs__ = "a:int=42"
f.__outputs__ = "result:bool=True"


def g():
    pass
g.__inputs__ = "a=42"
g.__outputs__ = "result=True"

def test_inputs_outputs():
    #assert sign_inputs(f) == [{'interface': openalea.core.interface.IInt, 'name': 'a', 'value': '42'}]
    #assert sign_outputs(f) == [{'interface': openalea.core.interface.IBool, 'name': 'result', 'value': 'True'}]
    in_ = sign_inputs(f)[0]
    out_ = sign_outputs(f)[0]
    
    assert in_['name'] == 'a'
    assert in_['value'] == '42'
    assert in_['interface'] == IInt
    assert out_['name'] == 'result'
    assert out_['value'] == 'True'
    assert out_['interface'] == IBool
    
def test_inputs_outputs2():
    #assert sign_inputs(f) == [{'interface': openalea.core.interface.IInt, 'name': 'a', 'value': '42'}]
    #assert sign_outputs(f) == [{'interface': openalea.core.interface.IBool, 'name': 'result', 'value': 'True'}]
    in_ = sign_inputs(g)[0]
    out_ = sign_outputs(g)[0]
    
    assert in_['name'] == 'a'
    assert in_['value'] == '42'
    #assert in_['interface'] == IInt
    assert out_['name'] == 'result'
    assert out_['value'] == 'True'
    #assert out_['interface'] == IBool

test_inputs_outputs()
test_inputs_outputs2()
