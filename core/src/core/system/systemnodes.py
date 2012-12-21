# -*- python -*-
#
#       OpenAlea.Core
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA
#
#       File author(s): Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#                       Christophe Pradal <christophe.prada@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################
"""System Nodes"""

__license__ = "Cecill-C"
__revision__ = " $Id$ "

from openalea.core.node import AbstractNode, Node, Annotation
from openalea.core.dataflow import SubDataflow


class AnnotationNode(Annotation):
    """ A DummyNode is a fake node."""

    __graphitem__ = "annotation.Annotation"

    def get_nb_input(self):
        """ Return the nb of input ports """
        return 0

    def get_nb_output(self):
        """ Return the nb of output ports """
        return 0

    def eval(self):
        return False


class IterNode(Node):
    """ Iteration Node """

    def __init__(self, *args):
        """ Constructor """

        Node.__init__(self, *args)
        self.iterable = "Empty"

    def reset(self):
        """ Reset to the intial state """
        self.iterable = "Empty"
        if hasattr(self,'nextval'):
            del self.nextval

    def eval(self):
        """
        Return True if the node need a reevaluation
        """
        try:
            if self.iterable == "Empty":
                self.iterable = iter(self.inputs[0])

            if(hasattr(self, "nextval")):
                self.outputs[0] = self.nextval
            else:
                self.outputs[0] = self.iterable.next()

            self.nextval = self.iterable.next()
            return True

        except TypeError, e:
            self.outputs[0] = self.inputs[0]
            return False

        except StopIteration, e:
            self.iterable = "Empty"
            if(hasattr(self, "nextval")):
                del self.nextval
            return False

class IterWithDelayNode(IterNode):
    """ Iteration Node """

    def eval(self):
        """
        Return True if the node need a reevaluation
        """
        try:
            if self.iterable == "Empty":
                self.iterable = iter(self.inputs[0])

            if(hasattr(self, "nextval")):
                self.outputs[0] = self.nextval
            else:
                self.outputs[0] = self.iterable.next()

            self.nextval = self.iterable.next()
            return self.inputs[1]

        except TypeError, e:
            self.outputs[0] = self.inputs[0]
            return False

        except StopIteration, e:
            self.iterable = "Empty"
            if(hasattr(self, "nextval")):
                del self.nextval
            return False

class StopSimulation(Node):
    """ Iteration Node """

    def __init__(self, *args):
        """ Constructor """

        Node.__init__(self, *args)
        self.reset()

    def reset(self):
        self._nb_cycles = 0

    def eval(self):
        """
        Stop the simulation after a given number of steps
        """
        nb_cycles = self.inputs[1]
        self.outputs[0] = self.inputs[0]
        self._nb_cycles += 1
        if self._nb_cycles < nb_cycles:
            return 1
        else:
            return False

class Counter(Node):
    """ Loop a number of cycle, then stop """

    def __init__(self, *args):
        """ Constructor """

        Node.__init__(self, *args)
        self.reset()

    def reset(self):
        self._current_cycle = None

    def eval(self):
        """
        Stop the simulation after a given number of steps
        """
        start, stop, step = self.inputs[:3]
        delay = self.delay
        if self._current_cycle is None:
            self._current_cycle = start
            self.outputs[0] = self._current_cycle
            return delay

        if self._current_cycle+step < stop:
            self._current_cycle+= step
            self.outputs[0] = self._current_cycle
            return delay
        
        return False

class RDVNode(Node):
    """
    Rendez Vous node (synchronisation)
    In1 : Value
    In2 : Unused (control flow)
    Out : Value, result of the control flow evaluation
    """

    def __call__(self, inputs):
        """ inputs is the list of input values """
        return inputs[0], inputs[1]


from openalea.core.datapool import DataPool


class PoolReader(Node):
    """
    In : Name (key)
    Out : Object (value)
    """

    def __init__(self, inputs, outputs):

        Node.__init__(self, inputs, outputs)
        self.pool = DataPool()

    def __call__(self, inputs):
        """ inputs is the list of input values """

        key = inputs[0]
        obj = self.pool.get(key)
        if key in self.pool:
            self.set_caption("%s"%(key, ))
        return (obj, )


class PoolWriter(Node):
    """
    In :  Name (String), Object (Any)
    """

    def __init__(self, inputs, outputs):

        Node.__init__(self, inputs, outputs)
        self.pool = DataPool()

    def __call__(self, inputs):
        """ inputs is the list of input values """

        key = inputs[0]
        obj = inputs[1]
        self.set_caption("%s = %s"%(key, obj))
        self.pool[key] = obj
        return (obj, )

class PoolDefault(Node):
    """
    In : Name (key), Default Value
    Out : Object (value)
    """

    def __init__(self, inputs, outputs):

        Node.__init__(self, inputs, outputs)
        self.pool = DataPool()

    def reset(self):
        if hasattr(self,'key'):
            del self.pool[self.key]

    def __call__(self, inputs):
        """ inputs is the list of input values """

        key = inputs[0]
        default_value = inputs[1]
        self.default = default_value
        self.key = key
        obj = self.pool.setdefault(key, default_value)
        if key in self.pool:
            self.set_caption("%s"%(key,))
        else:
            self.set_caption("%s = %s"%(key,default_value))
        return (obj, )

class InitNode(Node):
    """
    In0 : Init value
    In1 : Current Value
    In2 : State (Bool)

    If state is true, return In0, else return In1
    state is set to false in the first execution.
    """
    def __init__(self, inputs, outputs):

        Node.__init__(self, inputs, outputs)
        self.state = True

    def __call__(self, inputs):
        """ inputs is the list of input values """


        if(self.state):
            ret = inputs[0]
        else:
            ret = inputs[1]

        self.state = False
        return (ret, )

    def reset(self):
        Node.reset(self)
        self.state = True


