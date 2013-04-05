from openalea.vplab.control.controlmanager import ControlManager, ControlABC

def test_create_controls():
    """ Example of how to use control manager """ 
    class ControlExample(ControlABC):
        """ Empty class Control for test """
        def __init__(self):
            pass

    CM = ControlManager()
    CM.new_control("test1")
    C = ControlExample()
    CM.add_control("test2",C)
    
    assert len(CM.get_controls()) == 2

    

