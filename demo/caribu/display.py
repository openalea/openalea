__license__ = "Cecill-C"
__revision__ = " $Id: display.py 1586 2009-01-30 15:56:25Z cokelaer $ "

from openalea.plantgl.all import *
import random
import types

# TODO: store data (optics and transparencies in the scene
# Methods to color the scene, and the vertices.
# Add static methods to the scene
# test it with randomized values and color map
# Implement discrete color map (lut?)

class CanestraScene(object):
    def __init__(self, plants, soil, indexes):
        self.plants = plants
        self.soil = soil
        self.indexes = indexes
        self.scene = None

    def build_scene(self,
                    leaf_material=None, 
                    stem_material=None, 
                    soil_material=None):
        if not leaf_material:
            leaf_material = Material(Color3(0,180,0))

        if not stem_material:
            stem_material = Material(Color3(0,130,0))
        if not soil_material:
            soil_material = Material(Color3(170,85,0))

        scene = Scene()
        for id, plant in self.plants.iteritems():
            leaves = plant["leaves"]
            stems = plant["stems"]
            for lid, leaf in leaves.iteritems():
                shape = Shape(leaf, leaf_material)
                shape.name = str(lid)
                scene.add(shape)
            if len(stems.pointList) >0:
                shape = Shape(stems, stem_material)
                shape.name = str(id)
                scene.add(shape)
        if "soil" in self.soil:
            shape = Shape(self.soil["soil"], soil_material)
            scene.add(shape)
            
        self.scene = scene

    def build_scene_with_colors(self, colors):
        scene = Scene()
        for i, (label, count) in enumerate(self.indexes):
            pid = plant_id(label)
            plant = self.plants[pid]
            if is_leaf(label):
                lid = leaf_id(label)
                geom = plant["leaves"][lid]
            elif is_stem(label):
                geom = plant["stems"]
            else:
                geom = self.soil["soil"]
            if count == 0:
                geom.colorList = []
                geom.colorPerVertex=False
            
            assert 3*len(geom.colorList) == count
            if type(colors[i])==types.FloatType:
                geom.colorList.append(Color4(10,random.randint(0,255),30,0))
            else:
                r,g,b=colors[i]
                geom.colorList.append(Color4(r,g,b,0))

        for plant in self.plants.values():
            leaves = plant["leaves"]
            stems = plant["stems"]
            for leaf in leaves.values():
                scene += leaf
            if len(stems.pointList) >0:
                scene += stems
        if "soil" in self.soil:
            scene += self.soil["soil"]

        self.scene = scene

    def plot(self, colors = None):
        if not self.scene and not colors:
            self.build_scene()
        if colors:
            self.build_scene_with_colors(colors)

        if self.scene.isValid():
            Viewer.display(self.scene)
            
            
            


def process_line( line ):
    line = line.strip()
    if line[0] == '#':
        return None

    l = line.split()
    nb_polygon = int(l[-10])
    assert nb_polygon == 3
    coords = map(float,l[-9:])
    label = l[2]
    triangle = (Vector3(*coords[:3]), 
                Vector3(*coords[3:6]), 
                Vector3(*coords[6:]))
    return label, triangle
    

def read(fn):
    f = open(fn)
    index = 0
    elements = []
    for l in f.readlines():
        elt = process_line(l)
        if elt:
            elements.append(elt)
    f.close()
    return elements

def build_geometry(elements):
    plants = {}
    soil = {}
    indexes = []
    for i,(label, triangle) in enumerate(elements):
        pid = plant_id(label)
        if pid not in plants:
            plants[pid] = {"leaves":{},"stems":TriangleSet([],[])}

        plant = plants[pid]

        if is_leaf(label):
            lid = leaf_id(label)
            leaves = plant['leaves']
            if lid not in leaves:
                leaves[lid]=TriangleSet([],[])
            shape = leaves[lid]
        elif is_stem(label):
            shape = plant['stems']
        else:
            assert is_soil(label)
            if "soil" not in soil:
                soil["soil"]=TriangleSet([],[])
            shape = soil["soil"]

        count = len(shape.pointList)
        shape.pointList.append(triangle[0])
        shape.pointList.append(triangle[1])
        shape.pointList.append(triangle[2])
        shape.indexList.append(Index3(count, count+1,count+2))
        indexes.append((label,count))

    return CanestraScene(plants, soil, indexes)


def optical_species(label):
    return int(label[:-11])

def plant_id(label):
    return int(label[-11:-6])

def transparency(label):
    return int(bool(leaf_id(label)))

def leaf_id(label):
    return int(label[-6:-3])

def is_soil(label):
    return optical_species(label)==0 and transparency(label)==0

def is_leaf(label):
    return leaf_id(label) > 0

def is_stem(label):
    return (not is_leaf(label)) and (not is_soil(label))

def transparencies(indexes):
    return [transparency(t[0]) for t in indexes]

def optics(indexes): 
    return [optical_species(t[0]) for t in indexes]


def test(fn):
    elements = read(fn)
    plants, soil, indexes = build_geometry(elements)
    scene = build_scene(plants, soil)
    Viewer.display(scene)

