
def save_controls(controls, filename):
    f = open(filename, 'w')
    f.write('from openalea.oalab.service import control\n\n')
    moduleset = set()
    for c in controls:
        interfaceklass = c.interface.__class__.__name__
        interfacemodule = c.interface.__class__.__module__
        if not (interfaceklass,interfacemodule) in moduleset:
            f.write('from '+interfacemodule+' import '+interfaceklass+'\n\n') 
            moduleset.add((interfaceklass,interfacemodule))
        if hasattr(c.interface, 'module_dependence'):
            moddepends = c.interface.module_dependence()
            if type(moddepends) == str:
                moddepends = [moddepends]
            for moddep in moddepends:
                if not moddep in moduleset:
                    f.write("from "+moddep+" import *\n\n")
                    moduleset.add(moddep)
        else:
            valueklass = c.value.__class__.__name__
            valuemodule = c.value.__class__.__module__
            if (not valuemodule == '__builtin__') and (not (valueklass,valuemodule) in moduleset):
                f.write('from '+valuemodule+' import '+valueklass+'\n\n')
                moduleset.add((valueklass,valuemodule))
        f.write('minterface = '+repr(c.interface)+'\n')
        f.write('mcontrol = control.new('+repr(c.name)+',minterface,'+repr(c.value)+')\n\n')
    f.close()