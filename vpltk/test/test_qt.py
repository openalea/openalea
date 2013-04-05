from openalea.vpltk.qt import qt

import sip

def test_api():
    """
    Only usefull if you want to use IPython shell.
    If you prefer classical Python shell, you will have
    sip.getapi("QString") == 1
    """
    assert sip.getapi("QString") == 2
