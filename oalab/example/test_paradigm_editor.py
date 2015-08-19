

from openalea.core.data import PythonFile
from openalea.core.model import PythonModel
from openalea.core.path import tempdir

from openalea.oalab.testing.applet import test_applet

code = """
'''
output=out
'''
a=1
def f():
    return(a)

out = f()
print out
"""


def load_data():
    model = PythonModel(name='func')
    model.set_code(code)

    tmpdir = tempdir()

    data = PythonFile(content=code, path=tmpdir / "test.py")

    # ns is provided by tester
    editor = ns['editor_manager']
    editor.open_data(data)


if __name__ == '__main__':
    tests = [
        load_data
    ]
    test_applet('EditorManager', tests=tests)
