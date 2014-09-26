
def save_controls(controls, filename):
    f = open(filename, 'w')
    f.write('from openalea.core.service.control import new_control\n\n')
    moduleset = set()
    for c in controls:
        interfaceklass = c.interface.__class__.__name__
        interfacemodule = c.interface.__class__.__module__
        if not (interfaceklass, interfacemodule) in moduleset:
            f.write(
                'from %s import %s\n\n' % (interfacemodule, interfaceklass)
            )
            moduleset.add((interfaceklass, interfacemodule))
        if hasattr(c.interface, 'module_dependence'):
            moddepends = c.interface.module_dependence()
            if type(moddepends) == str:
                moddepends = [moddepends]
            for moddep in moddepends:
                if moddep not in moduleset:
                    f.write("from %s import *\n\n" % moddep)
                    moduleset.add(moddep)
        else:
            valueklass = c.value.__class__.__name__
            valuemodule = c.value.__class__.__module__
            if ((not valuemodule == '__builtin__') and
                    (not (valueklass, valuemodule) in moduleset)):
                f.write('from %s import %s\n\n' % (valuemodule, valueklass))
                moduleset.add((valueklass, valuemodule))
        f.write('minterface = ' + repr(c.interface) + '\n')
        f.write('mcontrol = new_control(' + repr(c.name) +
                ',minterface,' + repr(c.value) + ')\n\n')
    f.close()
