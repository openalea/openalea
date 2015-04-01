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

import unittest

from openalea.core.service.ipython import interpreter
from openalea.core.interpreter.python import Interpreter as PythonInterpreter
from openalea.core.interpreter.ipython import Interpreter as IPythonInterpreter


class TestCase(unittest.TestCase):

    def setUp(self):
        self.ip = interpreter()
        self.ipy = IPythonInterpreter()
        self.py = PythonInterpreter()

    def tearDown(self):
        pass

    def _run_all_interpreter(self, test):
        test(self.ip)
        test(self.ipy)
        test(self.py)

    def _run_cell(self, interp):
        interp.run_cell('a=1\nb=2\nc=a+b')
        assert 'c' in interp.user_ns
        dic = interp.get(['c'])
        assert dic == {'c': 3}

    def _delete(self, interp):
        interp.run_cell('a=1')
        assert 'a' in interp.user_ns
        interp.delete(['a'])
        assert 'a' not in interp.user_ns

    def _api(self, interp):
        assert interp is not None
        assert hasattr(interp, "user_ns")
        assert hasattr(interp, "run_cell")
        assert hasattr(interp, "run_code")
        assert hasattr(interp, "runcode")
        assert hasattr(interp, "loadcode")

    def test_api(self):
        self._api(self.ip)

    def test_run_cell(self):
        self._run_all_interpreter(self._run_cell)

    def test_delete(self):
        self._run_all_interpreter(self._delete)

    def test_get_interpreter_twice(self):
        interp = interpreter()
        interp2 = interpreter()
        assert interp is not None
        assert interp is interp2

if __name__ == '__main__':
    unittest.main()
