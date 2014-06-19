# -*- python -*-
#
#       OpenAlea.Core
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA
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
""" a script to run alea dataflow and scripts"""

__license__ = "Cecill-C"
__revision__ = "$Id$"

import sys
from optparse import OptionParser
#import threading
from openalea.core.pkgmanager import PackageManager


def start_qt(factory, node):
    """ Start QT, and open widget of factory, node

    :param factory: todo
    :param node: todo

    """

    from openalea.vpltk.qt import QtGui, QtCore

    app = QtGui.QApplication(sys.argv)

    # CTRL+C binding
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    dialog = QtGui.QDialog()
    widget = factory.instantiate_widget(node, autonomous=True)

    dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    widget.setParent(dialog)

    vboxlayout = QtGui.QVBoxLayout(dialog)
    vboxlayout.setContentsMargins(3, 3, 3, 3)
    vboxlayout.setSpacing(5)
    vboxlayout.addWidget(widget)

    dialog.setWindowTitle(factory.name)
    dialog.show()

    app.exec_()


def load_package_manager(*args):
    """ Return the package manager

    :param pkg_id:  package id
    :param node_id: node id
    :returns: package manager

    """
    pm = PackageManager()
    pm.init(verbose=False)

    return pm


def get_node(component, inputs, pm=None):
    """ retrieve a node from its component name and inputs

    :param component: todo
    :param inputs: todo
    :param pm: package manager

    """

    pkg_id, node_id = component

    if (not pm):
        pm = load_package_manager()

    try:
        factory = pm[pkg_id][node_id]
    except Exception, e:
        print "Cannot run node %s:%s" % (pkg_id, node_id)
        query(component, pm)
        raise e

    node = factory.instantiate()

    if (inputs):
        for k, v in inputs.iteritems():
            try:
                node.set_input(k, v)
            except KeyError, e:
                print "Unknown input %s" % (k, )
                query(component, pm)
                raise e

    return factory, node


def run_and_display(component, inputs, gui=False, pm=None):
    """ run component with inputs

    :param component: todo
    :param inputs: todo
    :param gui: todo
    :param pm: package manager
    :type gui: boolean (default is False)
    :type pm: package manager

    """
    factory, node = get_node(component, inputs, pm)

    if (not gui):

        try:
            node.eval()
            print _outputs(node)
        except Exception, error:
            print "Error while executing component : ", error
            print "Try with -g flag"
        return

    else:
        start_qt(factory, node)


def run(component, inputs, pm=None, vtx_id=-1):
    """ Run component with inputs. can exit by exception.

    If node_id is given, eval the dataflow from that node and return the result.
    """

    _factory, node = get_node(component, inputs, pm)

    if vtx_id < 0:
        node.eval()
        return _outputs(node)
    else:
        node.eval_as_expression(vtx_id)
        return _outputs(node.node(vtx_id))

def query(component, pm=None):
    """ show help of component """

    pkg_id, node_id = component

    if (not pm):
        pm = load_package_manager()

    # package not found
    if (not pkg_id or not pm.has_key(pkg_id)):

        print "Package '%s' not found." % (pkg_id)
        print "\nAvailable packages are :"

        keys = pm.keys()
        keys.sort()

        for p in keys:
            print "   ", p

        return

    pkg = pm[pkg_id]

    if(not pkg.has_key(node_id)):
        print "Unknown node '%s'" % (node_id, )
        node_id = None

    # query package
    print "\nPackage"
    print "-------"
    print "name : ", pkg.name

    for key, info in pkg.metainfo.iteritems():
        print "%s : %s" % (key, info)

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
        print "Name : %s" % (factory.name)
        print "Documentation : %s" % (doc, )
        print "Inputs:"
        for i in xrange(node.get_nb_input()):
            port = node.get_input_port(i)
            print "  ", port.get_tip()
        print "Outputs:"
        for port in node.output_desc:
            print "  ", port.get_tip()


def parse_component(name):
    """ Return (pkg_id, node_id) from name """

    tname = name.split('/')
    if(len(tname)<2):
        tname = name.split(':')

    if(len(tname) == 1):
        return (tname[0], None)
    elif(len(tname) == 2):
        return (tname[0], tname[1])
    else:
        raise ValueError("Component name error :\
            cannot parse 'pkg_id:node_id'")


def get_intput_callback(option, opt_str, value, parser):
    """todo"""
    assert value is None

    value = {}
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
            v = arg.split("=")
            if(len(v) != 2):
                raise ValueError("Invalid input %s" % (str(arg)))


            value[v[0]] = v[1]
            del rargs[0]


    for k, v in value.iteritems():
        try:
            v = eval(v)
            value[k] = v
        except:
            pass

    setattr(parser.values, option.dest, value)

def function(factory):
    ''' Return a function which is evaluated like a python function.

    factory is a NodeFactory.
    '''
    node = factory.instantiate()

    def f(*args, **kwds):
        for i, v in enumerate(args):
            node.set_input(i,v)
        for k, v in kwds.iteritems():
            node.set_input(k,v)

        node.eval()

        nb_output = node.get_nb_output()
        return tuple(node.output(i) for i in range(nb_output))
    
    return f


def _outputs(node):
    #return node.outputs
    return [node.output(i) for i in range(node.get_nb_output())]

def main():
    """ Parse options """

        # options
    usage = """
%prog [-r|-q] package_id[:node_id] [-i key1=val1 key2=val2 ...]
or
%prog [-r|-q] package_id[/node_id] [-i key1=val1 key2=val2 ...]
"""
    parser = OptionParser(usage=usage)

    parser.add_option("-q", "--query", dest="query",
                       help="Show package/component help.",
                       action="store_true",
                       default=True)

    parser.add_option("-r", "--run", dest="run",
                       help="Run component.",
                       action="store_true",
                       default=False)

    parser.add_option("-g", "--gui",
                       help="Open graphical user interface",
                       action="store_true", default=False)

    parser.add_option("-l", "--local_data",
                       help="Data are local (ie in current directory)",
                       action="store_true", default=False)


    parser.add_option("-i", "--input",
                       action="callback", callback=get_intput_callback,
                       help="Specify inputs as KEY=VALUE, KEY=VALUE...",
                       dest="input")

    try:
        (options, args)= parser.parse_args()
    except Exception, error:
        parser.print_usage()
        print "Error while parsing args:", error
        return

    if(len(args) < 1):
        parser.error("Incomplete command : specify a 'package_id:node_id'")

    component = parse_component(args[0])

    # Execute
    if(options.local_data):
        import openalea.core.data
        openalea.core.data.PackageData.__local__ = True

    if(options.run):
        run_and_display(component, options.input, options.gui)
    else:
        query(component, )


if __name__ == "__main__":
    main()


# this example need to be fixed
#python alea.py -r -g "adel.macro:6 plot_scene"
#-i leafdb="'$OPENALEAPKG/adel/adel/data/leaves1.db'"
# lsystem="'$OPENALEAPKG/adel/adel/lsystem/Adel.l'"
