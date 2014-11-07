
from openalea.core.service.model import ModelFactory
from openalea.core.service.data import DataFactory
from openalea.oalab.model.parse import InputObj, OutputObj
from openalea.oalab.gui.paradigm.python import PythonModelController


def test_constructor():
    model = ModelFactory(mimetype='text/x-python')
    model.inputs_info = [InputObj('a'), InputObj('b')]
    model.outputs_info = [OutputObj('c')]
    model.set_step_code('c = a + b')

    # Use a non existing directory to be sure data is not written on disk
    data = DataFactory('/tmp/donotexists/test.py', default_content="print('I am a python file')")
    c1 = "print('hello, I am a new model')"
    c2 = "print('hello, I am a new data')"

    kwds = [
        dict(name='Model1', content=c1),
        dict(filepath='/tmp/donotexists/test.py', content=c2),
        dict(model=model),
        dict(data=data),
    ]

    controller = PythonModelController(**kwds[0])
    assert controller.value() == c1
    assert hasattr(controller.model, 'run')

    controller = PythonModelController(**kwds[1])
    assert controller.value() == c2
    assert hasattr(controller.model, 'run')
    assert hasattr(controller._obj, 'run') is False

    controller = PythonModelController(**kwds[2])
    assert controller._obj is model
    assert hasattr(controller.model, 'run')

    controller = PythonModelController(**kwds[3])
    assert controller._obj is data
    assert hasattr(controller.model, 'run')
