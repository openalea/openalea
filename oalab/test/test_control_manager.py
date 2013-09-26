'''
from openalea.oalab.control.controlmanager import ControlManager, ControlABC

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

    
'''


from openalea.oalab.control.mapper import Mapper

def test_mapper_filter():
    mapper = Mapper()
    assert mapper._filterType("color_map") == "colormap"

def test_mapper_get_manager():
    mapper = Mapper()
    class Ctrl(object):
        def __init__(self):
            self.metatype = "color_map"
    control = Ctrl()   
    manag1 = mapper.getManager(control)
    manag2 = mapper.getManagerByType("color_map")
    assert manag1 == manag2