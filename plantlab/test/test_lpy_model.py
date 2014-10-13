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
from openalea.plantlab.lpy import LPyModel


def test_model_get_documentation():
    model_src = '''"""
input = lstring="_(0.01)-(90)F(1)"
output = lstring
"""
N = 2

derivation length: N

production:

F(x) :
  produce  F(x/3.0)+F(x/3.0)--F(x/3.0)+F(x/3.0)

endlsystem
'''
    model = LPyModel(code=model_src)
    assert model.get_documentation() == """input = lstring="_(0.01)-(90)F(1)"
output = lstring"""

    assert model.repr_code() == model_src


def test_model_inputs_info():
    model_src = '''"""
input = lstring="_(0.01)-(90)F(1)", a=1
output = lstring
"""
N = 2

derivation length: N

production:

F(x) :
  produce  F(x/3.0)+F(x/3.0)--F(x/3.0)+F(x/3.0)

endlsystem
'''
    model = LPyModel(code=model_src)
    assert len(model.inputs_info) == 2
    assert len(model.outputs_info) == 1
    assert model.inputs_info[0].name == "lstring"
    assert eval(model.inputs_info[0].default) == "_(0.01)-(90)F(1)"
    assert model.inputs_info[1].name == "a"
    assert model.inputs_info[1].default == "1"
    assert model.outputs_info[0].name == "lstring"


def test_magic():
    model_src = '''"""
input = lstring="_(0.01)-(90)F(1)", a=1
output = lstring
"""

%pylab inline
N = 2

derivation length: N

production:

F(x) :
  produce  F(x/3.0)+F(x/3.0)--F(x/3.0)+F(x/3.0)

endlsystem
'''
    model = LPyModel(code=model_src)
    assert model.repr_code() == model_src
    assert len(model.inputs_info) == 2
    assert len(model.outputs_info) == 1


def test_magic_not_first_line():
    model_src = '''
%pylab inline
N = 2

derivation length: N

production:

F(x) :
  produce  F(x/3.0)+F(x/3.0)--F(x/3.0)+F(x/3.0)

endlsystem

"""
input = lstring="_(0.01)-(90)F(1)", a=1
output = lstring
"""
'''
    model = LPyModel(code=model_src)
    assert model.repr_code() == model_src
    assert len(model.inputs_info) == 2
    assert len(model.outputs_info) == 1