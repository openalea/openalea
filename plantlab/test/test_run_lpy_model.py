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


def test_run():
    model_src = '''"""
input = lstring="_(0.01)-(90)F(1)", N=2
output = lstring
"""

derivation length: N

production:

F(x) :
  produce  F(x/3.0)+F(x/3.0)--F(x/3.0)+F(x/3.0)

endlsystem
'''
    model = LPyModel(code=model_src)
    assert model is not None
    assert model.outputs == []
    result = model()

    true_result = "_(0.01)-(90)F(0.111111111111)+F(0.111111111111)--F(0.111111111111)+F(0.111111111111)+F(0.111111111111)+F(0.111111111111)--F(0.111111111111)+F(0.111111111111)--F(0.111111111111)+F(0.111111111111)--F(0.111111111111)+F(0.111111111111)+F(0.111111111111)+F(0.111111111111)--F(0.111111111111)+F(0.111111111111)"
    assert str(model.outputs) == true_result
    assert str(result) == true_result

    result = model("_(0.01)-(90)F(1)", 0)
    assert result == "_(0.01)-(90)F(1)"

    result = model(N=0)
    assert result == "_(0.01)-(90)F(1)"

    true_result2 = "F(0.111111111111)+F(0.111111111111)--F(0.111111111111)+F(0.111111111111)+F(0.111111111111)+F(0.111111111111)--F(0.111111111111)+F(0.111111111111)--F(0.111111111111)+F(0.111111111111)--F(0.111111111111)+F(0.111111111111)+F(0.111111111111)+F(0.111111111111)--F(0.111111111111)+F(0.111111111111)"
    result = model.run("F(1)")
    assert str(result) == true_result2

    result = model(N=0, lstring="F(1)")
    assert result == "F(1)"

    result = model(lstring="F(5)", N=0)
    assert result == "F(5)"


def test_step():
    model_src = '''"""
input = lstring="F(1)", N=3
output = lstring
"""

derivation length: N

production:

F(x) :
  produce  F(x)+F(x)

endlsystem
'''
    model = LPyModel(code=model_src)
    # model()
    result = model.init()
    assert str(result) == "F(1)"

    result = model.step()
    assert str(result) == "F(1)+F(1)"
    result = model.step()
    assert str(result) == "F(1)+F(1)+F(1)+F(1)"
    result = model.step()
    assert str(result) == "F(1)+F(1)+F(1)+F(1)+F(1)+F(1)+F(1)+F(1)"
    result = model.step()
    assert str(result) == "F(1)"
    result = model.step()
    assert str(result) == "F(1)+F(1)"

    result = model.init()
    assert str(result) == "F(1)"

    # result = model.animate() # Will display QGLViewer !!!
    # assert str(result) == "F(1)+F(1)+F(1)+F(1)+F(1)+F(1)+F(1)+F(1)"

    result = model.init()
    assert str(result) == "F(1)"

    result = model.run()
    assert str(result) == "F(1)+F(1)+F(1)+F(1)+F(1)+F(1)+F(1)+F(1)"


def test_default_in_out_lstring():
    # Issue 5, part 4
    model_src = '''
derivation length: 2

production:

F(x) :
  produce  F(x)+F(x)

endlsystem

'''
    model = LPyModel(code=model_src)
    result = model("F(1)")
    assert str(result) == "F(1)+F(1)+F(1)+F(1)"
