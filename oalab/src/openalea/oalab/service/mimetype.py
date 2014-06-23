

def decode(mimetype, mimedata):
    """
    decode("openalealab/model", "model1") -> Model("model1")
    returns an object Model of model1
    """
    if mimetype == 'openalealab/control':
        from openalea.oalab.control.manager import ControlManager
        return ControlManager().control(mimedata)

def encode(data):
    """
    encode(Model("model1")) -> ("openalealab/model", "model1")
    returns a tuple mimetype, mimedata
    """
    from openalea.oalab.control.control import Control
    if isinstance(data, Control):
        return ('openalealab/control', data.name)
