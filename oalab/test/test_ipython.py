from openalea.core.interpreter import get_interpreter_class

def test_get_interpreter():  
    interpreter_class = get_interpreter_class()
    assert interpreter_class
