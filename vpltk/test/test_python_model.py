# -*- python -*-
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2014 INRIA - CIRAD - INRA
#
#       File author(s): Julien Coste <julien.coste@inria.fr>
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
from openalea.core.model import PythonModel


def test_model_get_documentation():
    model_src = '''"""
This is the doc of my model
"""

print "ok"
result = 42


"""
ok
"""
'''
    model = PythonModel(code=model_src)
    assert model.get_documentation() == "This is the doc of my model"


def test_model_inputs_info():
    model_src = '''"""

input = x:int=4, y:float=3.14, z, debug:bool
output = success

beautifull doc
"""

print "ok"
'''
    model = PythonModel(code=model_src)
    assert len(model.inputs_info) == 4
    assert len(model.outputs_info) == 1
    assert model.inputs_info[0].name == "x"
    assert model.inputs_info[0].default == "4"
    # assert model.inputs_info[0].interface == "int"
    assert model.inputs_info[1].name == "y"
    assert model.inputs_info[1].default == "3.14"
    # assert model.inputs_info[1].interface == "float"
    assert model.inputs_info[2].name == "z"
    assert model.inputs_info[3].name == "debug"
    # assert model.inputs_info[3].interface == "bool"
    assert model.outputs_info[0].name == "success"

    print model.get_documentation()
    assert model.get_documentation() == """input = x:int=4, y:float=3.14, z, debug:bool
output = success

beautifull doc"""

    model_src2 = '''"""

input = x=[1,2,3], y=(1,2), z=(1,), a=4, b
output = c, d, e:bool

beautifull doc
"""

print "ok"
'''
    model2 = PythonModel(code=model_src2)
    assert len(model2.inputs_info) == 5
    assert len(model2.outputs_info) == 3
    assert model2.inputs_info[0].name == "x"
    assert model2.inputs_info[0].default == "[1,2,3]"
    assert model2.inputs_info[1].name == "y"
    assert model2.inputs_info[1].default == "(1,2)"
    assert model2.inputs_info[2].name == "z"
    assert model2.inputs_info[2].default == "(1,)"
    assert model2.inputs_info[3].name == "a"
    assert model2.inputs_info[3].default == "4"
    assert model2.inputs_info[4].name == "b"
    assert model2.outputs_info[0].name == "c"
    assert model2.outputs_info[1].name == "d"
    assert model2.outputs_info[2].name == "e"
    # assert model2.outputs_info[2].interface == "bool"

    assert model2.get_documentation() == """input = x=[1,2,3], y=(1,2), z=(1,), a=4, b
output = c, d, e:bool

beautifull doc"""


def test_repr_code():
    model_src = '''"""

input = x:int=4, y:float=3.14, z, debug:bool
output = success

beautifull doc
"""

print "ok"
'''
    model = PythonModel(code=model_src)
    assert model.repr_code() == model_src


def test_magic():
    model_src = '''"""

input = x:int=4, y:float=3.14, z, debug:bool
output = success

beautifull doc
"""

%pylab inline

print "ok"
'''
    model = PythonModel(code=model_src)
    assert model.repr_code() == model_src
    assert model.get_documentation() is not None
    assert len(model.inputs_info) == 4
    assert len(model.outputs_info) == 1


def test_magic_not_first_line():
    model_src = '''
%pylab inline

print "ok"

"""

input = x:int=4, y:float=3.14, z, debug:bool
output = success

beautifull doc
"""
'''
    model = PythonModel(code=model_src)
    assert model.repr_code() == model_src
    assert model.get_documentation() is not None
    assert len(model.inputs_info) == 4
    assert len(model.outputs_info) == 1

