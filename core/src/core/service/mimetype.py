__all__ = [
    'decode',
    'encode',
]


def decode(mimetype, mimedata):
    """
    decode("openalealab/model", "model1") -> Model("model1")
    returns an object Model of model1
    """
    if mimetype == 'openalealab/control':
        from openalea.core.control.manager import ControlManager
        identifier, name = mimedata.split(';')
        control = ControlManager().control(name)
        if isinstance(control, list):
            return ControlManager().control(uid=identifier)
        return control
    elif mimetype == 'openalealab/data':
        from openalea.core.project.manager import ProjectManager
        from openalea.core.path import path
        pm = ProjectManager()
        return pm.get('data', path(mimedata).name)


def encode(data, mimetype=None):
    """
    encode(Model("model1")) -> ("openalealab/model", "model1")
    returns a tuple mimetype, mimedata
    """
    from openalea.core.control import Control
    from openalea.core.path import path
    if isinstance(data, Control) or mimetype == 'openalealab/control':
        return ('openalealab/control', '%s;%s' % (data.identifier, data.name))
    elif mimetype == 'openalealab/data':
        return ('openalealab/data', str(data.path))
