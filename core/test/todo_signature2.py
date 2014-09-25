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

def h():
    pass
g.__inputs__ = "a:int"
g.__outputs__ = "result:bool"

def i():
    pass
g.__inputs__ = "a"
g.__outputs__ = "result"

def j():
    pass
g.__inputs__ = "a:int=42, b:bool=False"
g.__outputs__ = "result"

def k():
    pass
g.__inputs__ = "a:int=42", "b:bool=False"
g.__outputs__ = "result"

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
    assert in_['interface'] == IInt
    assert out_['name'] == 'result'
    assert out_['value'] == 'True'
    assert out_['interface'] == IBool

def test_inputs_outputs3():
    # TODO value
    in_ = sign_inputs(h)[0]
    out_ = sign_outputs(h)[0]
    
    assert in_['name'] == 'a'
    #assert in_['value'] == '42'
    assert in_['interface'] == IInt
    assert out_['name'] == 'result'
    #assert out_['value'] == 'True'
    assert out_['interface'] == IBool
    
def test_inputs_outputs4():
    # TODO value, interface
    in_ = sign_inputs(h)[0]
    out_ = sign_outputs(h)[0]
    
    assert in_['name'] == 'a'
    #assert in_['value'] == '42'
    #assert in_['interface'] == IInt
    assert out_['name'] == 'result'
    #assert out_['value'] == 'True'
    #assert out_['interface'] == IBool

def test_inputs_outputs5():
    # TODO
    pass
    
def test_inputs_outputs6():
    # TODO
    pass
