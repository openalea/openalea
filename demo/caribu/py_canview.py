__license__ = "Cecill-C"
__revision__ = " $Id: py_canview.py 1586 2009-01-30 15:56:25Z cokelaer $ "

from openalea.core import *
import display

def read_can(fn):
    if not fn:
        return 
    elements = display.read(fn)
    canestra_scene = display.build_geometry(elements)
    return canestra_scene

def read_vec(fn):
    if not fn:
        return 
    f=open(fn)
    s=f.read()
    f.close()
    l=s.split()
    l= map(float,l)
    return l,

def plot_can(fn,colors):
    scene = read_can(fn)
    if scene:
        scene.build_scene()
        scene.plot(colors)
    
class CanestraDisplay(Node):

    def __init__(self):
        Node.__init__(self)

        self.add_input( name = "Canestra Scene" )
        self.add_input( name = "plants", interface = IEnumStr(['all']), value = 'all' )
        self.add_input( name = "optical species", interface = IEnumStr(['all']), value = 'all' )
        self.add_input( name = "transparency", interface = IEnumStr(['all']), value = 'all' )
        self.add_input( name = "color map", interface = IFunction )
            
        self.add_output( name = "PlantGL scene") 
        self.can_scene = None
        
    def __call__(self, can_scene, plant_id, opt_id, t_id, cmap):
        if not can_scene:
            return
        pids = can_scene.plants.keys()
        oids = set(display.transparencies(can_scene.indexes))
        tids = set(display.optics(can_scene.indexes))

        if can_scene != self.can_scene:
            # update the enum str with new values
            self.can_scene = can_scene

        # plant color 
        # leaf, stem, soil
        # vertices
        if int(plants_id) not in pids:
            plant_id = 'all'
        if int(opt_id) not in oids:
            opt_id = 'all'
        if int(t_id) not in tids:
            t_id = 'all'

        
        
