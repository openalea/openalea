from openalea.plantlab.lpy import import_lpy_file

lpy_str = """
Axiom: A
derivation length: 24
production:

A :    
	produce [+(60)B][-(60)B]F?P(0,0,0)A

B :
	produce F?P(0,0,0)@O(0.2)B

?P(x,y,z) :
    if 4*y*y +(z-10)**2 > 100:
        produce [+(2*z)F][-(2*z)F]%
    else:
        produce *
###### INITIALISATION ######
__lpy_code_version__ = 1.1

def __initialiseContext__(context):
	import openalea.plantgl.all as pgl
	Color_1 = pgl.Material("Color_1" , ambient = (65,45,15) , diffuse = 3 , )
	Color_1.name = "Color_1"
	context.turtle.setMaterial(1,Color_1)
	Color_4 = pgl.Material("Color_4" , ambient = (0,0,127) , diffuse = 1.09449 , )
	Color_4.name = "Color_4"
	context.turtle.setMaterial(4,Color_4)
	Color_5 = pgl.Material("Color_5" , ambient = (60,60,15) , diffuse = 3 , )
	Color_5.name = "Color_5"
	context.turtle.setMaterial(5,Color_5)
	Color_6 = pgl.Material("Color_6" , ambient = (78,0,117) , diffuse = 1.53846 , specular = (0,0,0) , )
	Color_6.name = "Color_6"
	context.turtle.setMaterial(6,Color_6)
	Color_7 = pgl.Material("Color_7" , ambient = (65,45,15) , diffuse = 3 , )
	Color_7.name = "Color_7"
	context.turtle.setMaterial(7,Color_7)
	Color_8 = pgl.Material("Color_8" , ambient = (0,0,0) , diffuse = 3 , specular = (0,0,0) , shininess = 0 , )
	Color_8.name = "Color_8"
	context.turtle.setMaterial(8,Color_8)
	Color_10 = pgl.Material("Color_10" , ambient = (0,0,255) , diffuse = 0 , specular = (0,0,0) , shininess = 0 , )
	Color_10.name = "Color_10"
	context.turtle.setMaterial(10,Color_10)
	context.options.setSelection('Module inheritance',1)
	import openalea.plantgl.all as pgl
	profile = pgl.BezierCurve2D(	
	    pgl.Point3Array([(0.00304516, 0.989158, 1),(0.919709, 0.988049, 1),(0.989333, 0.451245, 1),(0.942931, 0.0692266, 1),(0.432096, 0.0477193, 1),(-0.00755788, 0.0124374, 1)]) , 
	    )
	profile.name = "profile"
	profile2 = pgl.BezierCurve2D(	
	    pgl.Point3Array([(0.00030319, 0.144896, 1),(0.110857, 0.341659, 1),(0.279505, 0.157395, 1),(0.260455, 0.0381235, 1),(0.143832, -0.0595403, 1),(-0.00117527, 0.0996232, 1)]) , 
	    )
	profile2.name = "profile2"
	panel_0 = ({'active': True, 'visible': True, 'name': 'Panel 1'},[('Curve2D',profile),('Curve2D',profile2)])
	parameterset = [panel_0,]
	context["__functions__"] = []
	context["__curves__"] = [('profile',profile),('profile2',profile2),]
	context["__parameterset__"] = parameterset
	context["profile"] = profile
	context["profile2"] = profile2
	scalars = [('WITHLEAF', False, False, True), ('SEED', 1, 0, 100), ('WITH_TROPISM', False, False, True), ('TROPISM', 60, 0, 100), ('OLDSTRUCTURE', False, False, True), ('GENERATED_WITH_TROPISM', True, False, True), ('REGENERATE', True, False, True), ('COMPARE', True, False, True), ('FORCE_COMPARE', False, False, True), ('PROP_VIEW', True, False, True), ('RAMIF', 77, 0, 200), ('DETAILS', False, False, True)]
	context["__scalars__"] = scalars
	for n,v,mnv,mxv in scalars:
		context[n] = v
"""

def test_import_lpy():
    code, controls = import_lpy_file(lpy_str)
    assert controls["SEED"].value == 1
    assert controls["FORCE_COMPARE"].value == False
    assert controls["FORCE_COMPARE"].name == "FORCE_COMPARE"
    assert controls.has_key("color map")
    assert controls.has_key("profile")
    assert len(code) > 0
