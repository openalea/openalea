# -*- python -*-
# -*- coding: utf8 -*-
#
#       OpenAlea.OALab
#
#       Copyright 2014 INRIA - CIRAD - INRA
#
#       File author(s): Frédéric Boudon <frederic.boudon@inria.fr>
#
#       File contributor(s):
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################


def serialize_controls(controls):
    yield 'from openalea.core.control import Control\n\n'
    yield 'controls = []\n'
    moduleset = set()
    for c in controls:
        interfaceklass = c.interface.__class__.__name__
        interfacemodule = c.interface.__class__.__module__
        if not (interfaceklass, interfacemodule) in moduleset:
            yield 'from %s import %s\n\n' % (interfacemodule, interfaceklass)
            moduleset.add((interfaceklass, interfacemodule))
        if hasattr(c.interface, 'module_dependence'):
            moddepends = c.interface.module_dependence()
            if type(moddepends) == str:
                moddepends = [moddepends]
            for moddep in moddepends:
                if moddep not in moduleset:
                    yield "from %s import *\n\n" % moddep
                    moduleset.add(moddep)
        else:
            valueklass = c.value.__class__.__name__
            valuemodule = c.value.__class__.__module__
            if ((not valuemodule == '__builtin__') and
                    (not (valueklass, valuemodule) in moduleset)):
                yield 'from %s import %s\n\n' % (valuemodule, valueklass)
                moduleset.add((valueklass, valuemodule))
        yield 'minterface = ' + repr(c.interface) + '\n'
        yield 'mcontrol = Control(%r, minterface, %r)\n' % (c.name, c.value)
        yield 'controls.append(mcontrol)\n\n'


def save_controls(controls, filename):
    f = open(filename, 'w')
    for l in serialize_controls(controls):
        f.write(l)
    f.close()
