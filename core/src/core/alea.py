# -*- python -*-
#
#       OpenAlea.Core
#
#       Copyright 2006-2008 INRIA - CIRAD - INRA  
#
#       File author(s): Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

import os, sys
from optparse import OptionParser

from openalea.core.pkgmanager import PackageManager

#global package manager
pm = None


def load_package_manager(pkg_id, node_id):
    """ Return the package manager """
 
    print "\nSearching '%s:%s'..."%(pkg_id, node_id)
    
    pm = PackageManager()
    pm.init(verbose=False)

    return pm


def run(component, inputs, gui=False, pm=None):
    """ run component with inputs"""
    
    pkg_id, node_id = component
    
    if(not pm):
        pm = load_package_manager(pkg_id, node_id)

    try:
        node = pm.get_node(pkg_id, node_id)
    except Exception, e:
        node = None
    
    if(not node):

        print "Cannot run node %s:%s"%(pkg_id, node_id)
        query(component, pm)
        return
    
    if(inputs):
        for k,v in inputs.iteritems():
            try:
                node.set_input(k, v)
            except KeyError:
                print "Unknown input %s"%(k,)
                query(component, pm)
                return
                   
    node.eval()
    
    print node.outputs



def query(component, pm=None):
    """ show help of component """

    pkg_id, node_id = component

    if(not pm):
        pm = load_package_manager(pkg_id, node_id)

    # package not found
    if(not pkg_id or not pm.has_key(pkg_id)):
        
        print "Package '%s' not found."%(pkg_id)
        print "\nAvailable packages are :" 

        keys = pm.keys()
        keys.sort()

        for p in keys:
            print "   ", p
        
        return

    pkg = pm[pkg_id]
        
    if(not pkg.has_key(node_id)):
        print "Unknown node '%s'"%(node_id,)
        node_id = None

    # query package
    print "\nPackage"
    print "-------"
    print "name : ", pkg.name
        
    for key, info in pkg.metainfo.iteritems():
        print "%s : %s"%(key, info)

    if(not node_id):
        keys = pkg.keys()
        keys.sort()

        print "\nAvailable nodes are:"
        for k in keys:
            print "   ", pkg[k].get_id()
            
    # query node
    else:
        factory = pkg[node_id]
        node = factory.instantiate()
        doc = node.__doc__

        if doc:
            doc = doc.split('\n')
            doc = [x.strip() for x in doc] 
            doc = '\n'.join(doc)
        else:
            doc = factory.description

        print "\nComponent"
        print "---------"
        print "Name : %s"%(factory.name)
        print "Documentation : %s"%(doc,)
        print "Inputs:"
        for i in xrange(node.get_nb_input()):
            port = node.get_input_port(i)
            print "  ", port.get_tip()
        print "Outputs:"
        for port in node.output_desc:
            print "  ", port.get_tip()

            

        
        


def parse_component(name):
    """ Return (pkg_id, node_id) from name """

    tname = name.split(':')
    
    if(len(tname) == 1):
        return (tname[0], None)
    elif(len(tname) == 2):
        return (tname[0], tname[1])
    else:
        raise ValueError("Component name error : cannot parse 'pkg_id:node_id'")
    


def get_intput_callback(option, opt_str, value, parser):

    assert value is None
    done = 0
    value = []
    rargs = parser.rargs
    while rargs:
        arg = rargs[0]

        # Stop if we hit an arg like "--foo", "-a", "-fx", "--file=f",
        # etc.  Note that this also stops on "-3" or "-3.0", so if
        # your option takes numeric values, you will need to handle
        # this.
        if ((arg[:2] == "--" and len(arg) > 2) or
            (arg[:1] == "-" and len(arg) > 1 and arg[1] != "-")):
            break
        else:
            value.append(arg)
            del rargs[0]

    param_list = ",".join(value)
    try:
        dict = eval("dict(%s)"%(param_list,))
    except:
        raise ValueError("Invalid inputs %s"%(str(value)))

    setattr(parser.values, option.dest, dict)




def main():
    """ Parse options """
    
        # options
    usage = "usage: %prog [-r|-q] [-c package_id:node_id] [-i key1=val1 key2=val2]"
    parser = OptionParser(usage=usage)

    parser.add_option( "-c", "--component", dest="component",
                       help="Component is 'pkg_id:node_id'.",
                       default=None)

    parser.add_option( "-q", "--query", dest="query",
                       help="Show package/component help.",
                       action="store_true",
                       default=True)

    parser.add_option( "-r", "--run", dest="run",
                       help="Run component.",
                       action="store_true",
                       default=False)

    parser.add_option( "-g", "--gui",
                       help="Open graphical user interface",
                       action="store_true", default=False)

    parser.add_option( "-i", "--input", 
                       action="callback", callback=get_intput_callback,
                       help="Specify inputs as KEY=VALUE, KEY=VALUE...",
                       dest="input"
                       )

    (options, args)= parser.parse_args()

    if(options.component is None):
        parser.error("Need to specify component (-c option)")

    component = parse_component(options.component)


    if(options.run):
        print options.input
        run(component, options.input)
    else:
        query(component)






if(__name__ == "__main__"):
    main()
