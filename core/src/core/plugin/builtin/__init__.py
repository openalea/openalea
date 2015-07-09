
from openalea.core.plugin import PluginDef


@PluginDef
class PythonModel(object):
    implements = ['IModel']

    dtype = 'Python'
    mimetype = 'text/x-python'

    def __call__(self):
        from openalea.core.model import PythonModel
        return PythonModel


@PluginDef
class PythonFile(object):
    implements = ['IData']

    mimetype = 'text/x-python'
    default_name = 'Python'
    default_file_name = "script.py"
    pattern = "*.py"
    extension = "py"
    icon = ":/images/resources/Python-logo.png"

    def __call__(self):
        from openalea.core.data import PythonFile
        return PythonFile
