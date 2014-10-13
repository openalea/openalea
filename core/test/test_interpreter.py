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
from openalea.core.service.ipython import interpreter


def test_get_interpreter():
    interp = interpreter()
    assert interp is not None
    assert hasattr(interp, "user_ns")
    assert hasattr(interp, "run_cell")
    assert hasattr(interp, "runcode")


def test_get_interpreter_twice():
    interp = interpreter()
    interp2 = interpreter()
    assert interp is not None
    assert interp is interp2