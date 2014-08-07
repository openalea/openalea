
from openalea.lpy.__lpy_kernel__ import LpyParsing
from openalea.lpy.gui.objectmanagers import get_managers
from openalea.lpy.gui.scalar import ProduceScalar
from openalea.oalab.control.control import Control
from openalea.oalab.service.interface import guess
from openalea.plantgl.all import Material, NurbsCurve2D
from openalea.plantgl.oaplugins.controls import to_color
from openalea.lpy import Lsystem
from openalea.core.path import path

from openalea.oalab.service.control import register as register_control

def export_lpy_controls(controls, filename):
    """
    :param controls: [('name', interface, value)] ex: [('i', IInt(min=0, max=100), 1)]
    """

    from openalea.lpy.gui.objectmanagers import get_managers
    #from openalea.plantgl.oaplugins.interfaces import IMaterialList, IPatch, IQuantisedFunction, ICurve2D
    managers = get_managers()
    interface2manager = { 'IPatch' : managers['NurbsPatch'], 'IQuantisedFunction' : managers['Function'], 'ICurve2D' : managers['Curve2D']}

    visuobjects = []
    for name, interface, value in controls:
            manager = interface2manager.get(interface.__class__.__name__, None)
            if manager:
                print 'Export '+name+' ...'
                value.name = str(name)
                visuobjects.append((manager,value))

    visualparameters = ({},visuobjects)


    from openalea.lpy.simu_environ import getInitialisationCode

    
    code = getInitialisationCode(visualparameters=[visualparameters])

    f = open(filename, 'w')
    f.write(code)
    f.close()

def import_lpy_controls(filepath):
    if not path(filepath).isfile():
        return

    control = dict()

    f = open(filepath, 'r')
    script = f.read()
    f.close()

    if script is None: script = ""
    beginTag = LpyParsing.InitialisationBeginTag
    if not beginTag in script:
        return str(script), control
    else:
        txts = str(script).split(beginTag)
        new_script = txts[0]
        context_to_translate = txts[1]
        context = Lsystem().context()
        context.initialiseFrom(beginTag + context_to_translate)

    managers = get_managers()
    visualparameters = []
    scalars = []
    functions = []
    curves = []
    geoms = []

    lpy_code_version = 1.0
    if context.has_key('__lpy_code_version__'):
        lpy_code_version = context['__lpy_code_version__']
    if context.has_key('__scalars__'):
        scalars_ = context['__scalars__']
        scalars = [ ProduceScalar(v) for v in scalars_ ]
    if context.has_key('__functions__') and lpy_code_version <= 1.0 :
        functions = context['__functions__']
        for n, c in functions: c.name = n
        functions = [ c for n, c in functions ]
        funcmanager = managers['Function']
        geoms += [(funcmanager, func) for func in functions]
    if context.has_key('__curves__') and lpy_code_version <= 1.0 :
        curves = context['__curves__']
        for n, c in curves: c.name = n
        curves = [ c for n, c in curves ]
        curvemanager = managers['Curve2D']
        geoms += [ (curvemanager, curve) for curve in curves ]
    if context.has_key('__parameterset__'):
        for panelinfo, objects in context['__parameterset__']:
            for typename, obj in objects:
                visualparameters.append((managers[typename], obj))

    for scalar in scalars:
        control[unicode(scalar.name)] = scalar.value
    for (manager, geom) in geoms:
        if geom != list():
            control[geom.getName()] = geom
    for (manager, geom) in visualparameters:
        if geom != list():
            control[geom.getName()] = geom

    new_controls = []
    for name, value in control.items():
        interfaces = guess(value)
        if interfaces:
            new_controls.append(Control(name, interfaces[0], value))

    try:
        control["color map"] = to_color(context.turtle.getColorList())
    except AttributeError:
        pass
    else:
        new_controls.append(Control("color map", 'IColorList', control["color map"]))

    for control in new_controls:
        register_control(control)

