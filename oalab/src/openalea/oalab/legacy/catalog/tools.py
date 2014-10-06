# -*- python -*-
#
#       Plugin System for vpltk
# 
#       OpenAlea.VPLTk: Virtual Plants Lab Toolkit
#
#       Copyright 2013 INRIA - CIRAD - INRA
#
#       File author(s): Guillaume Baty <guillaume.baty@inria.fr>
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

import inspect
from openalea.oalab.legacy.catalog import Catalog

def color_interface_line(interface_id):
        catalog = Catalog()
        interface = catalog.interface(interface_id)
        hierarchy = [cl.__name__ for cl in reversed(inspect.getmro(interface)) if cl in catalog._interfaces.values()]
        hierarchy = ' > '.join(hierarchy)
        return '\033[93m%s\033[91m   (%s)\033[0m' % (interface_id, hierarchy)

def list_interfaces():
    catalog = Catalog()

    print '=========='
    print 'Interfaces'
    print '=========='

    for interface_id in sorted(catalog.interfaces()):
        interface = catalog.interface(interface_id)
        print color_interface_line(interface_id)
        print '       defined in:', interface.__module__
        print
    print

def list_implementations():
    catalog = Catalog()

    print '==============='
    print 'Implementations'
    print '==============='

    for interface_id in catalog.interfaces():
        print color_interface_line(interface_id)
        for factory in catalog.factories(interfaces=interface_id, exclude_tags=['wralea']):
            print '  *', factory.name
        print

