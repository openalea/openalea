import modulesample1
    
def test_module_info():
    assert modulesample1.__doc__ == 'Module documentation'

def test_factory():
    assert (not hasattr(modulesample1.f, '__factory__'))
    assert (hasattr(modulesample1.f1, '__factory__'))
    
def test_inputs():
    # check function with @inputs has a non empty attribute __inputs__
    pass

def test_outputs():
    # check function with @inputs has a non empty attribute __outputs__
    pass

