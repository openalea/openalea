

def decode(mimetype, mimedata):
    """
    decode("openalealab/model", "model1") -> Model("model1")
    returns an object Model of model1
    """
    if mimetype == 'openalealab/control':
        from openalea.oalab.control.manager import ControlManager
        identifier, name = mimedata.split(';')
        control = ControlManager().control(name)
        if isinstance(control, list):
            return ControlManager().control(uid=identifier)
    elif mimetype == 'openalealab/data':
        return mimedata

def encode(data, mimetype=None):
    """
    encode(Model("model1")) -> ("openalealab/model", "model1")
    returns a tuple mimetype, mimedata
    """
    from openalea.oalab.control.control import Control
    from openalea.core.path import path
    if isinstance(data, Control) or mimetype == 'openalealab/control':
        return ('openalealab/control', '%s;%s' % (data.identifier, data.name))
    elif mimetype == 'openalealab/data':
        return ('openalealab/data', data)