class AccuList(Node):
    """ List Accumulator
    
    Add to a list (in datapool) the receive value
    
    :param inputs: a list containing the value to append and 
        the name of the datapool variable
    
    """

    def __init__(self, inputs, outputs):

        Node.__init__(self, inputs, outputs)
        self.pool = DataPool()

    def __call__(self, inputs):

        varname = inputs[1]
        value = inputs[0]
        if(not varname):
            varname = "AccuList_%i"%(id(self))

        # Create datapool variable if necessary
        if(not self.pool.has_key(varname) or
           not isinstance(self.pool[varname], list)):
            l = list()
            self.pool[varname] = l
        else:
            l = self.pool[varname]

        self.set_caption("list accumulator : %s"%(repr(str(varname))))
        l.append(value)

        return (l, )


class AccuFloat(Node):
    """ Float Accumulator

    Add to a Float (in datapool) the receive value

    :param inputs: a list containing the value to append and 
        the name of the datapool variable

    """

    def __init__(self, inputs, outputs):

        Node.__init__(self, inputs, outputs)
        self.pool = DataPool()

    def __call__(self, inputs):

        varname = inputs[1]
        value = inputs[0]
        if(not varname):
            varname = "AccuFloat_%i"%(id(self))

        # Create datapool variable if necessary
        if(not self.pool.has_key(varname) or
           not isinstance(self.pool[varname], float)):
            self.pool[varname] = 0.

        self.set_caption("float accumulator : %s"%(repr(str(varname))))
        self.pool[varname] += float(value)
        return (self.pool[varname], )


class LambdaVar(Node):
    """ Return a lambda variable """
    #cpt = 0
    
    def __init__(self, *args):
        Node.__init__(self, *args)
        print 'args ', args
        self.set_caption("X")
        #self.set_caption("X" + str(LambdaVar.cpt))
        #LambdaVar.cpt = 1

    def __call__(self, inputs):
        return SubDataflow(None, None, 0, 0)


class Delay(Node):
    """ Return the previous value or an initial value """

    def __init__(self, *args):
        Node.__init__(self, *args)
        self.previous = None

    def __call__(self, inputs):
        init, x = inputs[:2]

        if self.previous is None:
            res = self.previous = init 
        else:
            res = self.previous
            self.previous = x

        return res,

    def reset(self):
        """ Reset to the intial state """
        self.previous = None

class WhileUniVar(Node):
    """ While Loop Univariate
    In 0 : Initial value
    In 1 : Test function
    In 2 : Process Function

    Out 0 : Result value
    """

    def __call__(self, inputs):

        value = inputs[0]
        test = inputs[1]
        func = inputs[2]

        cpt = 0
        while(test(value)):

            newvalue = func(value)

            # Test for infinite loop
            if(value == newvalue):
                cpt +=1
                if(cpt > 1000):
                    raise RuntimeError("Infinite Loop")
            else:
                value = newvalue
            print value

        return (value, )


class WhileMultiVar(Node):
    """ While Loop Multivariate
    In 0 : List of initial value
    In 1 : Test function
    In 2 : List of Process Function

    Out 0 : Result variables
    """

    def __call__(self, inputs):

        values = inputs[0]
        test = inputs[1]
        funcs = inputs[2]

        cpt = 0
        while(test(*values)):
            newvals = []


            for f in funcs:
                res = f(*values)
                newvals.append(res)

            # Test for infinite loop
            if(values == newvals):
                cpt +=1
                if(cpt > 1000):
                    raise RuntimeError("Infinite Loop")
            else:
                values = newvals

            print values

        return values

def while_multi2(values, test, function):
        cpt = 0
        while(test(*values)):
            newvals = function(*values)

            # Test for infinite loop
            if(values == newvals):
                cpt +=1
                if(cpt > 1000):
                    raise RuntimeError("Infinite Loop")
            else:
                values = newvals

            print values

        return values

def system_cmd(str_list):
    """ Execute a system command
    Input : a list of string
    Output : subprocess stdout, stderr
    """

    import subprocess

    return subprocess.Popen(str_list, stdout=subprocess.PIPE).communicate()

def shell_command(cmd, directory):
    """ Execute a command in a shell
    cmd : the command as a string
    dir : the directory where the cmd is executed
    Output : status
    """
    from subprocess import Popen,STDOUT, PIPE

    p = Popen(cmd, shell=True, cwd=directory,
        stdin=PIPE, stdout=STDOUT, stderr=STDOUT)
    status = p.wait()
    return status,

class For(Node):
    """ While Loop Univariate
    In 0 : Initial value
    In 1 : Sequence
    In 2 : Process Function

    Out 0 : Result value
    """

    def __call__(self, inputs):

        value = inputs[0]
        l = inputs[1]
        func = inputs[2]

        for i in l:
            value = func(value, i)

        return (value, )


def get_data(pattern='*.*', pkg_name=None, as_paths=False):
    """ Return all data that match the pattern """
    from openalea.core.pkgmanager import PackageManager
    pm = PackageManager()
    result = pm.get_data(pattern, pkg_name, as_paths)
    nodes = [x.instantiate() for x in result]
    for node in nodes:
        node.eval() 
    names = [x.name for x in result]
    filenames = [node.get_output(0) for node in nodes]
    return dict(zip(names,filenames))
